import subprocess
import threading

from nvos import file, remote
from start import utils, login
import os
import time
import logging
import concurrent.futures
import platform
import shutil

# 导入全局日志记录器
logger = logging.getLogger()


def command_init():
    status = login.check_login_status()
    if not status:
        print("Please login first. you could use login command to login this script")
        return
    workspace_path, success = utils.check_workspace_exist(os.getcwd())

    sub_workspace_path, flag = utils.check_subdirectory_workspace_exist(os.getcwd())
    if flag:
        print(
            f"The subdirectory has already bean initialized, don't repeat execute init command, this subdirectory:{sub_workspace_path}")
        try:
            shutil.rmtree(os.path.join(os.getcwd(), ".ndtc"))
        except OSError as e:
            print(f"Error: {os.path.join(os.getcwd(), '.ndtc')} : {e.strerror}")
        return

    print("please wait one minute.........")
    try:
        file.init_work_space(workspace_path)
    except Exception as e:
        logger.exception("command_init")
        print(f"Error: {e}")


def command_async(model=None):
    workspace_path, success = common_verify()
    if not success:
        return

    async_workspace = os.path.expanduser(os.path.join("~", '.ndtcrc', "aync_workspace"))
    all_workspace_list = []
    if os.path.exists(async_workspace):
        with open(async_workspace, 'r', encoding=utils.file_encoding) as f:
            for item in f:
                all_workspace_list.append(item.strip())

    all_workspace_list = set(all_workspace_list)
    if model is None or model == "start".lower():
        all_workspace_list.add(workspace_path)
    elif model == "stop".lower():
        all_workspace_list.remove(workspace_path)
    utils.check_local_workspace()
    with open(os.path.expanduser(os.path.join("~", '.ndtcrc', "aync_workspace")), "w", encoding=utils.file_encoding) as f:
        for item in list(all_workspace_list):
            f.write(item + '\n')

    if platform.system() == 'Windows':
        return
    # 在运行时执行

    proc1 = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
    proc2 = subprocess.Popen(['grep', 'ndtc'], stdin=proc1.stdout,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc1.stdout.close()  # Allow proc1 to receive a SIGPIPE if proc2 exits.
    out, err = proc2.communicate()
    number = 0
    for line in out.splitlines():
        if 'ndtc' in str(line).lower() and 'python' in str(line).lower() and 'async' in str(line).lower():
            number = number + 1
    if number > 1:
        return
    import daemon
    preserve_fds = [handler.stream for handler in logger.handlers]
    with daemon.DaemonContext(files_preserve=preserve_fds):
        s = threading.Thread(target=execute_pull, args=(async_workspace,))
        s.start()
        s1 = threading.Thread(target=execute_push, args=(async_workspace,))
        s1.start()
        while True:
            time.sleep(1)


def execute_push(async_workspace):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        while True:
            all_push_workspace_list = []
            with open(async_workspace, 'r', encoding=utils.file_encoding) as f:
                for item in f:
                    all_push_workspace_list.append(item.strip())
            for temp in all_push_workspace_list:
                logger.info("command_async push current run workspace is " + temp)
                executor.submit(file.push_data_to_cloud, temp)
            time.sleep(5)

def execute_pull(async_workspace):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        while True:
            all_pull_workspace_list = []
            with open(async_workspace, 'r', encoding=utils.file_encoding) as f:
                for item in f:
                    all_pull_workspace_list.append(item.strip())
            for temp in all_pull_workspace_list:
                logger.info("command_async pull current run workspace is " + temp)
                executor.submit(file.pull_data_from_cloud, temp)
            time.sleep(2)

def command_pull():
    workspace_path, success = common_verify()
    if not success:
        return
    print("please wait one minute.........")
    try:
        file.pull_data_from_cloud(workspace_path)
    except Exception as e:
        logger.exception("command_pull")
        print(f"Error: {e}")


def command_push():
    workspace_path, success = common_verify()
    if not success:
        return
    print("please wait one minute.........")
    try:
        file.push_data_to_cloud(workspace_path)
    except Exception as e:
        logger.exception("command_push")
        print(f"Error: {e}")


def common_verify():
    workspace_path, success = utils.check_workspace_exist(os.getcwd())
    if not success:
        print(
            "Please executor this command that your before executor init command of directory or subdirectory, or you can  executor init this directory")
        return workspace_path, False
    status = login.check_login_status()
    if not status:
        print("Please login first. you could use login command to login this script")
        return workspace_path, False
    return workspace_path, True


def command_env(env=None):
    if env is None:
        result = remote.get_current_env()
        print(f"current env:{result['env']} this cloud linked:{result['tip']}")
        return

    remote.switch_env(env)
    workspace_env = []
    if os.path.exists(os.path.expanduser(os.path.join("~", '.ndtcrc', "workspace_env"))):
        with open(os.path.expanduser(os.path.join("~", '.ndtcrc', "workspace_env")), 'r', encoding=utils.file_encoding) as f:
            for line in f:
                workspace_env.append(line.strip())
        for item in workspace_env:
            try:
                os.remove(os.path.join(item, ".ndtc", 'offset'))
                os.remove(os.path.join(item, ".ndtc", 'project_space'))
                os.remove(os.path.join(item, ".ndtc", 'config'))
            except OSError:
                logger.exception("command_env")


def command_upload():
    file_path = os.path.expanduser(os.path.join('~', 'ndtc.log'))
    remote.upload_logger_file(file_path)