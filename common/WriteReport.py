import logging
import xlsxwriter

from common import Path
from common.Pickle import read_info
from common.Report import OperateReport


def report(info, devices):
    try:
        logging.info('初始化测试报告')
        workbook = xlsxwriter.Workbook(Path.report_path()+''.join(devices.split(':'))+'报告.xlsx')
        bo = OperateReport(workbook)
        logging.info('生成监控报告')
        bo.monitor(info)
        logging.info('生成错误日志')
        bo.crash()
        logging.info('生成详细报告')
        bo.analysis(info)
        bo.close()
        logging.info('报告生成成功')
    except Exception as e:
        logging.error('生成测试报告失败')
        logging.error(e)
        raise


# report(read_info('H:\\project\Monkey-Monitor\\info\\info.pickle'))
