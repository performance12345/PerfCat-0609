import time
import traceback
from time import sleep
from PyQt5.QtCore import *
from Common import Common


class TempeThread(QThread, Common):

    trigger = pyqtSignal(int, bool)

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
            durtime = self.durtime.replace("min", "")
            interval = self.interval.replace("s", "")
            durtime = int(durtime)*60
            interval = int(interval)
            n = int(durtime / interval)

            for i in range(n):
                sleep_interval = 0.001
                start_time = time.time()
                if self.check_adb(self.package) == 1:
                    if self.check_adb(self.package) == 1:
                        # cmd_fps = "adb shell service call SurfaceFlinger 1013"
                        cmd = self.com.adb + " shell \"cat /sys/class/thermal/thermal_zone7/temp\""
                        res = self.execshell(cmd)
                        if res.poll() is None:
                            line = res.stdout.readline().decode('utf-8', 'ignore')
                            if 'Permission' not in line and 'No such file or directory' not in line:
                                line = line[0:2]
                                line = int(line)

                                self.lock['temp'].acquire()
                                self.trigger.emit(line, self.btn_enable)
                                row += 1
                                self.sheet.write(row, 14, line)
                                # print("temp %d" % row)
                                self.lock['net'].release()
                            else:
                                self.lock['temp'].acquire()
                                self.trigger.emit("null", self.btn_enable)
                                row += 1
                                self.sheet.write(row, 14, "null")
                                # print("temp %d" % row)
                                self.lock['net'].release()
                        # print("net release %d" % (self.lock['net'].available()))

                        while (time.time()-start_time)*1000000 <= interval * 1000000:
                            sleep_interval += 0.0000001
                            sleep(sleep_interval)
                        end_time = time.time()
                        # avg = (end_time-start_time)*1000
                        # print("Temp为%f" % avg)

            print("temp over")
            self.btn_enable = True
            self.trigger.emit(0, self.btn_enable)
            # self.workbook.save(self.excel)
        except Exception:
            self.com.writeLog().info(traceback.format_exc())

