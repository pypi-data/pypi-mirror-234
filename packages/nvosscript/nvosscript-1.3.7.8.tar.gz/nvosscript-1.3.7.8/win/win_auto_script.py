from nvos import file
import logging
import json
import os
import concurrent.futures
import time

logging.basicConfig(filename=os.path.expanduser(os.path.join("~", "ndtc_auto.log")), level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def execute_async(workspace_path):
    file.push_data_to_cloud(workspace_path)
    file.pull_data_from_cloud(workspace_path)


if __name__ == '__main__':
    logger.info("service start success......")
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        while True:
            logger.info("start execute next task........")
            try:
                if os.path.exists(os.path.expanduser(os.path.join("~", '.ndtcrc', "workspace"))):
                    with open(os.path.expanduser(os.path.join("~", '.ndtcrc', "workspace")), "r") as f:
                        all_workspace_path = json.loads(f.readline().strip())
                    for temp in all_workspace_path.keys():
                        logger.info("command_async current run workspace is " + temp)
                        executor.submit(execute_async, temp)
            except Exception as e:
                logger.exception("An exception occurred")
            time.sleep(10)
