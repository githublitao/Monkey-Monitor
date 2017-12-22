# -*- coding: utf-8 -*-
import logging
import os
import uuid
import time

import datetime

from common import Phoneinfo, MonkeyConfig, Monitor
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


def mkdirInit(devices, app, data=None):
    # destroy(devices)
    cpu = PATH("../info/" + devices + "_cpu.pickle")
    men = PATH("../info/" + devices + "_men.pickle")
    flow = PATH("../info/" + devices + "_flow.pickle")
    battery = PATH("../info/" + devices + "_battery.pickle")
    fps = PATH("../info/" + devices + "_fps.pickle")
    app[devices] = {"cpu": cpu, "men": men, "flow": flow, "battery": battery, "fps": fps, "header": get_phone(devices)}
    OperateFile(cpu).mkdir_file()
    OperateFile(men).mkdir_file()
    OperateFile(flow).mkdir_file()
    OperateFile(battery).mkdir_file()
    OperateFile(fps).mkdir_file()
    OperateFile(PATH("../info/info.pickle")).remove_file()
    OperateFile(PATH("../info/info.pickle")).mkdir_file() # 用于记录统计结果的信息，是[{}]的形式


def start(devices):
    # num = devicess["num"]
    app = {}
    mkdirInit(devices, app)
    mc = MonkeyConfig.monkeyConfig(PATH("../monkey.ini"))
    # 打开想要的activity
    # ba.open_app(mc["package_name"], mc["activity"], devices) 留着备用可以统计每次打开哪个页面的启动时间等
    # monkey开始测试
    mc["log"] = PATH("../log") + "\\" + str(uuid.uuid4())
    mc["monkey_log"] = mc["log"] + "monkey.log"
    logging.info('monkey日子路径： '+mc["monkey_log"])
    mc["cmd"] = mc['cmd'] + mc["monkey_log"]
    start_monkey("adb -s " + devices + " shell " + mc["cmd"], mc["log"])
    time.sleep(1)
    starttime = datetime.datetime.now()
    logging.info('测试开始时间 '+str(starttime))
    pid = Monitor.get_pid(mc["package_name"], devices)
    cpu_kel = Monitor.get_cpu_kel(devices)
    beforeBattery = Monitor.get_battery(devices)
    while True:
        with open(mc["monkey_log"], encoding='utf-8') as monkeylog:
            time.sleep(1)  # 每1秒采集检查一次
            Monitor.cpu_rate(pid, cpu_kel, devices)
            Monitor.get_men(mc["package_name"], devices)
            Monitor.get_fps(mc["package_name"], devices)
            Monitor.get_flow(pid, mc["net"], devices)
            Monitor.get_battery(devices)
            if monkeylog.read().count('Monkey finished') > 0:
                endtime = datetime.datetime.now()
                logging.info(str(devices)+"测试完成咯")
                # write_sum(1, path=PATH("./info/sumInfo.pickle"))
                app[devices] ["header"]["beforeBattery"] = beforeBattery
                app[devices]["header"]["afterBattery"] = Monitor.get_battery(devices)
                app[devices]["header"]["net"] = mc["net"]
                app[devices]["header"]["monkey_log"] = mc["monkey_log"]
                app[devices]["header"]["time"] = str((endtime - starttime).seconds) + "秒"
                write_info(app, PATH("../info/info.pickle"))
                monkeylog.close()
                break
        monkeylog.close()
    logging.info(read_info(PATH("../info/info.pickle")))
    report(read_info(PATH("../info/info.pickle")))
    os.popen("taskkill /f /t /im adb.exe")


# 开始脚本测试
def start_monkey(cmd, log):
    # Monkey测试结果日志:monkey_log
    os.popen(cmd)
    logging.info(cmd)

    # Monkey时手机日志,logcat
    logcatname = log + r"logcat.log"
    cmd2 = "adb logcat -d >%s" % (logcatname)
    os.popen(cmd2)

    # "导出traces文件"
    tracesname = log + r"traces.log"
    cmd3 = "adb shell cat /data/anr/traces.txt>%s" % tracesname
    os.popen(cmd3)


def kill_port():
    os.popen("adb kill-server adb")
    os.popen("adb start-server")


# if __name__ == '__main__':
#     kill_port()
#     time.sleep(1)
#     # runner_pool()
#     start()