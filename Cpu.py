import re
import time
import traceback
from PyQt5.QtCore import *
from Common import Common


class CpuThread(QThread, Common):

    trigger = pyqtSignal(str, bool)

    def __init__(self, excel, sheet, workbook, interval, durtime, package, lock):
        super(QThread, self).__init__()
        self.excel = excel
        self.interval = interval
        self.durtime = durtime
        self.package = package
        self.sheet = sheet
        self.workbook = workbook
        self.btn_enable = False
        self.lock = lock
        self.com = Common()

    def run(self):
        try:
            row = 0
            count = 0
            durtime = self.durtime.replace("min", "")
            interval = self.interval.replace("s", "")
            durtime = int(durtime)*60
            interval = int(interval)
            interval_time = interval
            n = int(durtime / interval)
            n = str(n)
            cpuCore = 1

            name = self.get_package(self.package)
            interval = str(interval)
            # cmd_cpu = self.com.adb + " shell \"top -n " + n + " -d " + interval + " | grep \"" + name + "\"\""
            cmd_cpu = self.com.adb + " shell top -n " + n + " -d " + interval + " | find \"" + name + "\""
            # self.execshell("adb shell")
            # cmd_cpu = "top -n " + n + " -d " + interval + " | find \"" + name + "\""

            if self.check_adb(self.package) == 1:
                phoneInfo = self.com.app_data()
                phoneModel = phoneInfo['phone_model']

                # 兼容三星A9机型
                if 'OPPO-R9' in phoneModel:
                    # cmd_cpu = self.com.adb + " shell top -n " + n + " -d " + interval + " | find \"" + name + "\""
                    cmd_cpu = self.com.adb + " shell \"top -n " + n + " -d " + interval + " | grep \"" + name + "\"\""

                cpuInfo_res = self.execshell(self.com.adb + " shell \"cat /proc/cpuinfo\"")
                #获取cpu核数
                while cpuInfo_res.poll() is None:
                    cpuInfo = cpuInfo_res.stdout.readline().decode('utf-8', 'ignore')
                    if "cpu cores" in cpuInfo:
                        cpuCore = int(re.findall("cpu cores\\t\:\s(\S*)", cpuInfo).pop())
                    elif "CPU architecture" in cpuInfo:
                        cpuCore = int(re.findall("CPU architecture:\s(\d)", cpuInfo).pop())

                res = self.execshell(cmd_cpu)
                while res.poll() is None:
                    start_time = time.time()
                    sleep_interval = 0.001
                    line = res.stdout.readline().decode('utf-8', 'ignore')

                    cpuRes = re.findall('cn\.(\S+)', line)
                    if cpuRes:
                        cpuRes = "cn." + cpuRes.pop()

                    if name == cpuRes:
                        if line != "":
                            cpu = self.format_by_re('(\d+)\%', line)
                            if len(cpu) == 0:
                                cpu = re.split('\s+', line)
                                if cpu[0] == "":
                                    cpu = float(cpu[9])
                                else:
                                    cpu = float(cpu[8])
                                cpu = cpu/cpuCore
                                cpu = str(round(cpu, 1))
                            else:
                                cpu = cpu.pop()

                            self.lock['cpu'].acquire()
                            self.trigger.emit(cpu, self.btn_enable)
                            count += 1
                            row += 1
                            self.sheet.write(row, 0, count)
                            self.sheet.write(row, 1, float(cpu))
                            # print("#####cpu %d#####" %row)
                            self.lock['battery'].release()
                            # print("battery release %d" % (self.lock['battery'].available()))

                            while (time.time() - start_time) * 1000000 <= interval_time * 1000000:
                                sleep_interval += 0.0000001
                                time.sleep(sleep_interval)
                            # end_time = time.time()
                            # print("#####cpu为%f######" % (end_time * 1000 - start_time * 1000))

                # print("cpu over")
                self.btn_enable = True
                self.trigger.emit('0', self.btn_enable)
                self.workbook.save(self.excel)
        except Exception:
            self.com.writeLog().info(traceback.format_exc())



