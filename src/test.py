import requests
import csv
import json

from conf import config
user = config["CURRENT_USER"]
pwd = config["CURRENT_PWD"]

url = "http://localhost:5000/api/v1/"

url_login = url + "login"
headers_login = {'Content-Type': 'application/json'}
r_login = requests.post(url_login,  json = {"user":user,"password":pwd}, headers=headers_login)
json_login = json.loads(r_login.text)
print(json_login)

url_run = url + "run"
headers_run = {'x-access-token':json_login["token"]}
fileobj = open('D:\\CIAT\\Code\\USAID\\aclimate_oryza\\data\\inputs.zip', 'rb')
r_run = requests.post(url_run,  files={"inputs": ("inputs", fileobj)}, headers=headers_run)
print(r_run.content)
for l in r_run.iter_lines():
    print(l)


# Cleaning env folder
# shutil.rmtree(env)