# -*- coding:utf-8 -*-
import subprocess
import os
import re
from wsgiref.validate import validator
import time
import logging

from common import Pickle, Path
from common.Custom_exception import GetPidError, ConnectAdbError


# 获取menu
def get_men(pkg_name, devices):
    """
    获取应用占用内存 adb -s 设备唯一标识（devices） shell dumpsys meminfo 包名（pkg_name）
    :param pkg_name: 被测应用包名
    :param devices: 被测设备唯一标识
    :return:
    """
    try:
        logging.info('读取 ' + pkg_name + ' 内存占用')
        cmd = "adb -s " + devices + " shell  dumpsys  meminfo %s" % pkg_name
        logging.info(cmd)
        output = subprocess.check_output(cmd).split()
        logging.debug(output)
        if not output:
            raise ConnectAdbError
        s_men = ".".join([x.decode() for x in output])  # 转换为string
        logging.debug("s_men = "+s_men)
        men2 = int(re.findall("TOTAL.(\d+)*", s_men, re.S)[0])
    except ConnectAdbError as e:
        logging.error(e)
        raise
    except Exception as e:
        logging.error(e)
        men2 = 0
    logging.info('读取内存占用： ' + str(men2))
    Pickle.write_info(men2, Path.scan_files(select_path=Path.info_path(), postfix=devices+'_men.pickle'))
    # Pickle.write_info(men2, PATH("../info/" + devices + "_men.pickle"))
    return men2


# 得到FPS
def get_fps(pkg_name, devices):
    """
    获取应用运行时的FPS  adb -s 设备的唯一标识（devices） shell dumpsys gfxinfo 包名（pkg_name）
    :param pkg_name:  被测应用包名
    :param devices:  被测设备的唯一标识
    :return:
    """
    logging.info('读取 ' + pkg_name + ' 运行时的FPS')
    try:
        _adb = "adb -s " + devices + " shell dumpsys gfxinfo %s" % pkg_name
        logging.info(_adb)
        results = os.popen(_adb).read().strip()
        if not results:
            raise ConnectAdbError
        logging.debug("results = "+results)
        frames = [x for x in results.split('\n') if validator(x)]
        logging.debug(frames)
        frame_count = len(frames)
        jank_count = 0
        vsync_overtime = 0
        render_time = 0
        for frame in frames:
            time_block = re.split(r'\s+', frame.strip())
            if len(time_block) == 3:
                try:
                    render_time = float(time_block[0]) + float(time_block[1]) + float(time_block[2])
                except:
                    render_time = 0

            '''
            当渲染时间大于16.67，按照垂直同步机制，该帧就已经渲染超时
            那么，如果它正好是16.67的整数倍，比如66.68，则它花费了4个垂直同步脉冲，减去本身需要一个，则超时3个
            如果它不是16.67的整数倍，比如67，那么它花费的垂直同步脉冲应向上取整，即5个，减去本身需要一个，即超时4个，可直接算向下取整

            最后的计算方法思路：
            执行一次命令，总共收集到了m帧（理想情况下m=128），但是这m帧里面有些帧渲染超过了16.67毫秒，算一次jank，一旦jank，
            需要用掉额外的垂直同步脉冲。其他的就算没有超过16.67，也按一个脉冲时间来算（理想情况下，一个脉冲就可以渲染完一帧）

            所以FPS的算法可以变为：
            m / （m + 额外的垂直同步脉冲） * 60
            '''
            if render_time > 16.67:
                jank_count += 1
                if render_time % 16.67 == 0:
                    vsync_overtime += int(render_time / 16.67) - 1
                else:
                    vsync_overtime += int(render_time / 16.67)

        _fps = int(frame_count * 60 / (frame_count + vsync_overtime))
    except ConnectAdbError as e:
        logging.error(e)
        raise
    except Exception as e:
        logging.error(e)
        _fps = 0
    logging.info('读取FPS： '+str(_fps))
    Pickle.write_info(_fps, Path.scan_files(select_path=Path.info_path(), postfix=devices+'_fps.pickle'))
    # Pickle.write_info(_fps, PATH("../info/" + devices + "_fps.pickle"))


def get_battery(devices):
    """
    获取设备当前电量  adb -s 设备唯一标识（devices） shell dumpsys battery
    :param devices: 被测设备唯一标识
    :return:
    """
    try:
        logging.info('获取设备的当前电量')
        cmd = "adb -s " + devices + " shell dumpsys battery"
        logging.info(cmd)
        output = subprocess.check_output(cmd).split()
        if not output:
            raise ConnectAdbError
        logging.debug(output)
        st = ".".join([x.decode() for x in output])  # 转换为string
        logging.debug("st = "+st)
        battery2 = int(re.findall("level:.(\d+)*", st, re.S)[0])
    except ConnectAdbError as e:
        logging.error(e)
        raise
    except Exception as e:
        logging.error(e)
        battery2 = 90
    logging.info('读取手机电量： '+str(battery2))
    # Pickle.write_info(battery2, PATH("../info/" + devices + "_battery.pickle"))
    Pickle.write_info(battery2, Path.scan_files(select_path=Path.info_path(), postfix=devices + '_battery.pickle'))
    return battery2


def get_pid(pkg_name, devices):
    """
    获取被测应用运行时的PID   adb -s 设备的唯一标识（devices） shell ps | findstr 包名（pkg_name）
    :param pkg_name: 被测应用包名
    :param devices: 被测设备唯一标识
    :return:
    """
    try:
        logging.info('获取被测应用运行时的PID')
        cmd = "adb -s " + devices + " shell ps | findstr " + pkg_name
        logging.info(cmd)
        pid = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE).stdout.readlines()
        logging.debug(pid)
        for item in pid:
            logging.debug(item)
            if item.split()[8].decode() == pkg_name:
                logging.debug(item)
                logging.info('获取待测应用的PID： '+item.split()[1].decode())
                return item.split()[1].decode()
        raise GetPidError   # 循环完毕后未获取到应用的PID，主动抛出异常
    except Exception as e:
        logging.error('获取待测应用的PID失败')
        logging.error(e)
        raise


def get_flow(uid, devices):
    """
    获取应用的流量信息   adb -s 设备的唯一标识（devices） shell cat /proc/PID(pd)/net/dev
    :param uid: UID值
    :param devices: 被测设备唯一标识
    :return:
    """
    logging.info('获取应用的流量信息')
    try:
        if uid is not None:
            cmd = "adb -s " + devices + " shell cat /proc/uid_stat/" + uid + "/tcp_snd"
            logging.info(cmd)
            _flow = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE).stdout.readlines()
            if not _flow:
                raise ConnectAdbError
            logging.debug(_flow)
            up_flow = _flow[0].split()[0].decode()
            logging.debug('上行流量： %sKB ' % up_flow)
            _adb = "adb -s " + devices + " shell cat /proc/uid_stat/" + uid + "/tcp_rcv"
            logging.info(_adb)
            _flow_down = subprocess.Popen(_adb, shell=True, stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE).stdout.readlines()
            if not _flow_down:
                raise ConnectAdbError
            logging.debug(_flow_down)
            down_flow = _flow_down[0].split()[0].decode()
            logging.debug('下行流量： %sKB ' % down_flow)
            Pickle.write_flow_info(int(up_flow), int(down_flow), Path.scan_files(select_path=Path.info_path(),
                                                                       postfix=devices+'_flow.pickle'))
    except ConnectAdbError as e:
        logging.error(e)
        raise
    except Exception as e:
        logging.error('获取应用流量信息失败')
        logging.error(e)


def total_cpu_time(devices):
    """
    CPU快照  adb - s 设备的唯一标识（devices）shell cat /proc/stat
    user: 从系统启动开始累计到当前时刻，处于用户态的运行时间，不包含 nice值为负进程。
    nice: 从系统启动开始累计到当前时刻，nice值为负的进程所占用的CPU时间
    system: 从系统启动开始累计到当前时刻，处于核心态的运行时间
    idle: 从系统启动开始累计到当前时刻，除IO等待时间以外的其它等待时间
    io_wait: 从系统启动开始累计到当前时刻，IO等待时间(since 2.5.41)
    irq: 从系统启动开始累计到当前时刻，硬中断时间(since 2.6.0-test4)
    soft_irq: 从系统启动开始累计到当前时刻，软中断时间(since 2.6.0-test4)
    steal_stolen: 这是时间花在其他的操作系统在虚拟环境中运行时（since 2.6.11）
    guest: 这是运行时间guest 用户Linux内核的操作系统的控制下的一个虚拟CPU（since 2.6.24）
    :param devices: 设备的唯一标识
    :return:
    """
    logging.info('获取运行过程中CPU处理时间')
    try:
        cmd = "adb -s " + devices + " shell cat /proc/stat"
        logging.info(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        if not p:
            raise ConnectAdbError
        logging.debug(p)
        (output, err) = p.communicate()
        res = output.split()
        logging.debug(res)
        for info in res:
            logging.debug(info)
            if info.decode() == "cpu":
                user = res[1].decode()
                nice = res[2].decode()
                system = res[3].decode()
                idle = res[4].decode()
                io_wait = res[5].decode()
                irq = res[6].decode()
                soft_irq = res[7].decode()
                logging.info("从系统启动开始累计到当前时刻，处于用户态的运行时间: " + user)
                logging.info("nice值:" + nice)
                logging.info("从系统启动开始累计到当前时刻，处于核心态的运行时间: " + system)
                logging.info("从系统启动开始累计到当前时刻，除IO等待时间以外的其它等待时间: " + idle)
                logging.info("从系统启动开始累计到当前时刻，IO等待时间: " + io_wait)
                logging.info("从系统启动开始累计到当前时刻，硬中断时间: " + irq)
                logging.info("从系统启动开始累计到当前时刻，软中断时间: " + soft_irq)
                result = int(user) + int(nice) + int(system) + int(idle) + int(io_wait) + int(irq) + int(soft_irq)
                logging.info("总的CPU使用情况： "+str(result))
                return result
    except ConnectAdbError as e:
        logging.error(e)
        raise
    except Exception as e:
        logging.error('获取运行过程中CPU处理时间失败')
        logging.error(e)


def process_cpu_time(pd, devices):
    """
    进程快照 adb -s 设备的唯一标识（devices) shell cat /proc/PID(pd)/stat
    pid： 进程号
    u_time： 该任务在用户态运行的时间，单位为jiffies
    s_time： 该任务在核心态运行的时间，单位为jiffies
    cu_time： 所有已死线程在用户态运行的时间，单位为jiffies
    cs_time： 所有已死在核心态运行的时间，单位为jiffies
    :param pd:
    :param devices:
    :return:
    """
    logging.info('获取该应用运行时间')
    try:
        cmd = "adb -s " + devices + " shell cat /proc/" + str(pd) + "/stat"
        logging.info(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        if not p:
            raise ConnectAdbError
        logging.debug(p)
        res = output.split()
        logging.debug(res)
        u_time = res[13].decode()
        s_time = res[14].decode()
        cu_time = res[15].decode()
        cs_time = res[16].decode()
        logging.info("该任务在用户态运行的时间: "+u_time+' jiffies')
        logging.info("该任务在核心态运行的时间: "+s_time+' jiffies')
        logging.info("所有已死线程在用户态运行的时间: "+cu_time+' jiffies')
        logging.info("所有已死在核心态运行的时间: "+cs_time+' jiffies')
        result = int(u_time) + int(s_time) + int(cu_time) + int(cs_time)
        logging.info("APP消耗CPU情况： "+str(result))
    except ConnectAdbError as e:
        logging.error(e)
        raise
    except Exception as e:
        logging.error(e)
        result = 0
    return result


def get_cpu_kel(devices):
    """
    获取设备CPU个数   adb -s device shell cat /proc/cpuinfo
    :param devices:  设备的唯一标识
    :return:
    """
    logging.info('获取设备CPU个数')
    try:
        cmd = "adb -s " + devices + " shell cat /proc/cpuinfo"
        logging.info(cmd)
        output = subprocess.check_output(cmd).split()
        if not output:
            raise ConnectAdbError
        s_item = ".".join([x.decode() for x in output])  # 转换为string
        logging.debug(s_item)
        return len(re.findall("processor", s_item))
    except Exception as e:
        logging.error(e)
        raise


def cpu_rate(pd, cpu_num, devices):
    """
    计算某进程的cpu使用率
    100*( processCpuTime2 – processCpuTime1) / (totalCpuTime2 – totalCpuTime1) (按100%计算，如果是多核情况下还需乘以cpu的个数);
    cpu_num cpu几核
    pid 进程id
    :param pd:  应用运行的PID
    :param cpu_num:   CPU个数
    :param devices:  设备的唯一标识
    :return:
    """
    process_cpu_time1 = process_cpu_time(pd, devices)
    # print(process_cpu_time1)
    time.sleep(1)
    process_cpu_time2 = process_cpu_time(pd, devices)
    # print(process_cpu_time2)
    process_cpu_time3 = process_cpu_time2 - process_cpu_time1
    # print(process_cpu_time3)
    total_cpu_time1 = total_cpu_time(devices)
    # print(total_cpu_time1)
    time.sleep(1)
    total_cpu_time2 = total_cpu_time(devices)
    # print(total_cpu_time2)
    total_cpu_time3 = (total_cpu_time2 - total_cpu_time1)*cpu_num
    # print(total_cpu_time3)
    logging.info("totalCpuTime3="+str(total_cpu_time3))
    logging.info("processCpuTime3="+str(process_cpu_time3))
    # try:
    #     cpu = 100 * process_cpu_time3 / total_cpu_time3
    # except:
    #     cpu = 0
    cpu = 100 * process_cpu_time3 / total_cpu_time3
    # Pickle.write_info(cpu, PATH("../info/" + devices + "_cpu.pickle"))
    Pickle.write_info(cpu, Path.scan_files(select_path=Path.info_path(), postfix=devices+'_cpu.pickle'))
    logging.info("CPU使用率： " + str(cpu)+'%')


def get_uid(pd, devices):
    """
    获取待测应用的uid值  adb -s devices shell cat /proc/pd/status
    :param pd: PID值
    :param devices:  设备的唯一标识
    :return:
    """
    try:
        logging.info('获取应用的UID值')
        cmd = 'adb -s '+devices+' shell cat /proc/'+pd+'/status'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        if not output:
            raise ConnectAdbError
        uid = output.split()[14].decode()
        logging.debug('UID值： '+uid)
        return uid
    except ConnectAdbError as e:
        logging.error('获取应用uid失败')
        logging.error(e)
        raise
    except Exception as e:
        logging.error(e)


# if __name__ == '__main__':
#     logging.basicConfig(level=logging.DEBUG,
#                         format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                         datefmt='%a, %d %b %Y %H:%M:%S',
#                         filemode='w')
#     pid = get_pid('com.sixty.nidoneClient', 'EAROU8VOSKAM99I7')
#     uid = get_uid(pid, 'EAROU8VOSKAM99I7')
#     get_flow(uid, 'EAROU8VOSKAM99I7')
    # while True:
    #     # get_fps('com.sixty.nidoneClient', 'EAROU8VOSKAM99I7')
    #     pid = get_pid('com.sixty.nidoneClient', 'EAROU8VOSKAM99I7')
    #     # get_battery('EAROU8VOSKAM99I7')
    #     get_cpu_kel('EAROU8VOSKAM99I7')
    #     # get_flow(pid, 'gprs', 'EAROU8VOSKAM99I7')
    #     # get_men('com.sixty.nidoneClient', 'EAROU8VOSKAM99I7')
    #     cpu_rate(pid, get_cpu_kel('EAROU8VOSKAM99I7'),'EAROU8VOSKAM99I7')
