# -*- coding:utf-8 -*-
import logging

import math


# total 是rom容量
def avg_men(men, total):
    """
    计算平均内存消耗
    :param men: 测试过程中获取的内存占用情况的列表
    :param total: 被测设备总的内存
    :return:
    """
    if len(men):
        logging.info('----------计算平均内存消耗----------')
        _men = [math.ceil(((men[i]) / total) * 1024) for i in range(len(men))]
        logging.debug(_men)
        men = str(math.ceil(sum(_men) / len(_men))) + "M"
        logging.info('计算平均内存消耗： ' + men)
        return men
    return "0"


def avg_cpu(cpu):
    """
    计算平均CPU占用
    :param cpu: 测试过程中获取的CPU占用情况的列表
    :return:
    """
    if len(cpu):
        logging.info('----------计算评价CPU消耗----------')
        resutl = "%.1f" % (sum(cpu) / len(cpu))
        logging.debug("resutl = "+resutl)
        cpu = str(math.ceil(float(resutl)*10)) + "%"
        logging.info('计算平均CPU消耗： ' + cpu)
        return cpu
    return "0%"


def avg_fps(fps):
    """
    计算平均FPS情况
    :param fps: 测试过程中获取的FPS情况的列表
    :return:
    """
    if len(fps):
        logging.info('----------计算平均FPS----------')
        fps = '%.2f' % float(str(math.ceil(sum(fps) / len(fps))))
        logging.info('平均FPS： ' + fps)
        return fps
    return 0.00


def max_men(men):
    """
    计算最大的内存占用
    :param men: 测试过程中获取的内存占用情况的列表
    :return:
    """
    if len(men):
        logging.info('----------计算最大的内存占用----------')
        logging.info("men=" + str(men))
        return str(math.ceil((max(men)) / 1024)) + "M"
    return "0M"


def max_cpu(cpu):
    """
    计算最大的CPU占用
    :param cpu: 测试过程中获取的内存占用情况的列表
    :return:
    """
    logging.info('----------计算最大的CPU消耗-----------')
    logging.info("maxCpu="+str(cpu))
    if len(cpu):
        result = "%.1f" % max(cpu)
        logging.debug("result = "+result)
        cpu = str(math.ceil(float(result)*10)) + "%"
        logging.info('最大的CPU消耗： '+cpu)
        return cpu
    return "0%"


def max_fps(fps):
    """
    计算最大的FPS
    :param fps:
    :return:
    """
    logging.info('----------计算最大的FPS-----------')
    logging.info('最大的FPS： '+str(fps))
    return str(max(fps))


def max_flow(flow):
    """
    计算最大的上传流量和下载流量
    :param flow: 流量消耗列表
    :return:
    """
    logging.info('----------计算最大的上传流量及下载流量----------')
    logging.debug(flow)
    _flowUp = []
    _flowDown = []
    for i in range(len(flow[0])):
        if i + 1 == len(flow[0]):
            break
        _flowUp.append(math.ceil((flow[0][i + 1] - flow[0][i]) / 1024))
        logging.debug(_flowUp)
    for i in range(len(flow[1])):
        if i + 1 == len(flow[1]):
            break
        _flowDown.append(math.ceil((flow[1][i + 1] - flow[1][i]) / 1024))
        logging.debug(_flowDown)
    if _flowUp:
        max_fps_up = str(max(_flowUp)) + "KB"  # 上行流量
    else:
        max_fps_up = "0"
    if _flowDown:
        max_fps_down = str(max(_flowDown)) + "KB"  # 下行流量
    else:
        max_fps_down = "0"
    logging.info('最大的上传流量 ' + max_fps_up)
    logging.info('最大的下载流量 ' + max_fps_down)
    return max_fps_up, max_fps_down


def avg_flow(flow):
    """
    计算平均下载流量和下载流量
    :param flow: 流量消耗列表
    :return:
    """
    logging.info('----------计算平均上传流量及下载流量----------')
    logging.debug(flow)
    _flowUp = []
    _flowDown = []
    for i in range(len(flow[0])):
        if i + 1 == len(flow[0]):
            break
        _flowUp.append((flow[0][i + 1] - flow[0][i])/1024)
    logging.debug(_flowUp)
    for i in range(len(flow[1])):
        if i + 1 == len(flow[1]):
            break
        _flowDown.append((flow[1][i + 1] - flow[1][i])/1024)
        logging.debug(_flowDown)
    if len(_flowUp):
        avg_fps_up = str(math.ceil(sum(_flowUp) / len(_flowUp))) + "KB"
    else:
        avg_fps_up = '0KB'
    if len(_flowDown):
        avg_fps_down = str(math.ceil(sum(_flowDown) / len(_flowDown))) + "KB"
    else:
        avg_fps_down = '0KB'
    logging.info('avg_fps_up: ' + avg_fps_up)
    logging.info('avg_fps_down: ' + avg_fps_down)
    return avg_fps_up, avg_fps_down


# if __name__ == '__main__':
#     logging.basicConfig(level=logging.DEBUG,
#                         format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                         datefmt='%a, %d %b %Y %H:%M:%S',
#                         filemode='w')
#     flow = [[93919172, 94987124, 96309507], [14250800, 14285269, 14331153]]
#     cpu = [1.9164759725400458, 0.40045766590389015, 0.8493771234428086, 1.8407534246575343]
#     men = [310171, 323267, 321179, 317913, 316569, 335277, 323853, 315837, 333765, 333829, 337433, 337473, 339877,
#            328953, 328881, 328909, 334029, 329873, 334645, 338649, 332541, 329273, 333581]
#     # print(maxFlow(flow))
