# -*- coding:utf-8 -*-
import logging

import math


# total 是rom容量
def avg_men(men, total):
    if len(men):
        _men = [math.ceil(((men[i]) / total) * 1024) for i in range(len(men))]
        men = str(math.ceil(sum(_men) / len(_men))) + "M"
        logging.info('计算平均内存消耗： ' + men)
        return men
    return "0"


def avg_cpu(cpu):
    if len(cpu):
        resutl = "%.1f" % (sum(cpu) / len(cpu))
        cpu = str(math.ceil(float(resutl)*10)) + "%"
        logging.info('计算平均CPU消耗： ' + cpu)
        return cpu
    return "0%"


def avg_fps(fps):
    if len(fps):
        fps = '%.2f' % float(str(math.ceil(sum(fps) / len(fps))))
        logging.info('平均FPS： ' + fps)
        return fps
    return 0.00


def max_men(men):
    if len(men):
        logging.info("men=" + str(men))
        return str(math.ceil((max(men)) / 1024)) + "M"
    return "0M"


def max_cpu(cpu):
    logging.info("maxCpu="+str(cpu))
    if len(cpu):
        result = "%.1f" % max(cpu)
        cpu = str(math.ceil(float(result)*10)) + "%"
        logging.info('计算最大的CPU消耗： '+cpu)
        return cpu
    return "0%"


def max_fps(fps):
    logging.info('最大的FPS： '+str(fps))
    return str(max(fps))


def max_flow(flow):
    logging.info('计算最大的上传流量及下载流量')
    logging.info("----------maxFlow111----------")
    logging.info(flow)
    _flowUp = []
    _flowDown = []
    for i in range(len(flow[0])):
        if i + 1 == len(flow[0]):
            break
        _flowUp.append(math.ceil((flow[0][i + 1] - flow[0][i]) / 1024))
    for i in range(len(flow[1])):
        if i + 1 == len(flow[1]):
            break
        _flowDown.append(math.ceil((flow[1][i + 1] - flow[1][i]) / 1024))
    if _flowUp:
        max_fps_up = str(max(_flowUp)) + "KB"  # 上行流量
    else:
        max_fps_up = "0"
    if _flowDown:
        max_fps_down = str(max(_flowDown)) + "KB"  # 下行流量
    else:
        max_fps_down = "0"
    return max_fps_up, max_fps_down


def avg_flow(flow):
    logging.info('计算平均上传流量及下载流量')
    _flowUp = []
    _flowDown = []
    for i in range(len(flow[0])):
        if i + 1 == len(flow[0]):
            break
        _flowUp.append((flow[0][i + 1] - flow[0][i])/1024)

    for i in range(len(flow[1])):
        if i + 1 == len(flow[1]):
            break
        _flowDown.append((flow[1][i + 1] - flow[1][i])/1024)
    try:
        avg_fps_up = str(math.ceil(sum(_flowUp) / len(_flowUp))) + "KB"
        avg_fps_down = str(math.ceil(sum(_flowDown) / len(_flowDown))) + "KB"
    except:
        avg_fps_up = '0KB'
        avg_fps_down = '0KB'
    return avg_fps_up, avg_fps_down

# if __name__ == '__main__':
#     flow = [[93919172, 94987124, 96309507], [14250800, 14285269, 14331153]]
#     cpu  = [1.9164759725400458, 0.40045766590389015, 0.8493771234428086, 1.8407534246575343]
#     men = [310171, 323267, 321179, 317913, 316569, 335277, 323853, 315837, 333765, 333829, 337433, 337473, 339877, 328953, 328881, 328909, 334029, 329873, 334645, 338649, 332541, 329273, 333581]
#
#     print(avgMen(men, 3014000))
#     # print(maxFlow(flow))
