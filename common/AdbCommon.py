# -*- coding:utf-8 -*-
# python module for interacting with adb
import logging
import os

from common.Custom_exception import ConnectAdbError

"""
基本的adb操作
"""


class AndroidDebugBridge(object):
    @staticmethod
    def call_adb(command):
        """
        通过ADB连接被测应用，获取信息
        :param command:
        :return:
        """
        command_result = ''
        command_text = 'adb %s' % command
        logging.info(command_text)
        results = os.popen(command_text, "r")
        logging.debug("results = " + str(results))
        if not results:
            raise ConnectAdbError
        else:
            while True:
                line = results.readline()
                if not line:
                    break
                command_result += line
            results.close()
            logging.debug("command_result = " + command_result)
            return command_result

    # check for any fast_boot device
    def fast_boot(self, device_id):
        pass

    # 检查设备
    def attached_devices(self):
        """
        检查待测是设备，获取设备列表， adb devices
        :return:
        """
        try:
            logging.info('连接检查设备')
            result = self.call_adb("devices")
            logging.debug('连接的设备 ' + result)
            devices = result.partition('\n')[2].replace('\n', '').split('\tdevice')
            return [device for device in devices if len(device) > 2]
        except Exception as e:
            logging.error('连接检查设备失败')
            logging.error(e)
            raise

    # 状态
    def get_state(self):
        """
        获取设备状态 adb get-state
        :return:
        """
        try:
            logging.info('获取设备状态')
            result = self.call_adb("get-state")
            result = result.strip(' \t\n\r')
            logging.debug("result = "+result)
            return result or None
        except Exception as e:
            logging.error('获取设备状态失败')
            logging.error(e)
            raise

    # 重启
    def reboot(self, option):
        """
        重启设备， adb reboot bootloader
        :param option: "bootloader", "recovery"
        :return:
        """
        command = "reboot"
        if len(option) > 7 and option in ("bootloader", "recovery",):
            command = "%s %s" % (command, option.strip())
        self.call_adb(command)

    # 将电脑文件拷贝到手机里面
    def push(self, local, remote):
        """
        从电脑上拷贝文件到手机里 adb push D:\file.txt /system/temp/
        :param local: 电脑上的文件路径 例如：D:\file.txt
        :param remote: 上传至手机的路径 例如：/system/temp/
        :return:
        """
        try:
            logging.info('上传文件 '+local+' 到手机 '+remote)
            result = self.call_adb("push %s %s" % (local, remote))
            logging.debug("result = " + result)
            return result
        except Exception as e:
            logging.error('上传文件到手机失败')
            logging.error(e)
            raise

    # 拉数据到本地
    def pull(self, remote, local):
        """
        下载手机数据到本地 adb pull /system/temp/ D:\file.txt
        :param remote: 手机上的数据地址 例如：/system/temp/
        :param local:  下载在电脑上的文件路径 例如：D:\file.txt
        :return:
        """
        try:
            logging.info('下载文件 ' + remote + ' 到本地 ' + local)
            result = self.call_adb("pull %s %s" % (remote, local))
            logging.debug("result = "+result)
            return result
        except Exception as e:
            logging.error('下载文件到PC失败')
            logging.error(e)
            raise

    # 同步更新 很少用此命名
    def sync(self, directory, **kwargs):
        command = "sync %s" % directory
        if 'list' in kwargs:
            command += " -l"
            result = self.call_adb(command)
            return result

    # 打开指定app
    def open_app(self, package_name, activity, devices):
        """
        打开指定的App  adb -s 设备的唯一标识（devices） shell am start -n 包名（package_name） activity
        :param package_name: 被测应用包名
        :param activity: 被测应用activity
        :param devices: 被测设备唯一标识
        :return:
        """
        try:
            logging.info('打开指定App')
            result = self.call_adb("-s " + devices+" shell am start -n %s/%s" % (package_name, activity))
            check = result.partition('\n')[2].replace('\n', '').split('\t ')
            logging.debug(check)
            logging.debug("check[0].find('Error') = "+str(check[0].find('Error')))
            if check[0].find("Error") >= 1:
                return False
            else:
                return True
        except Exception as e:
            logging.error('打开app失败')
            logging.error(e)
            raise

    # 根据包名得到进程id
    def get_app_pid(self, pkg_name):
        """
        根据包名获取运行时进程中的Pid     adb shell ps | grep 包名（pkg_name）
        :param pkg_name: 被测应用包名
        :return:
        """
        try:
            logging.info('根据包名得到进程id')
            string = self.call_adb("shell ps | grep "+pkg_name)
            if string == '':
                logging.error("the process doesn't exist.")
                return "the process doesn't exist."
            logging.debug("string = "+string)
            result = string.split(" ")
            logging.debug(result)
            logging.debug("result[4] = "+result[4])
            return result[4]
        except Exception as e:
            logging.error('根据包名获取进程PID失败')
            logging.error(e)
            raise


# if __name__ == '__main__':
#     logging.basicConfig(level=logging.DEBUG,
#                         format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                         datefmt='%a, %d %b %Y %H:%M:%S',
#                         filemode='w')
#     reuslt = AndroidDebugBridge().attached_devices()
#     for info in reuslt:
#         print(info)
