import subprocess
from ConfigParser import SafeConfigParser
from sys import stdin
import getpass
import yaml

def progress(op_code, cur_count, max_count=None, message=''):
    print(cur_count)

# read config
config_parser = SafeConfigParser()
config_parser.read('configs')

laputa_api_commit = config_parser.get('laputa-api', 'commit')
laputa_api_port = int(config_parser.get('laputa-api', 'public_port'))

verpix_async_commit = config_parser.get('verpix-async', 'commit')

laputa_db_commit = config_parser.get('laputa-db', 'commit')
laputa_db_webui_port = int(config_parser.get('laputa-db', 'webui_public_port'))
laputa_db_port = int(config_parser.get('laputa-db', 'db_public_port'))

# clone all project
# ask for github auth
print("git clone laputa-api, verpix-async, laputa-db now")
user = raw_input("Username for 'https://github.com':")
passwd = getpass.getpass()

HTTPS_REMOTE_URL = 'https://'+user+':'+passwd+'@github.com/TopPano/laputa-api.git'
DEST_NAME = 'laputa-api'
subprocess.call(["git", "clone", HTTPS_REMOTE_URL, DEST_NAME])
if laputa_api_commit != '':
    subprocess.call('cd '+DEST_NAME+' && git checkout '+laputa_api_commit, shell=True)


HTTPS_REMOTE_URL = 'https://@github.com/TopPano/verpix-async.git'
DEST_NAME = 'verpix-async'
subprocess.call(["git", "clone", HTTPS_REMOTE_URL, DEST_NAME])
if verpix_async_commit != '':
    subprocess.call('cd '+DEST_NAME+' && git checkout '+verpix_async_commit, shell=True)


HTTPS_REMOTE_URL = 'https://'+user+':'+passwd+'@github.com/TopPano/laputa-db.git'
DEST_NAME = 'laputa-db'
subprocess.call(["git", "clone", HTTPS_REMOTE_URL, DEST_NAME])
if laputa_db_commit != '':
    subprocess.call('cd '+DEST_NAME+' && git checkout '+laputa_db_commit, shell=True)


# read docker-compose.yml
r_stream = file('docker-compose_default.yml', 'r')
docker_compose = yaml.load(r_stream)
if isinstance(laputa_api_port, int):
    docker_compose['services']['verpix-dev-laputa-api']['ports'] = [str(laputa_api_port)+':3000']
if isinstance(laputa_db_webui_port, int):
    docker_compose['services']['verpix-dev-webui-mongodb']['ports'] = [str(laputa_db_webui_port)+':8081']
if isinstance(laputa_db_port, int):
    docker_compose['services']['verpix-dev-mongodb']['ports'] = [str(laputa_db_port)+':27017']

w_stream = file('docker-compose.yml', 'w')
yaml.dump(docker_compose, w_stream)