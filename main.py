import logging
import time
import threading

from common import AdbCommon
from common.monkeyTest import kill_port, start

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filemode='w')
    try:
        ba = AdbCommon.AndroidDebugBridge()
        device = ba.attached_devices()
        logging.debug(device)
        if device:
            kill_port()
            time.sleep(1)
            for i in device:
                t1 = threading.Thread(target=start, args=(i,))
                t1.start()
                # start(device[0])
        else:
            logging.error('请连接手机或开启USB调试模式')
    except Exception as e:
        logging.exception('errpr')
        logging.error('测试失败，请查看日志')
        logging.error(e)

