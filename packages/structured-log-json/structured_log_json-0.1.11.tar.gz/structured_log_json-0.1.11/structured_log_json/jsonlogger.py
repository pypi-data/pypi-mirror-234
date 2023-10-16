import logging
import logging.handlers
import logging.config
import os
from structured_log_json.jsonformat import JsonFormatter
from structured_log_json.jsonhandler import JsonRotatingFileHandler
from typing import List

def createFullFilename(path: str, device_name: str, mode_name: str) -> str:
    filename = device_name + '_' + mode_name + '.log'
    fullFilename = os.path.join(path, filename)
    return fullFilename


def setup_logging(path: str, device_name: str, mode_name: str, log_type: str, log_level, skip_attrs:List[str]=[]):
    logger = logging.getLogger(mode_name)
    logger.setLevel(log_level)

    # 1. 构建日志根目录
    if os.path.isdir(path):
        if os.path.exists(path) != True:
            # 创建目录
            os.mkdir(path)
    else:
        raise Exception("Invalid path %s!" % path)
    # 2. 构建完整路径
    fullFilename = createFullFilename(path, device_name, mode_name)
    json_handler = JsonRotatingFileHandler(
        fullFilename, maxBytes=500 * 1024 * 1024, backupCount=64)

    formatter = JsonFormatter(logtype=log_type, skip_fields=skip_attrs)
    json_handler.setFormatter(formatter)
    logger.addHandler(json_handler)

    # 设置log 配置文件
    # logging.config.fileConfig('logging.conf')
    # logger_cfg = logging.getLogger(mode_name)
    return logger
