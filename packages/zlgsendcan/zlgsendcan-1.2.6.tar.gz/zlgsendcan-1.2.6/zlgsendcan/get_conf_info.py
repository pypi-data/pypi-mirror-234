import os
import sys

from zlgsendcan import frozen_dir
from zlgsendcan import yaml_util

SETUP_DIR = frozen_dir.app_path()
sys.path.append(SETUP_DIR)
# 获取当前项目的绝对路径
# current = os.path.abspath(__file__)
# base_dir = os.path.dirname(os.path.dirname(current))
# log路径
# _log_path = base_dir + os.sep + "logs"

_log_path = SETUP_DIR + os.sep + "logs"

# _config_path = base_dir + os.sep + "config"
_config_path = SETUP_DIR
# _data_path = base_dir + os.sep + "data"
_data_path = SETUP_DIR + os.sep + "data"
_crc_path = SETUP_DIR + os.sep + "CRC_Check"


current = os.path.abspath(__file__)
base_dir = os.path.dirname(os.path.dirname(current))
# allure路径
_allure_path = base_dir + os.sep + 'software/allure-commandline-2.22.0/allure-2.22.0/bin'
#启动celery路径
celery_path = base_dir + os.sep + 'celery_task'
def get_celery_path():
    return celery_path
def get_allure_path():
    return _allure_path
def get_log_path():
    return _log_path


def get_json_path(filename):
    return _data_path + os.sep + filename


def get_crc_path(filename):
    return _crc_path + os.sep + filename


def get_config_file(filename):
    return _config_path + os.sep + filename


def get_data_file(filename):
    return _data_path + os.sep + filename


def get_icon_path(imagename):
    return _data_path + os.sep + 'image' + os.sep + imagename


def get_trace_path(database_name):
    return _data_path + os.sep + 'database' + os.sep + database_name


# def get_zlg_dll_path(dllname):
#     return base_dir + os.sep + dllname


# 获取对应的配置信息和文件信息
class GetBaseInfo:
    def __init__(self):

        self.yamlobj = yaml_util.YamlRead(get_config_file('base_conf.yml'))
        self.config = self.yamlobj.read_data()

    def get_base_config(self):
        return self.config

    def update_config(self, data):
        self.yamlobj.updata_yaml(data)

    def get_dbc_path(self, mode='r', text=None):
        try:
            with open(get_config_file('dbcpath.json'), mode, encoding='utf-8') as f:
                if mode == 'r':
                    a = f.read()
                    return a
                elif mode == 'w':
                    f.write(text)
        except Exception as e:
            return

    def get_config_log_level(self):
        return self.config['log']['log_level']

    def get_config_extenxion(self):
        return self.config['log']['log_extension']
    #
    # def get_config_env(self):
    #     return self.config['QA']['env']
    #
    # def get_file_path(self, filename):
    #     return _data_path + os.sep + filename
    #
    # def get_token_data(self):
    #     return self.config['QA']['token']
    #
    # def get_login_info(self):
    #     return self.config['QA']['login']


if __name__ == '__main__':
    # a = GetBaseInfo()
    # old_data = a.get_base_config()
    # udata = old_data['can初始化配置']['协议']
    # udata[0],udata[1] = udata[1],udata[0]
    # a.update_config(old_data)
    print(get_config_file('base_conf.yml'))
