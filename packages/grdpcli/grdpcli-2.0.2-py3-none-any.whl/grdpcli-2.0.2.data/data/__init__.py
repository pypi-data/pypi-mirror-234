from grdpcli import *
from grdpcli.variables import *
from grdpcli.cmd_exec import *

def getNamespace():
    if not os.path.exists(GRDP_CURRENT_CONFIG_PATH):
        return 'default'
    with open(GRDP_CURRENT_CONFIG_PATH, 'r') as config_file:
        return json.load(config_file)['k8s_namespace']

class callbackServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_POST(self):
        post_data = self.rfile.read(int(self.headers['Content-Length']))
        response_data = json.loads(post_data.decode('utf-8'))
        self._set_headers()
        self.wfile.write(bytes("", "utf-8"))
        if checkToken(response_data['access_token']):
            with open(GRDP_AUTH_CONFIG_PATH, "w") as json_file:
                json.dump(response_data, json_file)
            logger.info(f"Authentificated Successfully")
            exit(0)
        return False

    def log_message(self, format, *args):
        return

class GRDPPortForward:
    def __init__(self, pod_name, pod_port, local_port, local_ip):
        self.pod_name = pod_name
        self.namespace = getNamespace()
        self.pod_port = pod_port
        self.local_port = local_port
        self.local_ip = local_ip
        self.runPortForward(self.pod_name, self.namespace, self.pod_port, self.local_port, self.local_ip)
        return

    def kubernetesProxy(self, pod_name, namespace, pod_port):
        config.load_kube_config()
        client_v1 = client.CoreV1Api()
        pf = portforward(client_v1.connect_get_namespaced_pod_portforward, pod_name, namespace, ports=str(pod_port))
        return pf

    def sendDatas(self, source, destination, is_client_socket):
        while True:
            try:
                data = source.recv(4096)
                if len(data) == 0:
                    break
                destination.sendall(data)
            except Exception as e:
                # TODO Bad file descriptor
                print(e)
                break
        source.close()
        destination.close()

    def runPortForward(self, pod_name, namespace, pod_port, local_port, local_ip):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((local_ip, int(local_port)))
        logger.info(f"Port forwarded from pod: {pod_name}:{pod_port} to {local_ip}:{local_port}")
        logger.info(f"Press CTRL+C to stop portforwarding...")
        server.listen(1)
        while True:
            client_socket, client_address = server.accept()
            remote_socket = self.kubernetesProxy(pod_name, namespace, pod_port).socket(int(pod_port))
            threading.Thread(target=self.sendDatas, args=(client_socket, remote_socket, True)).start()
            threading.Thread(target=self.sendDatas, args=(remote_socket, client_socket, False)).start()

class cmd():
    def __init__(self, exec_list=False, show_all=False):
        self.namespace = getNamespace()
        self.exec_list = exec_list
        self.show_all = show_all
        return

    def getPods(self):
        pods_names_only = []
        headers = ["NAME", "READY", "STATUS", "RESTARTS", "AGE"]
        table = []
        for pod in client.CoreV1Api().list_namespaced_pod(self.namespace).items:
            ready_status = "0/0"
            if self.exec_list:
                if pod.status.phase == "Running":
                    pods_names_only.append(pod.metadata.name)
            if pod.status.container_statuses:
                ready_containers = sum(1 for c in pod.status.container_statuses if c.ready)
                total_containers = len(pod.spec.containers)
                ready_status = f"{ready_containers}/{total_containers}"
            table.append([
                pod.metadata.name,
                ready_status,
                pod.status.phase,
                pod.status.container_statuses[0].restart_count if pod.status.container_statuses else "N/A",
                getAge((datetime.now(timezone.utc) - pod.metadata.creation_timestamp).total_seconds()),
            ])
        if pods_names_only:
            return pods_names_only
        if not table and self.exec_list:
            logger.error("No created pods found")
            exit(0)
        result = sendOutput(tabulate(table, headers=headers, tablefmt="plain"), self.show_all)
        if self.show_all:
            return result

    def getLogs(self, follow, pod_name):
        if follow:
            try:
                for logs in Watch().stream(client.CoreV1Api().read_namespaced_pod_log, name=pod_name, namespace=getNamespace()):
                    print(logs)
            except KeyboardInterrupt:
                exit(0)
        else:
            try:
                print(client.CoreV1Api().read_namespaced_pod_log(name=pod_name, namespace=getNamespace()))
            except ApiException as e:
                logger.error('Cannot get pod logs')

    def getIngress(self):
        headers = ["NAME", "HOSTS", "PORTS", "AGE"]
        table = []
        for ingress in client.ExtensionsV1beta1Api().list_namespaced_ingress(self.namespace).items:
            host = "".join(ingress.spec.rules[0].host) if ingress.spec.rules else ""
            ports = ingress.spec.rules[0].http.paths[0].backend.service_port

            table.append([
                ingress.metadata.name,
                host,
                ports,
                getAge((datetime.now(timezone.utc) - ingress.metadata.creation_timestamp).total_seconds()),
            ])
        result = sendOutput(tabulate(table, headers=headers, tablefmt="plain"), self.show_all)
        if self.show_all:
            return result

    def getServices(self):
        headers = ["NAME", "TYPE", "CLUSTER-IP", "EXTERNAL-IP", "PORT(S)", "AGE"]
        table = []
        for service in client.CoreV1Api().list_namespaced_service(self.namespace).items:
            ports = ", ".join([f"{p.port}/{p.protocol}" for p in service.spec.ports])
            table.append([
                service.metadata.name,
                service.spec.type,
                service.spec.cluster_ip,
                service.spec.external_i_ps[0] if service.spec.external_i_ps else "<none>",
                ports,
                getAge((datetime.now(timezone.utc) - service.metadata.creation_timestamp).total_seconds())
            ])
        result = sendOutput(tabulate(table, headers=headers, tablefmt="plain"), self.show_all)
        if self.show_all:
            return result

    def getPVC(self):
        headers = ["NAME", "STATUS", "VOLUME", "CAPACITY", "ACCESS MODES", "STORAGECLASS", "AGE"]
        table = []

        for pvc in client.CoreV1Api().list_namespaced_persistent_volume_claim(self.namespace).items:
            pvc_name = pvc.metadata.name
            pvc_status = pvc.status.phase
            pvc_volume = pvc.spec.volume_name if pvc.spec.volume_name else ""
            pvc_capacity = pvc.spec.resources.requests.get('storage', "") if pvc.spec.resources and pvc.spec.resources.requests else ""
            pvc_access_modes = ', '.join(pvc.spec.access_modes) if pvc.spec.access_modes else ""
            pvc_storage_class = pvc.spec.storage_class_name if pvc.spec.storage_class_name else ""

            table.append([
                pvc_name,
                pvc_status,
                pvc_volume,
                pvc_capacity,
                pvc_access_modes,
                pvc_storage_class,
                getAge(int((datetime.now(timezone.utc) - pvc.metadata.creation_timestamp).total_seconds()))
            ])

        result = sendOutput(tabulate(table, headers=headers, tablefmt="plain"), self.show_all)
        if self.show_all:
            return result

    def execJoin(self, pod_name, command='/bin/bash'):
        joinToPod(self.namespace, pod_name, command)

    def execSendCommand(self, pod_name, command='/bin/bash'):
        sendOutput(stream(client.CoreV1Api().connect_get_namespaced_pod_exec, name=pod_name, namespace=getNamespace(), command=command, stderr=True, stdin=False, stdout=True, tty=False).rstrip(), self.show_all)

def sendOutput(output, show_all=False):
    if show_all:
        return output
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logger = logging.getLogger(__name__)
    logger.info(output)

def getAge(age_seconds):
    if age_seconds >= 86400:
        age_str = f"{int(age_seconds / 86400)}d"
    elif age_seconds >= 3600:
        age_str = f"{int(age_seconds / 3600)}h"
    elif age_seconds >= 60:
        age_str = f"{int(age_seconds / 60)}m"
    else:
        age_str = f"{int(age_seconds)}s"
    return age_str

def printHelp(args):
    with open(HELP_CONTENT_PATH, "r") as help_file:
         Console().print(Markdown(help_file.read()))
    exit(0)

def checkToken(access_token):
    r = requests.get(f"{GITLAB_URL}/api/v4/projects", headers={"Authorization": f"Bearer {access_token}"}).status_code
    if int(r) == 200:
        return True
    return False

def getConfigData():
    if not os.path.exists(GRDP_AUTH_CONFIG_PATH):
        logger.error("Config not found")
        exit(1)
    with open(GRDP_AUTH_CONFIG_PATH, 'r') as config_file:
        return json.load(config_file)

def getCurrentConfigData():
    if not os.path.exists(GRDP_CURRENT_CONFIG_PATH):
        return False
    with open(GRDP_CURRENT_CONFIG_PATH, 'r') as config_file:
        return json.load(config_file)

def updateKubeConfig():
    namespace_name = getCurrentConfigData()['k8s_namespace']
    k8s_access_token = getCurrentConfigData()['k8s_access_token']
    k8s_authority_data = getConfigData()['k8s_authority_data']
    k8s_api_address = getConfigData()['k8s_api_address']
    config_template = kubectl_config_template.format(namespace_name=namespace_name, k8s_access_token=k8s_access_token, k8s_authority_data=k8s_authority_data, k8s_api_address=k8s_api_address)
    with open(GRDP_KUBE_CONFIG_PATH, 'w') as kube_config:
        kube_config.write(config_template)
    config.load_kube_config(config_file=GRDP_KUBE_CONFIG_PATH)
    return True

def updateGRDPConfig(access_token, refresh_token):
    with open(GRDP_AUTH_CONFIG_PATH, 'r') as json_file:
        data = json.load(json_file)
    data['access_token'] = access_token
    data['refresh_token'] = refresh_token
    with open(GRDP_AUTH_CONFIG_PATH, 'w') as json_file:
        json.dump(data, json_file)
    if getConfigData()['access_token'] == access_token and getConfigData()['refresh_token'] == refresh_token:
        return True
    return False

def getProjectVariables(project_id, access_token, variable_name=''):
    result = requests.get(f"{GITLAB_URL}/api/v4/projects/{project_id}/variables/{variable_name}", headers={"Authorization": f"Bearer {access_token}"})
    if int(result.status_code) == 200:
        return result.json()
    return None

def updateCurrentConfig(project_id, project_path_with_namespace, k8s_namespace, k8s_access_token):
    current_config_template = {
        "id": project_id,
        "project_path_with_namespace": project_path_with_namespace,
        "k8s_namespace": k8s_namespace,
        "k8s_access_token": k8s_access_token
    }
    with open(GRDP_CURRENT_CONFIG_PATH, 'w') as json_file:
        json.dump(current_config_template, json_file)

    if getCurrentConfigData()['id'] == project_id and getCurrentConfigData()['project_path_with_namespace'] == project_path_with_namespace:
        logger.info(f"Current project: {project_path_with_namespace}")
        return True
    return False

def refreshAccessToken():
    response = requests.get(f'{AUTH_ADDRESS}/refresh', headers={'Refresh-Token': f'{getConfigData()["refresh_token"]}',}).json()
    if updateGRDPConfig(response['access_token'], response['refresh_token']):
        return True
    return False

def getAllProjects(access_token):
    PROJECT_LIST = []
    page = 0
    while True:
        page = page + 1
        projects_dict = requests.get(f"{GITLAB_URL}/api/v4/projects?page={page}", headers={"Authorization": f"Bearer {access_token}"}).json()
        if not len(projects_dict) > 0:
            break
        PROJECT_LIST = PROJECT_LIST + projects_dict
    return PROJECT_LIST

def generateGitlabProjectsConfig():
    logger.info("Updating project config file. It may take a while, please wait...")
    projects = getAllProjects(getConfigData()['access_token'])
    projects_json = {}
    for i in projects:
        projects_json[i['path_with_namespace']] = i['id']
    with open(GRDP_PROJECTS_CONFIG_PATH, 'w') as json_file:
        json.dump(projects_json, json_file)
    return

def getProjectsListFromConfig():
    if not os.path.exists(GRDP_PROJECTS_CONFIG_PATH):
        generateGitlabProjectsConfig()
    with open(GRDP_PROJECTS_CONFIG_PATH, 'r') as json_file:
        return json.load(json_file)

def getGitProjectName():
    if not os.path.exists('.git'):
        logger.error("Git project not found. Please change directory to git repository folder.")
        exit(1)
    match = re.search(r':(.*?)\.git', git.Repo('.').remote('origin').url)
    if match:
        result = match.group(1)
        return result
    else:
        logger.error("Cannot get repository name")
        exit(1)
    return False

def printKubectlConfig():
    if not os.path.exists(GRDP_CURRENT_CONFIG_PATH):
        logger.error("Project is not selected")
        exit(1)
    with open(GRDP_KUBE_CONFIG_PATH, 'r') as file:
        print(file.read())
        exit(0)
