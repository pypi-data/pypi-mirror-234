import os
import re
import logging
import gzip
import json
from skyeye import remote
from start import log


# 导入全局日志记录器
logger = logging.getLogger(__name__)
# 移除控制台处理器
for h in logger.handlers:
    if isinstance(h, logging.StreamHandler):
        logger.removeHandler(h)
logger.addHandler(log.log_handler)

def filter_effective_log(path, already_upload_file, auto):
    if path is None:
        print("please upload correct path")
        return
    logger.info(f" start filter_effective_log {path}")
    logger_list = []
    if not os.path.exists(path):
        print(f"{path} not exists ,Please reselect the path")
        return
    if os.path.isdir(path):
        dp_file_folder(path, logger_list, already_upload_file)
    else:
        file_name, data_list = read_log_data(path, already_upload_file)
        if len(data_list) > 0:
            logger_list.extend({"fileName": file_name, "dataList": data_list})

    remote.upload_file_process(logger_list)
    if not auto:
        return
    with open(os.path.expanduser(os.path.join("~", '.ndtcrc', "already_upload_file")), 'w') as f:
        f.write(json.dumps(already_upload_file))


def dp_file_folder(path, logger_list, already_upload_file):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            dp_file_folder(file_path, logger_list, already_upload_file)
        else:
            file_name, data_list = read_log_data(file_path, already_upload_file)
            if len(data_list) > 0:
                logger_list.append({"fileName": file_name, "dataList": data_list})


def read_log_data(path, already_upload_file):
    logger_list = []
    if not os.path.isfile(path):
        return "", logger_list
    file_name = os.path.basename(path)
    if file_name == ".DS_Store":
        return file_name,logger_list
    file_size = os.path.getsize(path)
    filter_key = "%s_%d" % (file_name, file_size)
    logger.info(f"read_log_data path {path} and file_name {file_name} file_size {file_size}")

    if filter_key in already_upload_file.keys():
        logger.info("read_log_data current file_name already read, dont repeat read file", file_name)
        return file_name, logger_list

    if file_name.endswith(".gz"):
        with gzip.open(path, 'rt') as file:
            content = file.read()
            for line in content.splitlines():
                matchObj = re.search("\d\|\d+\|\d+\|.*", line, re.M | re.I)
                if matchObj:
                    logger_list.append(line)
    else:
        with open(path, 'r') as f:
            for line in f:
                matchObj = re.search("\d\|\d+\|\d+\|.*", line, re.M | re.I)
                if matchObj:
                    logger_list.append(line)

    already_upload_file[filter_key] = file_name
    return file_name, logger_list


