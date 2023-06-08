import openpyxl
from openpyxl import Workbook

workbook = Workbook()
workbook.save(filename="data.xlsx")