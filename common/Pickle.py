# -*- coding:utf-8 -*-
import logging
import pickle
import os

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def write_sum(init, data=None, path="data.pickle"):
    if init == 0:
        result = data
    else:
        _read = read_info(path)
        logging.info(_read)
        result = _read - 1

    with open(path, 'wb') as f:
        logging.info("------writeSum-------")
        logging.info(result)
        pickle.dump(result, f)
        f.close()


def read_sum(path):
    data = {}
    with open(path, 'rb') as f:
        data = pickle.load(f)
        data = {}
        f.close()
    logging.info("------read-------")
    logging.info(path)
    logging.info(data)
    return data


def read_info(path):
    data = []
    with open(path, 'rb') as f:
        try:
            data = pickle.load(f)
            # print(data)
        except EOFError:
            data = []
    f.close()
    logging.info("------read-------")
    logging.info(path)
    logging.info(data)
    return data


def write_info(data, path="data.pickle"):
    _read = read_info(path)
    result = []
    if _read:
        _read.append(data)
        result = _read
    else:
        result.append(data)
    with open(path, 'wb') as f:
        logging.info("------writeInfo-------")
        logging.info(result)
        pickle.dump(result, f)
        f.close()


def write_flow_info(upflow, downflow, path="data.pickle"):
    logging.info("---data-----")
    logging.info("上行流量="+str(upflow))
    logging.info("下行流量="+str(downflow))

    _read = read_info(path)
    result = [[], []]
    if _read:
        _read[0].append(upflow)
        _read[1].append(downflow)
        result = _read
    else:
        result[0].append(upflow)
        result[1].append(downflow)
    with open(path, 'wb') as f:
        logging.info("------writeFlowInfo-------")
        logging.info(result)
        pickle.dump(result, f)
        f.close()


