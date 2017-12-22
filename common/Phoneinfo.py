import logging
import re
import subprocess
import chardet


# def reboot(dev):
#     cmd_reboot = "adb -s " + dev + " reboot"
#     os.popen(cmd_reboot)
import os

from common.Custom_exception import ConnectAdbError


def get_model(devices):
    """
    获取Android设备信息    adb -s + devices + shell cat /system/build.prop
    :param devices:  设备的唯一标识
    :return:
    """
    logging.info('获取Android设备信息')
    result = {}
    cmd = "adb -s " + devices + " shell cat /system/build.prop"
    logging.info(cmd)
    output = subprocess.check_output(cmd).decode()
    if not output:
        raise ConnectAdbError
    logging.debug(output)
    result["version"] = re.findall("version.release=(\d\.\d)*", output, re.S)[0]    # Android 系统，如android 4.0
    result["phone_name"] = re.findall("ro.product.model=(\S+)*", output, re.S)[0]   # 手机名
    result["phone_model"] = re.findall("ro.product.brand=(\S+)*", output, re.S)[0]  # 手机品牌
    logging.info('设备信息：')
    logging.info(result)
    return result


def get_men_total(devices):
    """
    获取设备的最大内存 adb -s devices(设备的唯一标识) shell cat /proc/meminfo
    :param devices:
    :return:
    """
    logging.info('获取设备的最大内存')
    cmd = "adb -s " + devices + " shell cat /proc/meminfo"
    logging.info(cmd)
    output = subprocess.check_output(cmd).split()
    if not output:
        raise ConnectAdbError
    logging.debug("设备的最大内存是： " + str(output))
    # item = [x.decode() for x in output]
    logging.info('获取手机内存大小： ' + output[1].decode())
    return int(output[1].decode())


# 得到几核cpu
def get_cpu_kel(devices):
    """
    获取设备CPU个数  adb -s  + devices + shell cat /proc/cpuinfo
    :param devices:  设备的唯一标识
    :return:
    """
    logging.info('获取设备的唯一标识')
    cmd = "adb -s " + devices + " shell cat /proc/cpuinfo"
    logging.info(cmd)
    output = subprocess.check_output(cmd).split()
    if not output:
        raise ConnectAdbError
    logging.debug(output)
    s_item = ".".join([x.decode() for x in output]) # 转换为string
    num = str(len(re.findall("processor", s_item))) + "核"
    logging.info('获取手机内核个数：'+num)
    return num


# 得到手机分辨率
def get_app_pix(devices):
    """
    获取Android设备的分辨率  adb -s + devices + shell wm size
    :param devices:  设备的唯一标识
    :return:
    """
    logging.info('获取Android设备的分辨率')
    cmd = "adb -s " + devices + " shell wm size"
    logging.info(cmd)
    pix = subprocess.check_output(cmd).split()[2].decode()
    if not pix:
        raise ConnectAdbError
    logging.info('获取手机分辨率： '+pix)
    return pix


# 手机信息
def get_phone_kernel(devices):
    pix = get_app_pix(devices)
    men_total = get_men_total(devices)
    phone_msg = get_model(devices)
    cpu_sum = get_cpu_kel(devices)
    return phone_msg, men_total, cpu_sum, pix


# if __name__ == '__main__':
#     print(get_phone_kernel('EAROU8VOSKAM99I7'))
#     print(get_model('EAROU8VOSKAM99I7'))
#     print(get_men_total('EAROU8VOSKAM99I7'))
#     print(get_cpu_kel('EAROU8VOSKAM99I7'))
#     print(get_app_pix('EAROU8VOSKAM99I7'))
