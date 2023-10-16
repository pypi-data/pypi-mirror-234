#!/usr/bin/env python
import os
import shutil
from distutils.core import setup

package_version = os.environ.get('CI_COMMIT_TAG', 'N\A')
package_name = 'grdpcli'
target_execute_path = '/usr/local/bin/grdp'

data_files=[
        ('grdpcli/__init__.py'),
        ('grdpcli/variables.py'),
        ('grdpcli/cmd_exec.py'),
        ('grdpcli/help_content.py'),
        ('grdpcli/version.py'),
    ]

#MacOS
if not os.path.exists(target_execute_path):
    shutil.copy('grdp', target_execute_path)

def package_files(data_files, directory_list):
    paths_dict = {}
    for directory in directory_list:
        for (path, directories, filenames) in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(path, filename)
                install_path = os.path.join('share', package_name, path)
                if install_path in paths_dict.keys():
                    paths_dict[install_path].append(file_path)
                else:
                    paths_dict[install_path] = [file_path]
    for key in paths_dict.keys():
        data_files.append((key, paths_dict[key]))
    return data_files

setup(name='grdpcli',
      version=package_version,
      description='Gitlab Rapid Development Platform CLI client',
      author='Anton Marusenko',
      author_email='anton.marusenko@onix-systems.com',
      url='https://onix-systems.com',
      data_files=package_files(data_files, ['grdpcli/']),
      install_requires=[
          'GitPython==3.1.24',
          'requests==2.27.1',
          'tabulate==0.9.0',
          'kubernetes==21.7.0',
          'rich==10.16.2',
          'questionary==2.0.1'
      ],
      scripts=["grdp"],
      python_requires='>=3'
     )
