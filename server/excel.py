from datetime import datetime
from config import Configuration
from xlsxwriter.workbook import Workbook


config_path = './config.ini'


class Excel():
    def __init__(self):
        self.config = Configuration()
        self.config.load(config_path)
        self.path = self.config.get('excel', 'path')

    def export_to_excel(self, query):
        now = datetime.now()
        bottles = Workbook(f'{self.path}bottles_{now.strftime("%m_%d_%Y_%H-%M")}.xlsx')
        worksheet = bottles.add_worksheet()
        for i, row in enumerate(query):
            for j, value in enumerate(row):
                worksheet.write(i, j, value)
        bottles.close()
        return 'ok'