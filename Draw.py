import traceback
import pandas as pd
from Common import Common
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']


class Draw(Common):
    def __init__(self):
        super(Draw, self).__init__()
        self.com = Common()

    # 绘制cpu折线图
    def cpu_line_chart(self, excel):
        if excel:
            i = 0
            excelList = []
            lineLabel = []
            for e in excel:
                excelList.append(pd.read_excel(e))
                s = re.findall("\S+/(\w+)_Report", e)
                if s:
                    lineLabel.append(s.pop())
                else:
                    lineLabel.append("性能数据")
            for data in excelList:
                try:
                    x = range(len(data))
                    y = data['CPU(%)']
                except Exception:
                    self.com.writeLog().info(traceback.format_exc())
                else:
                    # plt.plot(x[::10], y[::10], label=lineLabel[i])
                    plt.plot(x, y, label=lineLabel[i])
                    i += 1

            ylabel = "CPU(%)"
            chart_title = "CPU趋势"
            plt.legend()  # 让图例生效
            plt.ylabel(ylabel)  # Y轴标签
            plt.title(chart_title)  # 标题

            plt.grid(axis="y")
            plt.xticks(rotation=30)
            plt.show()
            plt.close()

    # 绘制内存折线图
    def mem_line_chart(self, excel):
        if excel:
            i = 0
            excelList = []
            lineLabel = []
            for e in excel:
                excelList.append(pd.read_excel(e))
                s = re.findall("\S+/(\w+)_Report", e)
                if s:
                    lineLabel.append(s.pop())
                else:
                    lineLabel.append("性能数据")
            for data in excelList:
                try:
                    x = range(len(data))
                    y = data['MEM(M)']
                except Exception:
                    self.com.writeLog().info(traceback.format_exc())
                else:
                    # plt.plot(x[::10], y[::10], label=lineLabel[i])
                    plt.plot(x, y, label=lineLabel[i])
                    i += 1

            ylabel = "PSS(Mb)"
            chart_title = "PSS趋势"
            plt.legend()  # 让图例生效
            plt.ylabel(ylabel)  # Y轴标签
            plt.title(chart_title)  # 标题

            plt.grid(axis="y")
            plt.xticks(rotation=30)
            plt.show()
            plt.close()

    # 绘制fps折线图
    def fps_line_chart(self, excel):
        if excel:
            i = 0
            excelList = []
            lineLabel = []
            for e in excel:
                excelList.append(pd.read_excel(e))
                s = re.findall("\S+/(\w+)_Report", e)
                if s:
                    lineLabel.append(s.pop())
                else:
                    lineLabel.append("性能数据")
            for data in excelList:
                try:
                    x = range(len(data))
                    y = data['FPS']
                except Exception:
                    self.com.writeLog().info(traceback.format_exc())
                else:
                    # plt.plot(x[::10], y[::10], label=lineLabel[i])
                    plt.plot(x, y, label=lineLabel[i])
                    i += 1

            ylabel = "FPS"
            chart_title = "FPS趋势"
            plt.legend()  # 让图例生效
            plt.ylabel(ylabel)  # Y轴标签
            plt.title(chart_title)  # 标题

            plt.grid(axis="y")
            plt.xticks(rotation=30)
            plt.show()
            plt.close()

    # 绘制drawcall折线图
    def drawcall_line_chart(self, excel):
        if excel:
            i = 0
            excelList = []
            lineLabel = []
            for e in excel:
                excelList.append(pd.read_excel(e))
                s = re.findall("\S+/(\w+)_Report", e)
                if s:
                    lineLabel.append(s.pop())
                else:
                    lineLabel.append("性能数据")
            for data in excelList:
                try:
                    x = range(len(data))
                    y = data['Drawcall']
                except Exception:
                    self.com.writeLog().info(traceback.format_exc())
                else:
                    # plt.plot(x[::10], y[::10], label=lineLabel[i])
                    plt.plot(x, y, label=lineLabel[i])
                    i += 1

            ylabel = "Drawcall"
            chart_title = "Drawcall趋势"
            plt.legend()  # 让图例生效
            plt.ylabel(ylabel)  # Y轴标签
            plt.title(chart_title)  # 标题

            plt.grid(axis="y")
            plt.xticks(rotation=30)
            plt.show()
            plt.close()



if __name__ == '__main__':
    excel = u"D:/PerfReport/三星note3_单人_Report_2020-05-13_15-41-20_性能数据.xls"
    excel2 = u"D:/PerfReport/三星note3_多人多怪_Report_2020-05-13_16-07-58_性能数据.xls"
    dr = Draw()
    dr.cpu_line_chart(excel)
    dr.mem_line_chart(excel2)
