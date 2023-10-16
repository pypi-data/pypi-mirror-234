from skyeye import remote,loghandler
from start import utils,log
import os
import json
import daemon
import subprocess
import logging
import time


# 导入全局日志记录器
logger = logging.getLogger()
# 移除控制台处理器
for h in logger.handlers:
    if isinstance(h, logging.StreamHandler):
        logger.removeHandler(h)
logger.addHandler(log.log_handler)


def command_env(env=None):
    if env is None:
        result = remote.get_current_env()
        print(f"current env:{result['env']} this cloud linked:{result['tip']}")
        return
    remote.switch_env(env)


def command_log(path=None):
    if path is not None:
        loghandler.filter_effective_log(path,{},False)
        return

    proc1 = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
    proc2 = subprocess.Popen(['grep', 'ndtc'], stdin=proc1.stdout,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc1.stdout.close()  # Allow proc1 to receive a SIGPIPE if proc2 exits.
    out, err = proc2.communicate()
    number = 0
    for line in out.splitlines():
        if 'ndtc' in str(line).lower() and 'python' in str(line).lower() and 'upload' in str(line).lower():
            number = number + 1
    if number > 1:
        return
    preserve_fds = [handler.stream for handler in logger.handlers]
    with daemon.DaemonContext(files_preserve=preserve_fds):
        while True:
            try:
                already_upload_file = {}
                if os.path.exists(os.path.expanduser(os.path.join("~", '.ndtcrc', "already_upload_file"))):
                    with open(os.path.expanduser(os.path.join("~", '.ndtcrc', "already_upload_file")),'r') as f:
                        already_upload_file = json.loads(f.read())
                total_path = []
                config = utils.get_config()
                total_path.extend(config["log_path"])
                for temp in total_path:
                    loghandler.filter_effective_log(temp,already_upload_file,True)
                time.sleep(2)
            except Exception:
                logger.exception("handle exception")



