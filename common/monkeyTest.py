# -*- coding: utf-8 -*-
import logging
import os
import uuid
import time

import datetime

from common import Phoneinfo, MonkeyConfig, Monitor, Path
from common.File import OperateFile
from common.Pickle import write_info, read_info
from common.WriteReport import report

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


info = []


# 手机信息
def get_phone(devices):
    os.popen('adb shell')
    logging.info('获取手机信息')
    bg = Phoneinfo.get_phone_kernel(devices)
    app = {}
    app["phone_name"] = bg[0]["phone_name"] + "_" + bg[0]["phone_model"] + "_" + bg[0]["version"]
    app["pix"] = bg[3]
    app["rom"] = bg[1]
    app["kel"] = bg[2]
    logging.info(app)
    return app


def mkdirInit(devices, app):
    # destroy(devices)
    # cpu = PATH("../info/" + devices + "_cpu.pickle")
    # men = PATH("../info/" + devices + "_men.pickle")
    # flow = PATH("../info/" + devices + "_flow.pickle")
    # battery = PATH("../info/" + devices + "_battery.pickle")
    # fps = PATH("../info/" + devices + "_fps.pickle")
    cpu = Path.info_path()+'\\'+devices + "_cpu.pickle"
    men = Path.info_path()+'\\'+devices + "_men.pickle"
    flow = Path.info_path()+'\\'+devices + "_flow.pickle"
    battery = Path.info_path()+'\\'+devices + "_battery.pickle"
    fps = Path.info_path()+'\\'+devices + "_fps.pickle"
    app[devices] = {"cpu": cpu, "men": men, "flow": flow, "battery": battery, "fps": fps, "header": get_phone(devices)}
    OperateFile(cpu).mkdir_file()
    OperateFile(men).mkdir_file()
    OperateFile(flow).mkdir_file()
    OperateFile(battery).mkdir_file()
    OperateFile(fps).mkdir_file()
    # OperateFile(PATH("../info/info.pickle")).remove_file()
    # OperateFile(PATH("../info/info.pickle")).mkdir_file()  # 用于记录统计结果的信息，是[{}]的形式
    OperateFile(Path.info_path()+'\\'+"info.pickle").remove_file()
    OperateFile(Path.info_path()+'\\'+"info.pickle").mkdir_file()


def start(devices):
    # num = devicess["num"]
    app = {}
    mkdirInit(devices, app)
    mc = MonkeyConfig.monkey_config(Path.scan_files(postfix='.ini'))
    # 打开想要的activity
    # ba.open_app(mc["package_name"], mc["activity"], devices) 留着备用可以统计每次打开哪个页面的启动时间等
    # monkey开始测试
    mc["log"] = Path.log_path() + "\\" + str(uuid.uuid4())
    logging.debug('log路径 ' + mc["log"])
    mc["monkey_log"] = mc["log"] + "monkey.log"
    logging.debug('monkey日志路径： '+mc["monkey_log"])
    mc["cmd"] = mc['cmd'] + mc["monkey_log"]
    start_monkey("adb -s " + devices + " shell " + mc["cmd"], mc["log"])
    time.sleep(1)
    start_time = datetime.datetime.now()
    logging.info('测试开始时间 '+str(start_time))
    pid = Monitor.get_pid(mc["package_name"], devices)
    cpu_kel = Monitor.get_cpu_kel(devices)
    before_battery = Monitor.get_battery(devices)
    num = 0
    while True:
        with open(mc["monkey_log"], encoding='utf-8') as monkey_log:
            time.sleep(1)  # 每1秒采集检查一次
            num = num+1
            Monitor.cpu_rate(pid, cpu_kel, devices)
            Monitor.get_men(mc["package_name"], devices)
            Monitor.get_fps(mc["package_name"], devices)
            Monitor.get_flow(pid, mc["net"], devices)
            Monitor.get_battery(devices)
            if monkey_log.read().count('Monkey finished') > 0:
                end_time = datetime.datetime.now()
                logging.info(str(devices)+"测试完成咯")
                # write_sum(1, path=PATH("./info/sumInfo.pickle"))
                app[devices]["header"]["beforeBattery"] = before_battery
                app[devices]["header"]["afterBattery"] = Monitor.get_battery(devices)
                app[devices]["header"]["net"] = mc["net"]
                app[devices]["header"]["monkey_log"] = mc["monkey_log"]
                app[devices]["header"]["time"] = str((end_time - start_time).seconds) + "秒"
                app[devices]['num'] = num
                write_info(app, Path.scan_files(select_path=Path.info_path(), postfix='info.pickle'))
                monkey_log.close()
                break
    monkey_log.close()
    logging.info(read_info(Path.scan_files(select_path=Path.info_path(), postfix='info.pickle')))
    logging.info('测试结束。。。。。')
    report(read_info(Path.scan_files(select_path=Path.info_path(), postfix='info.pickle')))
    os.popen("taskkill /f /t /im adb.exe")


# 开始脚本测试
def start_monkey(cmd, log):
    # Monkey测试结果日志:monkey_log
    logging.info('执行monkey')
    try:
        os.popen(cmd)
        logging.info(cmd)

        # Monkey时手机日志,logcat
        log_cat_name = log + r"logcat.log"
        logging.info('手机日志存放路径 ' + log_cat_name)
        cmd2 = "adb logcat -d >%s" % log_cat_name
        os.popen(cmd2)

        # "导出traces文件"
        traces_name = log + r"traces.log"
        logging.info('到处traces文件' + traces_name)
        cmd3 = "adb shell cat /data/anr/traces.txt>%s" % traces_name
        os.popen(cmd3)
    except Exception as e:
        logging.error('执行monkey失败')
        logging.error(e)
        raise


def kill_port():
    logging.info('关闭adb服务')
    os.popen("adb kill-server adb")
    logging.info('开启adb服务')
    os.popen("adb start-server")


# if __name__ == '__main__':
#     kill_port()
#     time.sleep(1)
#     # runner_pool()
#     start()
