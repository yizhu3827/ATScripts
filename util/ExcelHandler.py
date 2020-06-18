import xlrd
from conf import settings
class ExcelHandler(object):
    # Excel功能：
    def __init__(self, excel_file_path=None):
        self.excel_file_path = excel_file_path
    def get_excel_data(self, excel_file_path):
        # 读取Excel表格：
        book = xlrd.open_workbook(excel_file_path)
        # 根据sheet名称获取sheet对象：
        sheet = book.sheet_by_name('自动化测试')
        # 获取标题：
        title = sheet.row_values(0)
        # l = []
        # 方式一循环添加返回列表：
        # for row in range(1, sheet.nrows):
        #     l.append(dict(zip(title, sheet.row_values(row))))
        # return l
        # 方式二列表解析式返回：
        return [dict(zip(title, sheet.row_values(row))) for row in range(1, sheet.nrows)]
    def write_excel(self):
        # 写入Excel表格：
        pass
if __name__ == '__main__':
    ExcelHandler().get_excel_data(settings.EXCEL_FILE_PATH)