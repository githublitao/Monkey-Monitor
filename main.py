import logging
import threading

import time

from common import AdbCommon
from common.monkeyTest import kill_port, start

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filemode='w')
    wifi_list = ['127.0.0.1:21503', ]
    try:
        kill_port()
        time.sleep(3)
        ba = AdbCommon.AndroidDebugBridge()
        ba.connect_wifi_devices(wifi_list)
        device = ba.attached_devices()
        logging.debug(device)
        if device:
            for i in device:
                t1 = threading.Thread(target=start, args=(i,))
                t1.start()
        else:
            logging.error('请连接手机或开启USB调试模式')
    except Exception as e:
        logging.exception('error')
        logging.error('测试失败，请查看日志')
        logging.error(e)

