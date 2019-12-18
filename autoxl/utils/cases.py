import openpyxl


class BaseOneFileCase:

    def __init__(self, file, bonus_count):
        self.work_book = openpyxl.load_workbook(file)
        self.bonus_count = bonus_count
        self.first_sheet = self.work_book.get_sheet_names()[0]
        self.work_sheet = self.work_book.get_sheet_by_name(self.first_sheet)


class CaseCabinet007TonsBagbonus(BaseOneFileCase):
    pass
