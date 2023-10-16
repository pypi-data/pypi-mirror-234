import os
import subprocess
import logging
import json
from nvos import remote
from start import utils

logger = logging.getLogger(__name__)


# 初始化工作环境
def init_work_space(workspace_path):
    if len(workspace_path) == 0:
        return False
    init_path = os.path.join(workspace_path, ".ndtc", "init")
    with open(init_path, 'w', encoding=utils.file_encoding) as f:
        f.write(workspace_path)

    nvos_dir = os.path.join(workspace_path, ".ndtc")
    project_space_list, success = sync_project_data(workspace_path)
    logger.info(f"sync_project_data end projectSpaceList: {project_space_list} success:{success} ")
    file_list = []
    find_json_config(workspace_path, file_list, project_space_list)
    # 将来可以优化上传文件信息，针对于已经上传过的就不在上传
    with open(os.path.join(nvos_dir, "config"), 'w', encoding=utils.file_encoding) as file:
        for item in file_list:
            file.write(json.dumps(item) + "\n")

    remote.upload_file(workspace_path, file_list, project_space_list)

    workspace_env = []
    if os.path.exists(os.path.expanduser(os.path.join("~", '.ndtcrc', "workspace_env"))):
        with open(os.path.expanduser(os.path.join("~", '.ndtcrc', "workspace_env")), 'r', encoding=utils.file_encoding) as f:
            for line in f:
                workspace_env.append(line.strip())
    workspace_env.append(workspace_path)
    workspace_env = list(set(workspace_env))
    utils.check_local_workspace()
    with open(os.path.expanduser(os.path.join("~", '.ndtcrc', "workspace_env")), 'w', encoding=utils.file_encoding) as f:
        for item in workspace_env:
            f.write(item + "\n")

    return True


def pull_data_from_cloud(workspace_path):
    sync_project_data(workspace_path)

    overwrite_file(workspace_path)


def push_data_to_cloud(workspace_path):
    logger.info(f"push_data_to_cloud start execute workspace_path: {workspace_path}")
    project_space_list, success = sync_project_data(workspace_path)
    nvos_path = os.path.join(workspace_path, ".ndtc")

    origin_file_list = []
    with open(os.path.join(nvos_path, "config"), 'r', encoding=utils.file_encoding) as f:
        for line in f:
            origin_file_list.append(json.loads(line))
    origin_file_map = {}
    for temp in origin_file_list:
        origin_file_map.update({"%s_%s" % (temp["file_path"], temp["git_branch"]): temp["file_size"]})

    file_list = []
    find_json_config(workspace_path, file_list, project_space_list)
    add_file_list = []
    for temp in file_list:
        if "%s_%s" % (temp["file_path"], temp["git_branch"]) not in origin_file_map:
            add_file_list.append(temp)
    logger.info(f"push add_file_list: {add_file_list}")
    if len(add_file_list) > 0:
        remote.upload_file(workspace_path, add_file_list, project_space_list)
        logger.info(f"start save all file config ")
        origin_file_list.extend(add_file_list)
        with open(os.path.join(nvos_path, "config"), 'w', encoding=utils.file_encoding) as f:
            for item in origin_file_list:
                f.write(json.dumps(item) + "\n")


# 同步项目数据到远程
def sync_project_data(workspace_path):
    logger.info(f"start execute sync_project_data {workspace_path}")
    project_space_path = os.path.join(workspace_path, ".ndtc", "project_space")
    origin_project_space_list = []
    if os.path.exists(project_space_path):
        with open(project_space_path, 'r', encoding=utils.file_encoding) as f:
            for line in f:
                origin_project_space_list.append(json.loads(line.strip()))
    project_space_list = []
    find_project_space(workspace_path, project_space_list)
    project_space_list = filter_project_space(workspace_path, project_space_list)
    sync_project_offset(workspace_path, project_space_list)
    if len(project_space_list) != len(origin_project_space_list):
        logger.info(
            f"projectSpace changed projectSpaceList: {project_space_list}          originProjectSpaceList:{origin_project_space_list}")
        remote.save_workspace(workspace_path, project_space_list)
        with open(project_space_path, 'w', encoding=utils.file_encoding) as f:
            for item in project_space_list:
                f.write(json.dumps(item) + "\n")
        return project_space_list, True
    logger.info("start compare projectSpace git branch  changed")
    upload_data = False
    for item in project_space_list:
        flag = False
        for origin_item in origin_project_space_list:
            if item["project_space"] == origin_item["project_space"] and item["git_branch"] == origin_item[
                "git_branch"]:
                flag = True
        if not flag:
            remote.save_workspace(workspace_path, project_space_list)
            upload_data = True
            break

    with open(project_space_path, 'w', encoding=utils.file_encoding) as f:
        for item in project_space_list:
            f.write(json.dumps(item) + "\n")
    logger.info(f"end method sync_project_data project_space_list: {project_space_list}")
    return project_space_list, upload_data


def sync_project_offset(workspace_path, project_space_list):
    offset_path = os.path.join(workspace_path, ".ndtc", "offset")
    if not os.path.exists(offset_path):
        for project_space in project_space_list:
            project_space["offset"] = 1
        with open(offset_path, 'w', encoding=utils.file_encoding) as f:
            f.writelines(json.dumps(project_space_list))
    else:
        with open(offset_path, 'r', encoding=utils.file_encoding) as f:
            offset_json_list = json.loads(f.readline())
        offer_map = {}
        filter_list = []
        for offset in offset_json_list:
            offer_map["%s_%s" % (offset["project_space"], offset["git_branch"])] = offset["offset"]
        for project_space in project_space_list:
            if not "%s_%s" % (project_space["project_space"], project_space["git_branch"]) in offer_map:
                project_space["offset"] = 1
                filter_list.append(project_space)
        offset_json_list.extend(filter_list)
        with open(offset_path, 'w', encoding=utils.file_encoding) as f:
            f.writelines(json.dumps(offset_json_list))


def filter_project_space(workspace_path, project_space_list):
    exit_git_data = []
    not_exit_git_data = []
    for project_space in project_space_list:
        if project_space["git_branch"] == "nvos_default":
            not_exit_git_data.append(project_space)
        else:
            exit_git_data.append(project_space)
    if len(not_exit_git_data) == 0:
        project_space_list.clear()
        for project_space in exit_git_data:
            # if project_space["git_branch"] != "(no branch)":
            project_space_list.append(project_space)
        return filter_ecus_dir(project_space_list)
    if len(exit_git_data) == 0:
        result_list = []
        for file_path in os.listdir(workspace_path):
            if file_path == ".idea" or file_path == ".repo" or file_path == ".ndtc" or file_path == ".DS_Store":
                continue
            if os.path.isdir(os.path.join(workspace_path, file_path)):
                temp = {"project_space": os.path.join(workspace_path, file_path),
                        "fileDirectory": os.path.join(workspace_path, file_path),
                        "git_branch": "nvos_default", "gitBranch": "nvos_default"}
                result_list.append(temp)
        return filter_ecus_dir(result_list)

    filter_exit_data = []
    for project_space in not_exit_git_data:
        max_prefix = ""
        max_public_str = ""

        for item in exit_git_data:
            prefix = item["project_space"][:item["project_space"].rfind(os.path.sep)]
            while True:
                if project_space["project_space"].startswith(prefix) and len(prefix) > len(max_prefix):
                    max_prefix = prefix
                    max_public_str = project_space["project_space"][len(prefix) + 1:]
                    max_public_str = max_public_str[:max_public_str.find(os.path.sep)]
                    max_public_str = os.path.join(max_prefix, max_public_str)
                if os.path.basename(prefix) == os.path.basename(workspace_path):
                    break
                prefix = prefix[:prefix.rfind(os.path.sep)]

        temp = {"project_space": max_public_str, "fileDirectory": max_public_str,
                "git_branch": "nvos_default", "gitBranch": "nvos_default"}
        filter_exit_data.append(temp)

    filter_duplicate = []
    for item in filter_exit_data:
        flag = True
        for temp in filter_duplicate:
            if temp["project_space"] == item["project_space"]:
                flag = False
                break
        if flag:
            filter_duplicate.append(item)
    project_space_list.clear()
    for project_space in exit_git_data:
        # if project_space["git_branch"] != "(no branch)":
        project_space_list.append(project_space)
    project_space_list.extend(filter_duplicate)

    # 再过滤一次ecus的目录
    return filter_ecus_dir(project_space_list)

def filter_ecus_dir(project_space_list):
    final_project_space_list = []
    for item in project_space_list:
        # 取当前目录
        now_dir = item["fileDirectory"]
        # 发现是xxxx/xxx/ecus
        if os.path.basename(now_dir) == "ecus":
            git_branch = get_current_git_branch(now_dir)
            for name in os.listdir(now_dir):
                if name == ".idea" or name == ".repo" or name == ".ndtc" or name == ".DS_Store" or name == ".git" or name == ".gitignore":
                    continue
                sub_dir = os.path.join(now_dir, name)
                if os.path.isdir(sub_dir):
                    if len(git_branch) == 0:
                        git_branch = get_current_git_branch(sub_dir)
                        if len(git_branch) == 0:
                            git_branch = "nvos_default"
                    temp = {"project_space": sub_dir, "fileDirectory": sub_dir,
                            "git_branch": git_branch, "gitBranch": git_branch}
                    final_project_space_list.append(temp)
        else:
            final_project_space_list.append(item)
    return final_project_space_list

def get_current_git_branch(workspace_path):
    git_path = os.path.join(workspace_path, ".git")
    if not os.path.exists(git_path):
        return ""

    try:
        completed_process = subprocess.run(['git', 'branch'], stdout=subprocess.PIPE)
        git_branch_val = completed_process.stdout.decode().splitlines()
        if len(git_branch_val) == 0:
            return "(no branch)"
        git_branch_data = ""
        for line in git_branch_val:
            if "*" in line:
                git_branch_data = line.split("*")[1].strip()
        return git_branch_data
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip()
        logger.exception(f"Git命令执行出错：{error_message}")
        return "(no branch)"
    except Exception:
        logger.exception(f"Error: {os.path.join(os.getcwd(), '.ndtc')}")
        return "(no branch)"


# 获取项目的空间
def find_project_space(workspace_path, result_list):
    for file_path in os.listdir(workspace_path):
        if file_path == ".idea" or file_path == ".repo" or file_path == ".ndtc" or file_path == ".DS_Store":
            continue
        if not os.path.isdir(os.path.join(workspace_path, file_path)):
            if file_path.endswith(".json"):
                result_list.append({"project_space": os.path.join(workspace_path, file_path),
                                    "fileDirectory": os.path.join(workspace_path, file_path),
                                    "git_branch": "nvos_default", "gitBranch": "nvos_default"})
            continue
        os.chdir(os.path.join(workspace_path, file_path))
        git_branch = get_current_git_branch(os.path.join(workspace_path, file_path))
        if len(git_branch) == 0:
            find_project_space(os.path.join(workspace_path, file_path), result_list)
        else:
            result = {"project_space": os.path.join(workspace_path, file_path), "git_branch": git_branch,
                      "fileDirectory": os.path.join(workspace_path, file_path), "gitBranch": git_branch}
            os.chdir("..")
            result_list.append(result)


def overwrite_file(workspace_path):
    logger.info(f"overwrite_file start overwrite file {workspace_path}")
    offset_file_path = os.path.join(workspace_path, ".ndtc", "offset")

    with open(offset_file_path, 'r', encoding=utils.file_encoding) as f:
        offset_json_list = json.loads(f.readline())
    offer_map = {}
    for offset in offset_json_list:
        offer_map["%s_%s" % (offset["project_space"], offset["git_branch"])] = offset["offset"]

    project_space_path = os.path.join(workspace_path, ".ndtc", "project_space")
    project_space_list = []
    with open(project_space_path, 'r', encoding=utils.file_encoding) as f:
        for line in f:
            project_space_list.append(json.loads(line))
    logger.info(f"overwrite_file project_space_list: {project_space_list} offer_map:{offer_map}")
    for project_space in project_space_list:
        project_space["syncTag"] = offer_map.get(
            "%s_%s" % (project_space["project_space"], project_space["git_branch"]))

    response_list = remote.pull_workspace(workspace_path, project_space_list)
    for project_space in response_list["projectSpaceList"]:
        offer_map["%s_%s" % (project_space["fileDirectory"], project_space["gitBranch"])] = project_space["syncTag"]
        remote.download_file(project_space)
    for offset in offset_json_list:
        offset["offset"] = offer_map.get("%s_%s" % (offset["project_space"], offset["git_branch"]))
    with open(offset_file_path, 'w', encoding=utils.file_encoding) as f:
        f.writelines(json.dumps(offset_json_list))


def find_json_config(file_path, config_list, project_space_list):
    for file_name in os.listdir(file_path):
        if file_name == ".idea" or file_name == ".git" or file_name == ".repo" or file_name == ".ndtc" or file_name == ".DS_Store":
            continue
        if os.path.isdir(os.path.join(file_path, file_name)):
            find_json_config(os.path.join(file_path, file_name), config_list, project_space_list)
        elif file_name.endswith(".json") or file_name == "module-cfg.cmake":
            file_full_path = os.path.join(file_path, file_name)
            for project_space in project_space_list:
                if file_full_path.startswith(project_space["project_space"]):
                    file_data = {"file_path": os.path.join(file_path, file_name),
                                 "file_size": os.path.getsize(os.path.join(file_path, file_name)),
                                 "git_branch": project_space["git_branch"]}
                    config_list.append(file_data)
                    break


def create_work_space(user_name, work_space):
    return "%s_%s" % (user_name, work_space)
