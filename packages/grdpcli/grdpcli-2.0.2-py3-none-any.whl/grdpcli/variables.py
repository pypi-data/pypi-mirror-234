import re
import os
import sys
import tty
import pty
import git
import json
import time
import errno
import fcntl
import select
import signal
import struct
import socket
import termios
import logging
import argparse
import requests
import threading
import subprocess
import webbrowser
import questionary
from tabulate import tabulate
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime, timezone, timedelta
from kubernetes import client, config
from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.watch import Watch
from kubernetes.stream import stream
from kubernetes.stream import portforward
from kubernetes.stream.ws_client import PortForward
from rich.console import Console
from rich.markdown import Markdown

kubectl_blank_template = """
apiVersion: v1
clusters:
- cluster:
    server: https://grdpcli
  name: grdpcli
contexts:
- context:
    cluster: grdpcli
    user: grdpcli
  name: grdpcli
current-context: grdpcli
kind: Config
preferences: {}
"""

kubectl_config_template = """apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: {k8s_authority_data}
    server: {k8s_api_address}
  name: grdp-cluster
contexts:
- context:
    cluster: grdp-cluster
    namespace: {namespace_name}
    user: {namespace_name}
  name: {namespace_name}
current-context: {namespace_name}
kind: Config
preferences: {{}}
users:
- name: {namespace_name}
  user:
    token: {k8s_access_token}
"""

GITLAB_URL = 'https://gitlab.onix.ua'
LOCAL_HOSTNAME = '127.0.0.1'
LOCAL_SERVER_PORT = 65510
AUTH_ADDRESS = 'https://grdp-cli-auth.staging.onix.ua'
MANUAL_AUTH_ADDRESS = f'{AUTH_ADDRESS}/manual'
HELP_CONTENT_PATH = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), 'help_content.py'))
VERSION_FILE_PATH = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), 'version.py'))
GRDP_AUTH_CONFIG_FILE = 'grdp.config'
GRDP_PROJECTS_CONFIG_FILE = 'projects.config'
GRDP_CURRENT_CONFIG_FILE = 'current.config'
GRDP_KUBE_CONFIG_FILE = 'kube.config'
GRDP_HOME_DIRECTORY = os.path.join(os.path.expanduser("~"), '.grdp')
GRDP_AUTH_CONFIG_PATH = os.path.join(GRDP_HOME_DIRECTORY, GRDP_AUTH_CONFIG_FILE)
GRDP_PROJECTS_CONFIG_PATH = os.path.join(GRDP_HOME_DIRECTORY, GRDP_PROJECTS_CONFIG_FILE)
GRDP_CURRENT_CONFIG_PATH = os.path.join(GRDP_HOME_DIRECTORY, GRDP_CURRENT_CONFIG_FILE)
GRDP_KUBE_CONFIG_PATH = os.path.join(GRDP_HOME_DIRECTORY, GRDP_KUBE_CONFIG_FILE)

if not os.path.exists(GRDP_KUBE_CONFIG_PATH):
    if not os.path.exists(GRDP_HOME_DIRECTORY):
        os.mkdir(GRDP_HOME_DIRECTORY)
    with open(GRDP_KUBE_CONFIG_PATH, "w") as file:
        file.write(kubectl_blank_template)

config.load_kube_config(config_file=GRDP_KUBE_CONFIG_PATH)

ALL_RESOURCES_TEMPLATE = """
Pods:
{}
\nServices:
{}
\nVolumes:
{}
\nIngresses:
{}
    """

class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    green = "\x1b[38;5;115m"
    format = "%(message)s"
    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

logger = logging.getLogger('GRDPCLI')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

def getCurrentVersion():
    grdpcli_version = "N\A, build N\A"
    if os.path.exists(VERSION_FILE_PATH):
        grdpcli_version = open(VERSION_FILE_PATH, "r").read().strip().split('\n')
    return f"{grdpcli_version[0]}, build {grdpcli_version[1]}"
