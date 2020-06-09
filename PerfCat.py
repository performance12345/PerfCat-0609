import sys
import time
import traceback
from queue import Queue
import xlrd
import xlwt
from PyQt5 import QtWidgets
from PyQt5.QtCore import QMutex, QMutexLocker, QSemaphore
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import *
from xlutils.copy import copy
import re
from Battery import BatteryThread
from Cpu import CpuThread
from Drawcall import DrawcallThread
from Mem import MemThread
from Common import Common
from Fps import FpsThread
from Net import NetThread
from Temperature import TempeThread
from Draw import Draw
from Time import TimeThread


class MyWindow(QWidget):

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.init_Ui()
        self.com = Common()
        self.title = [
            u"COUNT", u"CPU(%)", u"MEM(M)", u"FPS",
            u"Wifi下行(KB/S)", u"Wifi上行(KB/S)", u"下载流量(MB)", u"上传流量(MB)", u"Wifi总流量(MB)",
            u"移动网络下行(KB/S)", u"移动网络上行(KB/S)", u"下载流量(MB)", u"上传流量(MB)", u"移动网络总流量(MB)",
            u"温度", "Drawcall", u"电量"
        ]
        self.excel_path = "D:\PerfReport"
        # self.create_excel()
        self.getData = 0

        BufferSize = 1 #同时并发的线程数
        FpsS = QSemaphore(BufferSize)  # cpu并发锁
        CpuS = QSemaphore(0)
        DrawcallS = QSemaphore(0)
        NetS = QSemaphore(0)
        MemS = QSemaphore(0)
        TempS = QSemaphore(0)
        BatteryS = QSemaphore(0)
        TimeS = QSemaphore(0)
        self.lock = {} #并发锁词典
        self.lock['cpu'] = CpuS
        self.lock['fps'] = FpsS
        self.lock['drawcall'] = DrawcallS
        self.lock['net'] = NetS
        self.lock['mem'] = MemS
        self.lock['temp'] = TempS
        self.lock['battery'] = BatteryS
        self.lock['time'] = TimeS
        self.dw = Draw()
        self.isCollect = 0

    def init_Ui(self):
        self.setWindowTitle('性能测试自动化工具')
        self.resize(450, 170)

        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.excel_name = QLineEdit(self.centralwidget)
        self.excel_name.setObjectName("excel_name")
        self.excel_name.setEnabled(False)
        self.gridLayout.addWidget(self.excel_name, 0, 1, 1, 1)

        self.check_device = QPushButton(self.centralwidget)
        self.check_device.setObjectName("check_device")
        self.check_device.clicked.connect(self.check_device_fun)
        self.gridLayout.addWidget(self.check_device, 1, 2, 1, 1)

        self.open_dir = QPushButton(self.centralwidget)
        self.open_dir.setObjectName("open_dir")
        self.open_dir.clicked.connect(self.open_dir_fun)
        self.gridLayout.addWidget(self.open_dir, 0, 2, 1, 1)

        self.drawBtn = QPushButton(self.centralwidget)
        self.drawBtn.setObjectName("drawBtn")
        self.drawBtn.clicked.connect(self.draw)
        self.gridLayout.addWidget(self.drawBtn, 2, 2, 1, 1)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)

        self.test_package = QComboBox(self.centralwidget)
        self.test_package.setObjectName("test_package")
        self.test_package.addItem("")
        self.test_package.addItem("")
        self.test_package.addItem("")
        self.test_package.addItem("")
        self.test_package.addItem("")
        self.test_package.addItem("")
        self.test_package.addItem("")
        self.gridLayout.addWidget(self.test_package, 1, 1, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.interval_time = QComboBox(self.centralwidget)
        self.interval_time.setObjectName("interval_time")
        self.interval_time.addItem("")
        self.interval_time.addItem("")
        self.interval_time.addItem("")
        self.interval_time.addItem("")
        self.gridLayout.addWidget(self.interval_time, 2, 1, 1, 1)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.during_time = QComboBox(self.centralwidget)
        self.during_time.setObjectName("during_time")
        self.during_time.addItem("")
        self.during_time.addItem("")
        self.during_time.addItem("")
        self.during_time.addItem("")

        self.timer = QtWidgets.QLabel(self.centralwidget)
        self.timer.setText("")
        self.timer.setObjectName("timer")

        self.gridLayout.addWidget(self.during_time, 3, 1, 1, 1)
        self.gridLayout.addWidget(self.timer, 3, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.get_cpu = QPushButton(self.centralwidget)
        self.get_cpu.setObjectName("get_cpu")
        self.horizontalLayout.addWidget(self.get_cpu)
        self.get_cpu.clicked.connect(self.get_cpu_fun)

        self.stop_collect = QPushButton(self.centralwidget)
        self.stop_collect.setObjectName("stop_collect")
        self.horizontalLayout.addWidget(self.stop_collect)
        self.stop_collect.clicked.connect(self.stop_collect_fun)

        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_cpu = QtWidgets.QLabel(self.centralwidget)
        self.label_cpu.setObjectName("label_cpu")
        self.horizontalLayout_2.addWidget(self.label_cpu)
        self.cpu_data = QtWidgets.QLabel(self.centralwidget)
        self.cpu_data.setText("")
        self.cpu_data.setObjectName("cpu")
        self.horizontalLayout_2.addWidget(self.cpu_data)
        self.label_mem = QtWidgets.QLabel(self.centralwidget)
        self.label_mem.setObjectName("label_mem")
        self.horizontalLayout_2.addWidget(self.label_mem)
        self.mem_data = QtWidgets.QLabel(self.centralwidget)
        self.mem_data.setText("")
        self.mem_data.setObjectName("mem")
        self.horizontalLayout_2.addWidget(self.mem_data)
        self.label_fps = QtWidgets.QLabel(self.centralwidget)
        self.label_fps.setObjectName("label_fps")
        self.horizontalLayout_2.addWidget(self.label_fps)
        self.fps = QtWidgets.QLabel(self.centralwidget)
        self.fps.setText("")
        self.fps.setObjectName("fps")
        self.horizontalLayout_2.addWidget(self.fps)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_recieve = QtWidgets.QLabel(self.centralwidget)
        self.label_recieve.setObjectName("label_recieve")
        self.horizontalLayout_3.addWidget(self.label_recieve)
        self.recieve = QtWidgets.QLabel(self.centralwidget)
        self.recieve.setText("")
        self.recieve.setObjectName("recieve")
        self.horizontalLayout_3.addWidget(self.recieve)
        self.label_send = QtWidgets.QLabel(self.centralwidget)
        self.label_send.setObjectName("label_send")
        self.horizontalLayout_3.addWidget(self.label_send)
        self.send = QtWidgets.QLabel(self.centralwidget)
        self.send.setText("")
        self.send.setObjectName("send")
        self.horizontalLayout_3.addWidget(self.send)
        self.label_total = QtWidgets.QLabel(self.centralwidget)
        self.label_total.setObjectName("label_total")
        self.horizontalLayout_3.addWidget(self.label_total)
        self.total = QtWidgets.QLabel(self.centralwidget)
        self.total.setText("")
        self.total.setObjectName("total")
        self.horizontalLayout_3.addWidget(self.total)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 3, 0, 1, 1)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_drawcall = QtWidgets.QLabel(self.centralwidget)
        self.label_drawcall.setObjectName("label_drawcall")
        self.horizontalLayout_4.addWidget(self.label_drawcall)
        self.drawcall = QtWidgets.QLabel(self.centralwidget)
        self.drawcall.setText("")
        self.drawcall.setObjectName("drawcall")
        self.horizontalLayout_4.addWidget(self.drawcall)

        self.label_battery = QtWidgets.QLabel(self.centralwidget)
        self.label_battery.setObjectName("label_battery")
        self.horizontalLayout_4.addWidget(self.label_battery)
        self.battery = QtWidgets.QLabel(self.centralwidget)
        self.battery.setText("")
        self.battery.setObjectName("battery")
        self.horizontalLayout_4.addWidget(self.battery)

        self.label_tempe = QtWidgets.QLabel(self.centralwidget)
        self.label_tempe.setObjectName("label_tempe")
        self.horizontalLayout_4.addWidget(self.label_tempe)
        self.tempe = QtWidgets.QLabel(self.centralwidget)
        self.tempe.setText("")
        self.tempe.setObjectName("tempe")
        self.horizontalLayout_4.addWidget(self.tempe)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 4, 0, 1, 1)

        self.setLayout(self.gridLayout)
        self.setLayout(self.gridLayout_2)

        self.label.setText("存储的Excel文件名：")
        self.open_dir.setText("打开目录")
        self.excel_name.setPlaceholderText("默认存储到D盘PefReport目录")
        self.check_device.setText("检测设备")
        self.label_4.setText("选择测试包：")
        self.test_package.setItemText(0, "JJ斗地主")
        self.test_package.setItemText(1, "JJ比赛")
        self.test_package.setItemText(2, "JJ欢乐斗地主")
        self.test_package.setItemText(3, "单机斗地主")
        self.test_package.setItemText(4, "JJ捕鱼")
        self.test_package.setItemText(5, "JJ麻将")
        self.test_package.setItemText(6, "JJ象棋")
        self.label_2.setText("数据采集间隔：")
        self.interval_time.setItemText(0, "2s")
        self.interval_time.setItemText(1, "3s")
        self.interval_time.setItemText(2, "5s")
        self.interval_time.setItemText(3, "10s")
        self.label_3.setText("数据采集时长：")
        self.during_time.setItemText(0, "10min")
        self.during_time.setItemText(1, "30min")
        self.during_time.setItemText(2, "60min")
        self.during_time.setItemText(3, "90min")
        self.get_cpu.setText("开始采集数据")
        self.stop_collect.setText("停止采集数据")
        self.label_cpu.setText("实时CPU ：")
        self.label_mem.setText("实时内存：")
        self.label_fps.setText("实时FPS：")

        self.label_total.setText("总流量 ：")
        self.label_drawcall.setText("Drawcall：")
        self.label_send.setText("上行速度：")
        self.label_recieve.setText("下行速度：")
        self.label_tempe.setText("cpu温度：")
        self.label_battery.setText("实时电量：")
        self.drawBtn.setText("绘制折线图")


    # 打开存储文件夹
    def open_dir_fun(self):
        QFileDialog.getOpenFileNames(self, "打开...", self.excel_path, "All Files(*)")

    # 停止采集数据
    def stop_collect_fun(self):
        try:
            if self.isCollect:
                self.cpu_thread.terminate()
                self.fps_thread.terminate()
                self.drawcall_thread.terminate()
                self.mem_thread.terminate()
                self.tempe_thread.terminate()
                self.net_thread.terminate()
                self.battery_thread.terminate()
                self.time_thread.terminate()

                self.cpu_data.setText("")
                self.mem_data.setText("")
                self.fps.setText("")
                self.send.setText("")
                self.recieve.setText("")
                self.total.setText("")
                self.tempe.setText("")
                self.drawcall.setText("")
                self.battery.setText("")
                self.timer.setText("")

                self.get_cpu.setEnabled(True)
                self.stop_collect.setEnabled(False)
        except Exception:
            self.com.writeLog().info(traceback.format_exc())


    # 读取性能数据excel绘制数据分析图表
    def draw(self):
        try:
            file, type = QFileDialog.getOpenFileNames(self, "打开...", self.excel_path, "All Files(*)")
            self.dw.cpu_line_chart(file)
            self.dw.mem_line_chart(file)
            self.dw.fps_line_chart(file)
            self.dw.drawcall_line_chart(file)
        except Exception:
            self.com.writeLog().info(traceback.format_exc())

    # 使用QMessageBox提示
    def closeEvent(self, QCloseEvent):
        try:
            reply = QMessageBox.warning(self, "提示", "确认退出并保存数据到默认目录？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if (reply == QMessageBox.Yes):
                if self.getData:
                    self.wb.save(self.excel)
                QCloseEvent.accept()
            if (reply == QMessageBox.No):
                QCloseEvent.ignore()
        except Exception:
            self.com.writeLog().info(traceback.format_exc())

    # 创建excel表格，如已存在，默认插入该表格中，如无创建
    def create_excel(self):
        app_data = self.com.app_data()
        self.android_version = "安卓版本:" + app_data['android_version']
        self.phone_model = "手机型号：" + app_data['phone_model']
        self.mem_total = app_data['mem_total']
        self.book = self.excel_name.text()
        self.current_time = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
        self.excel = "D:\\PerfReport\\" + self.book + "_Report" + "_" + self.current_time + "_性能数据.xls"
        res = self.com.check_excel(self.excel)
        if res == 0:
            self.wb = xlwt.Workbook()
            self.writeSheet = self.wb.add_sheet('report', cell_overwrite_ok=True)
            self.writeSheet.write(0, 17, self.android_version + "__" + self.phone_model + "__" + self.mem_total)
            for i in range(0, len(self.title)):
                self.writeSheet.write(0, i, self.title[i])
            # self.wb.save(self.excel)
        else:
            self.workbook = xlrd.open_workbook(self.excel)
            self.wb = copy(self.workbook)
            self.writeSheet = self.wb.get_sheet(0)

    # 检测设备是否连接
    def check_device_fun(self):
        package = self.test_package.currentText()
        status = self.com.check_adb(package)
        if status == 0:
            res = "ADB连接异常，请连接ADB或者允许USB调试"
            self.show_msg(res)
            return status
        elif status == 1:
            if self.com.check_adb(package) == 1:
                self.show_msg('连接成功')
                app_data = self.com.app_data()
                self.android_version = "安卓版本:" + app_data['android_version']
                self.phone_model = "手机型号：" + app_data['phone_model']
                self.mem_total = app_data['mem_total']
                if self.mem_total is not None:
                    self.mem_total = int(re.findall('\d+', self.mem_total).pop()) / 1024 / 1024
                    self.mem_total = str(round(self.mem_total, 2))
                    self.mem_total = "手机内存：" + self.mem_total + "G"
                    self.show_msg(self.android_version + self.phone_model + self.mem_total)
                return status
        elif status == 2:
            res = "测试包启动异常，手机端运行APP与工具所选测试包不一致或手机端未启动运行测试包"
            self.show_msg(res)
            return status

    # 采集数据槽函数
    def get_cpu_fun(self):
        device = self.check_device_fun()
        self.interval = self.interval_time.currentText()
        self.durtime = self.during_time.currentText()
        self.package = self.test_package.currentText()

        if device == 1:
            self.create_excel()
            self.get_cpu.setEnabled(False)
            self.show_msg("采集性能数据")
            self.getData = 1
            path = "D:\\PerfReport"
            self.com.mkdir(path)

            self.cpu_thread = CpuThread(self.excel, self.writeSheet, self.wb, self.interval, self.durtime, self.package
                                        , self.lock)
            self.mem_thread = MemThread(self.excel, self.writeSheet, self.wb, self.interval, self.durtime, self.package
                                        , self.lock)
            self.fps_thread = FpsThread(self.excel, self.writeSheet, self.wb, self.interval, self.durtime, self.package
                                        , self.lock)
            self.net_thread = NetThread(self.excel, self.writeSheet, self.wb, self.interval, self.durtime, self.package
                                        , self.lock)
            self.tempe_thread = TempeThread(self.excel, self.writeSheet, self.wb, self.interval, self.durtime, self.package
                                        , self.lock)
            self.battery_thread = BatteryThread(self.excel, self.writeSheet, self.wb, self.interval, self.durtime, self.package
                                        , self.lock)
            self.drawcall_thread = DrawcallThread(self.excel, self.writeSheet, self.wb, self.interval, self.durtime, self.package
                                        , self.lock)
            self.time_thread = TimeThread(self.excel, self.writeSheet, self.wb, self.interval, self.durtime,
                                                  self.package, self.lock)

            self.mem_thread.trigger.connect(self.stop_get_mem)
            self.cpu_thread.trigger.connect(self.stop_get_cpu)
            self.fps_thread.trigger.connect(self.stop_get_fps)
            self.net_thread.trigger.connect(self.stop_get_net)
            self.tempe_thread.trigger.connect(self.stop_get_tempe)
            self.battery_thread.trigger.connect(self.stop_get_battery)
            self.drawcall_thread.trigger.connect(self.stop_get_drawcall)
            self.time_thread.trigger.connect(self.stop_get_time)

            QueThread = Queue()
            QueThread.put(self.cpu_thread)
            QueThread.put(self.fps_thread)
            QueThread.put(self.battery_thread)
            QueThread.put(self.mem_thread)
            QueThread.put(self.tempe_thread)
            QueThread.put(self.net_thread)
            QueThread.put(self.drawcall_thread)
            QueThread.put(self.time_thread)

            while not QueThread.empty():
                QueThread.get().start()
            self.isCollect = 1
            self.stop_collect.setEnabled(True)


    # 电量采集槽函数
    def stop_get_battery(self, int, bool):
        # print("电量采集")
        self.battery.setText(str(int))
        self.get_cpu.setEnabled(bool)

    # drawcall采集槽函数
    def stop_get_drawcall(self, int, bool):
        # print("drawcall采集")
        self.drawcall.setText(str(int))
        self.get_cpu.setEnabled(bool)

    # 终止温度采集槽函数
    def stop_get_tempe(self, int, bool):
        # print("温度采集")
        self.tempe.setText(str(int))
        self.get_cpu.setEnabled(bool)

    # 终止cpu采集槽函数
    def stop_get_cpu(self, str, bool):
        # print("cpu采集")
        self.cpu_data.setText(str)
        self.get_cpu.setEnabled(bool)

    # 内存采集槽函数
    def stop_get_mem(self, float, bool):
        # print("内存采集")
        self.mem_data.setText(str(float))
        self.get_cpu.setEnabled(bool)

    # fps采集槽函数
    def stop_get_fps(self, float, bool):
        # print("fps采集")
        self.fps.setText(str(float))

    # net采集槽函数
    def stop_get_net(self, list, bool):
        # print("流量采集")
        self.get_cpu.setEnabled(bool)
        self.recieve.setText(str(list[0]) + 'Kb/s')
        self.send.setText(str(list[1]) + 'Kb/s')
        self.total.setText(str(list[4]) + 'Mb')

    def stop_get_time(self, str):
        self.timer.setText(str)

    # 展示消息弹窗
    def show_msg(self, text):
        QMessageBox.information(self, "提示:", text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()
    sys.exit(app.exec_())
