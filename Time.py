import re
import time
import traceback
from PyQt5.QtCore import *
from Common import Common


class TimeThread(QThread, Common):

    trigger = pyqtSignal(str)

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
            durtime = self.durtime.replace("min", "")
            interval = self.interval.replace("s", "")
            durtime = int(durtime) * 60
            interval = int(interval)
            n = int(durtime / interval)
            name = self.get_package(self.package)

            for i in range(n):
                start_time = time.time()
                sleep_interval = 0.001

                durtime -= interval
                min = int(durtime / 60)
                sec = (durtime % 60)
                timeCount = str(min) + ":" + str(sec)

                self.lock['time'].acquire()
                self.trigger.emit(timeCount)
                self.lock['fps'].release()
                # print("fps release %d" % (self.lock['fps'].available()))

                while (time.time() - start_time) * 1000000 <= interval * 1000000:
                    sleep_interval += 0.0000001
                    time.sleep(sleep_interval)
                end_time = time.time()
                # avg = (end_time - start_time) * 1000
                # print("内存为%f" % avg)

            # print("time over")
            self.trigger.emit("0")
            # self.workbook.save(self.excel)
        except Exception:
            self.com.writeLog().info(traceback.format_exc())


