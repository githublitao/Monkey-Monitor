#   封装配置文件地址
import os

from common.File import OperateFile

father_path = os.getcwd()
# father_path = os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")


def report_path():
    """
    测试报告
    :return:
    """
    path = father_path+'\\'
    return path


def log_path():
    """
    日志位置
    :return:
    """
    path = father_path + '\\log'
    OperateFile(path).mk_dir()
    return path


def info_path():
    """
    info路径
    :return:
    """
    path = father_path + '\\info'
    OperateFile(path).mk_dir()
    return path


def scan_files(select_path=father_path, prefix=None, postfix=None):
    """
    查询目录下后缀或前缀的文件
    :param select_path: 待搜索的目录
    :param prefix:  匹配前缀文件名称，例如： prefix=test，匹配所有test开头的文件
    :param postfix: 匹配后缀名文件，例如： postfix=.py ，匹配目录下所有.py文件
    :return:
    """
    #   返回文件路径
    files_list = []
    for root, sub_dirs, files in os.walk(select_path):
        for special_file in files:
            if postfix:
                if special_file.endswith(postfix):
                    files_list.append(os.path.join(root, special_file))
            elif prefix:
                if special_file.startswith(prefix):
                    files_list.append(os.path.join(root, special_file))
            else:
                files_list.append(os.path.join(root, special_file))
    return files_list[0]
