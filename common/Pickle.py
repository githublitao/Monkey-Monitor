# -*- coding:utf-8 -*-
import logging
import pickle
import os

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def write_sum(init, data=None, path="data.pickle"):
    """
    写入设备信息
    :param init:  设备数量
    :param data:  内容
    :param path:  文件路径
    :return:
    """
    logging.info('写入设备信息，文件路径 ' + path)
    logging.debug(init)
    logging.debug(data)
    logging.debug(path)
    try:
        if init == 0:
            result = data
            logging.debug('sum = ' + result)
        else:
            _read = read_info(path)
            logging.debug(_read)
            result = _read - 1

        with open(path, 'wb') as f:
            logging.info("正在写入中。。。。。。。")
            logging.debug(result)
            pickle.dump(result, f)
            f.close()
            logging.info('写入完成。。。。')
    except Exception as e:
        logging.error('写入设备信息失败')
        logging.error(e)
        raise


def read_sum(path):
    """
    读取设备信息
    :param path: sum.pickle文件路径
    :return:
    """
    try:
        logging.info('读取设备信息文件 ' + path)
        with open(path, 'rb') as f:
            data = pickle.load(f)
            f.close()
        logging.info('读取完成')
        logging.debug(data)
        return data
    except Exception as e:
        logging.error('读取设备信息文件失败： '+path)
        logging.error(e)
        raise


def read_info(path):
    """
    读取记录结果的文件
    :param path: info.pickle文件的路径
    :return:
    """
    try:
        logging.info('读取测试结果' + path)
        with open(path, 'rb') as f:
            try:
                data = pickle.load(f)
                # print(data)
            except EOFError:
                data = []
        f.close()
        logging.info('读取完成')
        logging.debug(data)
        return data
    except Exception as e:
        logging.error('读取测试结果失败')
        logging.error(e)
        raise


def write_info(data, path="data.pickle"):
    """
    写入测试结果
    :param data:  待写入的内容
    :param path:  测试结果保存的文件路径
    :return:
    """
    logging.info('写入测试结果 ' + path)
    logging.debug(data)
    logging.debug(path)
    try:
        _read = read_info(path)
        logging.debug(_read)
        result = []
        if _read:
            _read.append(data)
            result = _read
        else:
            result.append(data)
        logging.debug(result)
        with open(path, 'wb') as f:
            pickle.dump(result, f)
            f.close()
        logging.info('写入完成')
    except Exception as e:
        logging.error('写入结果失败')
        logging.error(e)
        raise


def write_flow_info(upflow, downflow, path="data.pickle"):
    """
    写入流量信息
    :param upflow:   上传流量
    :param downflow:  下载流量
    :param path:
    :return:
    """
    logging.info('写入流量信息')
    logging.debug("上行流量="+str(upflow))
    logging.debug("下行流量="+str(downflow))
    logging.debug(path)
    try:
        _read = read_info(path)
        logging.debug(_read)
        result = [[], []]
        if _read:
            _read[0].append(upflow)
            _read[1].append(downflow)
            result = _read
        else:
            result[0].append(upflow)
            result[1].append(downflow)
        with open(path, 'wb') as f:
            logging.debug(result)
            pickle.dump(result, f)
            f.close()
        logging.info('写入完成。。。。。')
    except Exception as e:
        logging.error('写入流量信息失败')
        logging.error(e)
        raise



