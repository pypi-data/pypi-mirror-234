import os
import logging
from logging.handlers import RotatingFileHandler

log_file = os.path.expanduser(os.path.join('~', 'ndtc.log'))
log_size_limit = 1024 * 1024 * 1024
log_backup_count = 5

# 配置日志格式化信息
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 创建 RotatingFileHandler 处理器
log_handler = RotatingFileHandler(
    log_file,
    maxBytes=log_size_limit,
    backupCount=log_backup_count
)

log_handler.setFormatter(formatter)