import os
import datetime
import openpyxl
from django.http import HttpResponse
from django.utils.http import urlquote


class ExcelGenerator:
    def __init__(self, data_list, header_dict):
        self.data_list = data_list
        self.header_dict = header_dict

    def generate_excel(self, filename):
        # 创建目录
        directory = os.path.dirname(filename)
        os.makedirs(directory, exist_ok=True)

        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # 写入表头
        header_row = []
        for header_key in self.header_dict.keys():
            header_row.append(self.header_dict[header_key])
        sheet.append(header_row)

        # 写入数据
        for data_dict in self.data_list:
            data_row = []
            for header_key in self.header_dict.keys():
                search_key = data_dict.get(header_key)
                if search_key is not None:
                    data_row.append(search_key)
                else:
                    data_row.append("")  # 缺失数据的占位符
            sheet.append(data_row)

        # 保存工作簿
        workbook.save(filename)
        return filename

    def generate_excel_response(self, filename):
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # 写入表头
        header_row = []
        for header_key, header_value in self.header_dict.items():
            if isinstance(header_value, tuple):
                header_row.append(header_value[0])
            else:
                header_row.append(header_value)
        sheet.append(header_row)

        # 写入数据
        for data_dict in self.data_list:
            data_row = []
            for header_key, header_value in self.header_dict.items():
                search_key = data_dict.get(header_key)
                if isinstance(header_value, tuple):
                    value_func = header_value[1]
                    if value_func is not None:
                        data_row.append(value_func(data_dict))
                    else:
                        data_row.append(search_key if search_key is not None else "")
                else:
                    data_row.append(search_key if search_key is not None else "")
            sheet.append(data_row)

        # 创建一个 HttpResponse 对象，将生成的 Excel 文件作为响应返回
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{urlquote(filename)}"'
        # 将工作簿内容写入 HttpResponse 流
        workbook.save(response)

        return response

# Example usage
# data = [
#     {"Name": "Alice", "Age": 25, "Country": "USA"},
#     {"Name": "Bob", "Age": 30, "Country": "Canada"},
#     {"Name": "Charlie", "Age": 28, "Country": "UK"}
# ]
#
# header = {
#     "Name": "姓名",
#     "Age": "年龄",
#     "Country": "国家"
# }
#
# excel_generator = ExcelGenerator(data, header)
# excel_generator.generate_excel("output.xlsx")
