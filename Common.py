import logging
import re
import subprocess
import os
import traceback

import pandas as pd
import xlrd
import xlwt
from xlutils.copy import copy
import copy


class Common():

    def __init__(self):

        self.title = [u"COUNT", u"CPU(%)", u"MEM(M)"]
        self.data = []
        self.lock = ['cpu']
        self.adb = "adb" #adb执行程序的路径

    # 捕捉异常并写入到日志
    def writeLog(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(level=logging.INFO)
        handler = logging.FileHandler("D:\Perfcat_Log.txt")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('######%(asctime)s###### - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    # 获得锁标识
    def getLock(self, t):
        return self.lock[0]

    # 读取excel表格
    def read_excel(self, excel_path):
        return pd.read_excel(excel_path)

    # 将传入的字符串按照指定规定的正则匹配提取字符串
    def format_by_re(self, pattern, line):
        str = re.findall(pattern, line)
        return str

    # 执行系统命令
    def execshell(self, cmd):
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return res

    # 获取当前运行app包名
    def get_current_package(self):
        cmd_find = "adb shell dumpsys window | findstr mCurrentFocus"
        res = self.execshell(cmd_find)
        if res.poll() is not None:
            print("END")
        if res.poll() is None:
            line = res.stdout.readline()
            line = line.decode('utf-8', 'ignore')
        return line

    # 判断app是否启动
    def app_isRunning(self, app):
        cmd = "adb shell ps | findstr \"" + app + "\""
        res = self.execshell(cmd)
        if res.poll() is not None:
            print("END")
            return 0
        if res.poll() is None:
            line = res.stdout.readline()
            line = line.decode('utf-8', 'ignore')
            if line == "":
                return 2
            elif 'no devices' in line:
                return 0
            else:
                return 1

    # 检测adb是否连接成功
    def check_adb(self, package):
        try:
            status = 0
            app = self.get_package(package)
            cmd = self.adb+" shell \"ps | grep \"" + app + "\"\""
            res = self.execshell(cmd)

            while res.poll() is None:
                line = res.stdout.readline().decode('utf-8', 'ignore')
                if 'no devices' in line or 'error' in line:
                    status = 0
                    return status
                isRun = re.findall('cn\.(\S+)', line)
                if isRun:
                    isRun = "cn." + isRun.pop()
                    if app == isRun:
                        status = 1
                        return status
                else:
                    status = 2
            return status
        except Exception:
            self.com.writeLog().info(traceback.format_exc())

    # #返回检测设备文字提示
    # def check_adb_text(self):
    #     status = self.check_adb()
    #     res = ""
    #     if status == 0:
    #         res = "ADB未连接，请连接ADB"
    #     # elif status == 1:
    #     #     res = "JJ已启动"
    #     elif status == 2:
    #         res = "JJ未启动，请启动JJ比赛或JJ斗地主"
    #     return res


    # 获取传入的excel的文件名称
    def get_excel_name(self, excel):
        index = excel.rindex('.')
        name = excel[0:index]
        return name

    # 创建excel表格
    def create_excel(self, excel):
        self.workbook = xlwt.Workbook()
        self.sheet = self.workbook.add_sheet('report', cell_overwrite_ok=True)

        for i in range(0, len(self.title)):
            self.sheet.write(0, i, self.title[i])
        self.workbook.save(excel)

    # 向指定excel表格指定列中追加数据，参数为list
    def write_excel(self, col, excel, data):
        row = 1
        res = self.check_excel(excel)
        if res == 0:
            self.create_excel(excel)
        else:
            self.workbook = xlrd.open_workbook(excel)
            wb = copy(self.workbook)
            writeSheet = wb.get_sheet(0)
            for i in range(len(data)):
                writeSheet.write(row, 0, i)
                writeSheet.write(row, col, data[i])
                row = row + 1
            wb.save(excel)

    # 向指定excel表格指定列中追加数据,传入参数为字符串
    def write_excel_bystr(self, row, col, excel, line):
        try:
            res = self.check_excel(excel)
            if res == 0:
                self.create_excel(excel)
            else:
                self.workbook = self.create_excel(excel)
                self.workbook = xlrd.open_workbook(excel)
                wb = copy(self.workbook)
                writeSheet = wb.get_sheet(0)
                writeSheet.write(row, 0, row)
                writeSheet.write(row, col, line)
                wb.save(excel)
        except Exception:
            self.com.writeLog().info(traceback.format_exc())


    # 对传入的excel表进行校验，验证是否存在
    def check_excel(self, excel):
        res = os.path.exists(excel)
        return res

    # 选择测试包
    def get_package(self, package):
        if 'JJ比赛' in package:
            return 'cn.jj.hall'
        elif 'JJ斗地主' in package:
            return 'cn.jj'
        elif 'JJ欢乐斗地主' in package:
            return 'cn.jj.lordhl'
        elif '单机斗地主' in package:
            return 'com.philzhu.www.ddz'
        elif 'JJ捕鱼' in package:
            return 'cn.jj.fish'
        elif 'JJ麻将' in package:
            return 'cn.jj.mahjong'
        elif 'JJ象棋' in package:
            return 'cn.jj.chess'

    # 创建文件夹
    def mkdir(self, path):
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            # print(path + ' 创建成功')
            return True
        else:
            # print(path + ' 目录已存在')
            return False

    # 获取命令行执行结果
    def get_cmd_res(self, cmd):
        res = self.execshell(cmd)
        cmd_res = []
        while res.poll() is None:
            line = res.stdout.readline()
            line = line.decode('utf-8', 'ignore')
            if line != '':
                cmd_res.append(line)
        return cmd_res

    # 展示APP信息
    def app_data(self):
        cmd_res = {'android_version':'', 'phone_version':'', 'mem_total':''}
        cmd_android_version = self.adb + " shell getprop ro.build.version.release"
        cmd_phone_model = self.adb + " -d shell getprop ro.product.model"
        cmd_mem_info = self.adb + " shell cat /proc/meminfo "
        cmd_res['android_version'] = self.get_cmd_res(cmd_android_version).pop()
        cmd_res['phone_model'] = self.get_cmd_res(cmd_phone_model).pop()
        cmd_res['mem_total'] = self.get_cmd_res(cmd_mem_info).pop(0)
        return cmd_res
