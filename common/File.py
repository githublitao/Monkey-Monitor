# -*- coding:utf-8 -*-
import logging

__author__ = 'shikun'
import os

'''
操作文件
'''


class OperateFile:
    # method(r,w,a)
    def __init__(self, file, method='w+'):
        """
        :param file: 文件的路径
        :param method: 读写方式r , r+ , w , w+ , a , a+， 默认w+，可读可写，若文件不存在，创建
        """
        self.file = file
        self.method = method
        self.fileHandle = None

    def write_txt(self, line):
        """
        :param line: 写入的内容
        :return:
        """
        OperateFile(self.file).check_file()
        try:
            logging.info('写入文件')
            logging.debug(self.file + '写入内容' + line)
            self.fileHandle = open(self.file, self.method)
            self.fileHandle.write(line + "\n")
            self.fileHandle.close()
        except Exception as e:
            logging.error('写入文件失败')
            logging.error(e)
            raise

    def read_txt_row(self):
        resutl = ""
        try:
            logging.info('读取文件 ' + self.file)
            if OperateFile(self.file).check_file():
                self.fileHandle = open(self.file, self.method)
                resutl = self.fileHandle.readline()
                self.fileHandle.close()
            logging.debug('读取的文件内容： ' + resutl)
            return resutl
        except Exception as e:
            logging.error('读取文件失败')
            logging.error(e)
            raise

    def read_txt_rows(self):
        try:
            logging.info('读取文件 ' + self.file)
            if OperateFile(self.file).check_file():
                self.fileHandle = open(self.file, self.method)
                file_list = self.fileHandle.readlines()
                logging.debug('读取的文件内容： ')
                logging.debug(file_list)
                for i in file_list:
                    logging.info(i.strip("\n"))
                self.fileHandle.close()
        except Exception as e:
            logging.error('读取文件失败')
            logging.error(e)
            raise

    def check_file(self):
        """
        检查文件是否存在
        :return:
        """
        logging.info('检查文件是否存在 ' + self.file)
        if not os.path.isfile(self.file):
            logging.info('文件不存在' + self.file)
            # sys.exit()
            return False
        else:
            return True
        # print("文件存在！")

    def mkdir_file(self):
        """
        创建文件目录
        :return:
        """
        try:
            logging.info('创建文件 ' + self.file)
            if not os.path.isfile(self.file):
                f = open(self.file, self.method)
                f.close()
                logging.info("创建文件成功 " + self.file)
            else:
                os.remove(self.file)
                f = open(self.file, self.method)
                f.close()
                logging.info("创建文件成功 " + self.file)
        except Exception as e:
            logging.error('创建文件失败 ' + self.file)
            logging.error(e)
            raise

    def remove_file(self):
        """
        删除文件
        :return:
        """
        logging.info('删除文件 ' + self.file)
        try:
            if os.path.isfile(self.file):
                os.remove(self.file)
                logging.info("删除文件成功")
            else:
                logging.info("文件不存在 " + self.file)
        except Exception as e:
            logging.error('删除文件失败 ' + self.file)
            logging.error(e)
            raise

    def mk_dir(self):
            # 去除首位空格
            path = self.file.strip()
            # 去除尾部 \ 符号
            path = path.rstrip("\\")

            # 判断路径是否存在
            # 存在     True
            # 不存在   False
            is_exists = os.path.exists(path)

            # 判断结果
            if not is_exists:
                try:
                    # 如果不存在则创建目录
                    # 创建目录操作函数
                    os.makedirs(path)
                except Exception as e:
                    logging.error('新建路径失败' + self.file)
                    logging.error(e)
                    raise
            else:
                # 如果目录存在则不创建，并提示目录已存在
                pass

# if __name__ == '__main__':
#     logging.basicConfig(level=logging.DEBUG,
#                         format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                         datefmt='%a, %d %b %Y %H:%M:%S',
#                         filemode='w')
#     bf = OperateFile("text.xml")
#     if not bf.check_file():
#         bf.mkdir_file()
#     bf.write_txt("111")
