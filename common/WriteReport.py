import os
import xlsxwriter

from common.Report import OperateReport

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def report(info):
    workbook = xlsxwriter.Workbook('报告.xlsx')
    bo = OperateReport(workbook)
    bo.monitor(info)
    bo.crash()
    bo.analysis(info)
    bo.close()
