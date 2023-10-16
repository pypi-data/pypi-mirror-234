import ldap3
import os
import json
from start import utils


def login_user_check(user_name, password):
    try:
        server = ldap3.Server('ldap.fareast.nevint.com')
        conn = ldap3.Connection(server, user_name, password, client_strategy=ldap3.SAFE_SYNC, auto_bind=True)
        status, result, response, _ = conn.search('o=test', '(objectclass=*)')
        workspace_path = os.path.join(os.getcwd(), ".ndtc")
        if not os.path.exists(workspace_path):
            os.mkdir(workspace_path)
        path = os.path.join(os.path.join(workspace_path, "login"))
        with open(path, 'w') as f:
            user_data = {"user_name": user_name.split("@")[0], "login": "success"}
            f.writelines(json.dumps(user_data))
    except Exception:
        return "login fail"
    else:
        return "login success"


def check_login_status():
    workspace_path, success = utils.check_workspace_exist(os.getcwd())
    if not success:
        return False

    path = os.path.join(workspace_path, '.ndtc', "login")
    login_exist = os.path.exists(path)
    if not login_exist:
        return False
    with open(path, 'r') as file:
        content = file.readline()
        login_data = json.loads(content)
        login_success = login_data["login"] == "success"
    return login_success


def get_user_id(workspace_value = None):
    workspace_path = ""
    if workspace_value is None:
        workspace_path, success = utils.check_workspace_exist(os.getcwd())
        if not success:
            return False
    else:
        workspace_path = workspace_value
    path = os.path.join(workspace_path, '.ndtc', "login")
    with open(path, 'r') as file:
        content = file.readline()
        login_data = json.loads(content)
        user_id = login_data["user_name"]
    return user_id
