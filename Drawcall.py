import re
import time
import traceback
from time import sleep
from PyQt5.QtCore import *
from Common import Common


class DrawcallThread(QThread, Common):

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

                    # cmd_fps = "adb shell service call SurfaceFlinger 1013"
                    cmd = self.com.adb + " shell \"cat /sdcard/jjlog_fps.log\""
                    res = self.execshell(cmd)
                    if res.poll() is None:
                        line = res.stdout.readline().decode('utf-8', 'ignore')
                        # line = str(res.stdout.readline())
                        if 'No such file or directory' in line:
                            self.lock['drawcall'].acquire()
                            self.trigger.emit(0, self.btn_enable)
                            row += 1
                            self.sheet.write(row, 15, "NULL")
                            self.workbook.save(self.excel)
                            self.lock['time'].release()
                            # print("time release %d" % (self.lock['time'].available()))
                        else:
                            line = re.findall('Draw\scall\s\:\s(\d+)', line)
                            if line:
                                line = line.pop()
                                line = int(line)
                                self.lock['drawcall'].acquire()
                                self.trigger.emit(line, self.btn_enable)
                                row += 1
                                self.sheet.write(row, 15, line)
                                self.workbook.save(self.excel)
                                self.lock['time'].release()
                                # print("time release %d" % (self.lock['time'].available()))

                    while (time.time()-start_time)*1000000 <= interval * 1000000:
                        sleep_interval += 0.0000001
                        sleep(sleep_interval)
                    end_time = time.time()
                    # avg = (end_time-start_time)*1000
                    # print("Drawcall为%f" % avg)
            # print("drawcall over")
            self.btn_enable = True
            self.trigger.emit(0, self.btn_enable)
            self.workbook.save(self.excel)
        except Exception:
            self.com.writeLog().info(traceback.format_exc())