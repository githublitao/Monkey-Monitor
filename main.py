import logging
import time

import os

from common import AdbCommon
from common.monkeyTest import kill_port, start

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filemode='w')
    ba = AdbCommon.AndroidDebugBridge()
    device = ba.attached_devices()
    if device:
        kill_port()
        time.sleep(1)
        start(device[0].split(' ')[-1])
    else:
        logging.error('请连接手机或开启USB调试模式')
