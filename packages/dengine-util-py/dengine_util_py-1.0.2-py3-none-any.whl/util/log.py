import logging
import re
import os
from logging.handlers import TimedRotatingFileHandler

from util.path import get_project_dir

# 设置日志文件的最大大小（可选）
max_file = 1024 * 1024 * 1024 * 1
# 最大备份小时
backup_count = 24 * 30

hander = TimedRotatingFileHandler(filename=get_project_dir()+"/log/all.log", when="H", interval=1,
                                  backupCount=backup_count)
hander.suffix = '%Y%m%d%H'
ext_match = r"^\d{10}$"
hander.extMatch = re.compile(ext_match, re.ASCII)
_project_name = '_' + os.environ.get('PROJECT_NAME')

# 配置日志

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s][%(asctime)s.%(msecs)d][%(filename)s:%(lineno)d] %(_project_name)s||%(message)s",
    handlers=[
        hander
        # logging.StreamHandler() 输出日志到标准输出
    ],
    datefmt='%Y-%m-%dT%H:%M:%S',
)

# 创建日志记录器
logger = logging.getLogger(__name__)
