from app import root_dir, ninja_token
from datetime import datetime
import json, requests, os

ninja_host = os.environ.get("NINJA_HOST",os.getenv('NINJA_HOST'))
ninja_port = os.environ.get("NINJA_PORT",os.getenv('NINJA_PORT'))
ninja_version = os.environ.get("NINJA_API_VERSION",os.getenv('NINJA_API_VERSION'))
fix_ninja = "http://"+ninja_host+"/api/"+ninja_version+"/"
ninja_headers = {
        "X-Ninja-Token": ninja_token
}
def timeset():
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

def mkdir(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)

def read_file(file):
    with open(file, 'r') as outfile:
        return outfile.read()

def list_dir(dirname):
    listdir = list()
    for root, dirs, files in os.walk(dirname):
        for file in files:
            listdir.append(os.path.join(root, file))
    return listdir

def send_http(url, data, header=None):
    send = requests.post(url, data=data, headers=header)
    respons = send.json()
    return respons

def get_http(url, param=None, header=None):
    json_data = None
    if param:
        json_data = param
    get_func = requests.get(url, params=json_data, headers=header)
    data = get_func.json()
    return data

def get_ninja(api, params=None):
    uri = fix_ninja+api
    a = get_http(url=uri,param=params, header=ninja_headers)
    return a

def post_ninja(api, data):
    uri = fix_ninja+api
    a = send_http(url=uri, data=data, header=ninja_headers)
    return a
