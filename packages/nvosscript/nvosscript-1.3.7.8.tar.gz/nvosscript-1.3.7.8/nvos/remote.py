import time
import traceback

import boto3
import os
import requests
import hashlib
import json
import re
import concurrent.futures
import multiprocessing
from tqdm import tqdm
from start import utils, login
import logging

# 导入全局日志记录器
logger = logging.getLogger(__name__)
daemon_network = "https://nvos-toolchain.nioint.com"

daemon_network_mapping = {
    "prod": "https://nvos-toolchain.nioint.com",
    "stg": "https://nvos-toolchain-stg.nioint.com",
    "dev": "https://nvos-toolchain-dev.nioint.com"
}

daemon_network_front_mapping = {
    "prod": "https://ndtc.nioint.com/#/nvosTool/spaceList",
    "stg": "https://ndtc-stg.nioint.com/#/nvosTool/spaceList",
    "dev": " https://soa-tools-dev.nioint.com/#/nvosTool/spaceList"
}
global_var = 0


def upload_logger_file(file_path):
    get_current_env()
    s3_secret = get_s3_secret()
    bucket_name = s3_secret["bucket"]
    aws_ak = s3_secret["ak"]
    aws_sk = s3_secret["sk"]
    aws_region = s3_secret["regionId"]
    s3 = boto3.resource('s3', region_name=aws_region, aws_access_key_id=aws_ak,
                        aws_secret_access_key=aws_sk)
    bucket = s3.Bucket(bucket_name)
    file_name = "/log/" + login.get_user_id() + "/ndtc.log"
    bucket.upload_file(file_path, file_name)
    print("success upload file name " + file_name)

def upload_linux_client_script():
    file_name = "/nvos-script/linux/nvosscript.zip"
    file_path = os.path.join(os.getcwd(), 'nvosscript.zip');
    upload_client_script(file_name, file_path)


def upload_win_client_script():
    file_name = "/nvos-script/nvosscript.zip"
    file_path = os.path.join(os.getcwd(), 'nvosscript.zip')
    upload_client_script(file_name, file_path)


def upload_client_script(file_name, file_path):
    get_current_env()
    s3_secret = get_s3_secret()
    bucket_name = s3_secret["bucket"]
    aws_ak = s3_secret["ak"]
    aws_sk = s3_secret["sk"]
    aws_region = s3_secret["regionId"]
    s3 = boto3.resource('s3', region_name=aws_region, aws_access_key_id=aws_ak,
                        aws_secret_access_key=aws_sk)
    bucket = s3.Bucket(bucket_name)
    bucket.upload_file(file_path, file_name)


def file_upload_notify(workspace_path, project_list):
    get_current_env()
    url = "%s%s" % (daemon_network, "/workspace/analyse")
    post_param = {"userId": login.get_user_id(workspace_path), "fileDirectory": workspace_path, "projectSpaceList": project_list}
    data = post_data(url, post_param)
    return data

def upload_file(workspace_path, file_path_list, project_space_list):
    upload_list = []
    filter_upload_re = filter_upload_dir()
    for project_space in project_space_list:
        for file_path in file_path_list:
            flag = False
            for temp in filter_upload_re:
                matchObj = re.match(temp, file_path["file_path"], re.M | re.I)
                if matchObj:
                    flag = True
                    break
            if not flag:
                f = file_path["file_path"]
                logger.info(f"file :{f} ")
                continue

            if project_space["project_space"] in file_path["file_path"]:
                local_file_path = file_path["file_path"]
                temp_file = {"local_file_path": local_file_path, "project_space": project_space["project_space"], "project_space_git_branch": project_space["git_branch"]}
                upload_list.append(temp_file)
    upload_process(workspace_path,upload_list)

    file_upload_notify(workspace_path, project_space_list)

def upload_process(workspace_path,upload_list):
    global global_var
    multiprocessing.set_start_method('spawn', True)
    cores = multiprocessing.cpu_count()
    with concurrent.futures.ThreadPoolExecutor(max_workers=cores) as executor, tqdm(desc="uploading", total=len(upload_list)) as progress:
        for index, file in enumerate(upload_list):
            executor.submit(uploading_file, workspace_path, file)
        time_count = 0
        addition = 0
        while True:
            time.sleep(1)
            time_count += 1
            progress.update(global_var - addition)
            addition = global_var
            if (global_var == len(upload_list) or global_var >= len(upload_list) - 20):
                break


def uploading_file(workspace_path, file):

    global global_var

    get_current_env()
    url = "%s%s" % (daemon_network, "/file/upload")

    local_file_path = file["local_file_path"]

    try:
        with open(local_file_path, 'r', encoding=utils.file_encoding) as f:
            contents = f.read()
        post_param = {"projectSpaceGitBranch": file["project_space_git_branch"], "projectSpaceFileDirectory": file["project_space"], "userId": login.get_user_id(workspace_path), "filePath": local_file_path, "fileContent": contents}
        post_data(url, post_param)
        logger.info(f"upload file local full path:{local_file_path}")
        global_var += 1
    except Exception:
        traceback.print_exc()
        logger.exception('uploading_file error: %s', local_file_path)



def download_file(project_space):
    get_current_env()
    url = "%s%s" % (daemon_network, "/file/download")
    for file in project_space["changedFileList"]:
        file_id = file["fileId"]
        file_full_path = file["fileFullPath"]
        try:
            post_param = {"id": file_id}
            data = post_data(url, post_param)
            file_content = data["fileContent"]
            with open(file_full_path, "w", encoding=utils.file_encoding) as f:
                f.write(file_content)
        except Exception:
            logger.exception(f"this file sync fail  id:{file_id} ")
        else:
            logger.info(f"this file sync success  id:{file_id} ")

def save_workspace(workspace_path, project_list):
    get_current_env()
    url = "%s%s" % (daemon_network, "/workspace/add")
    post_param = {"userId": login.get_user_id(workspace_path), "fileDirectory": workspace_path, "projectSpaceList": project_list}
    return post_data(url, post_param)


def pull_workspace(workspace, project_list):
    get_current_env()
    url = "%s%s" % (daemon_network, "/workspace/getChangedFiles")
    post_param = {"userId": login.get_user_id(workspace), "fileDirectory": workspace, "projectSpaceList": project_list}
    return post_data(url, post_param)


def post_data(url, params):
    headers = {"content-type": "application/json"}
    logger.info(f'request url:{url} params:{params}')
    response = requests.post(url, headers=headers, data=json.dumps(params))
    logger.info(f"response status_code: {response.status_code} text: {response.text} \n content:{response.content}")
    if response.status_code == 200:
        result = json.loads(response.text)
        if result["success"]:
            return result["data"]
        else:
            message = result["message"]
            raise Exception('please check error message is :{}'.format(message))
    return {}


def md5(git_branch, project_space):
    string = "%s%s" % (git_branch, project_space)
    hash_object = hashlib.md5(string.encode())
    md5_hash = hash_object.hexdigest()
    return md5_hash


def filter_upload_dir():
    get_current_env()
    url = "%s%s" % (daemon_network, "/workspace/getFilePathRegular")
    return post_data(url, {})

def get_s3_secret():
    get_current_env()
    url = "%s%s" % (daemon_network, "/file/config")
    headers = {"content-type": "application/json"}
    logger.info(f'request url:{url}')
    response = requests.post(url, headers=headers, data=json.dumps({}))
    if response.status_code == 200:
        response_data = json.loads(response.text)["data"]
        return response_data
    return {}


def switch_env(env):
    val = daemon_network_mapping.get(env)
    if len(val) == 0:
        return
    tip = daemon_network_front_mapping.get(env)
    result = {"cloud":val,"tip":tip,"env":env}
    utils.check_local_workspace()
    with open(os.path.expanduser(os.path.join('~','.ndtcrc' ,'nvos_env')), 'w', encoding=utils.file_encoding) as f:
        f.writelines(json.dumps(result))
    print(f"this script current env:{env} and cloud linked:{tip}")


def get_current_env():
    global daemon_network
    result = {}
    if os.path.exists(os.path.expanduser(os.path.join('~', '.ndtcrc', 'nvos_env'))):
        with open(os.path.expanduser(os.path.join('~', '.ndtcrc', 'nvos_env')), 'r', encoding=utils.file_encoding)as f:
            result = json.loads(f.readline().strip())
            daemon_network = result["cloud"]
            tip = result["tip"]
            env = result["env"]
            logger.info(f"current env:{env} this cloud linked:{tip} daemon_network:{daemon_network}")
    if result == {}:
        result["cloud"] = daemon_network_mapping.get('prod')
        result['env'] = 'prod'
        result['tip'] = daemon_network_front_mapping.get('prod')
    return result
