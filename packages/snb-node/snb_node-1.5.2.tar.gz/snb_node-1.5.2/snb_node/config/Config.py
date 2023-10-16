import configparser
import platform
import os
import base64

if platform.system().lower() == 'windows':
    path = r'd:/smartnotebook/snb_node/snb_node/config/config.ini'
else:
    path = r'/home/.config/config.ini'

config = configparser.ConfigParser()
config.read(path)

#"http://172.30.81.116:8888"
SNB_SERVER_URL = config.get('snb_server_url', 'url')

workspace_uid = config.get('workspace', 'workspace_uid')
envir_uid = config.get('workspace', 'envir_uid')

cull_idle_timeout_int = config.getint('kernel', 'cull_idle_timeout')

pem_base64= config.get('workspace', 'private_pem')
pem_base64_bytes = base64.standard_b64decode(pem_base64.encode('utf-8'))
pem = pem_base64_bytes.decode('utf-8')




BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))