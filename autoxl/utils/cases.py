import openpyxl
from . import utils


class BaseOneFileCabinet:

    def __init__(self, file, bonus_count):
        self.bonus_count = bonus_count
        self.work_book = openpyxl.load_workbook(file)
        self.first_sheet = self.work_book.get_sheet_names()[0]
        self.work_sheet = self.work_book.get_sheet_by_name(self.first_sheet)
        self.data = self.get_managers_data()

    def get_managers_data(self):
        iteration = 0
        free_cell = 0
        managers_data = []
        manager = []
        manager_data = []
        new_phone_number = True
        new_manager_name = True
        while free_cell < 2:
            iteration += 1
            cell_A = self.work_sheet[f'A{iteration}'].value
            cell_B = self.work_sheet[f'B{iteration}'].value
            cell_C = self.work_sheet[f'C{iteration}'].value
            if cell_A:
                free_cell = 0
                if new_phone_number:
                    manager.append(cell_A)
                    new_phone_number = False
                    continue
                if not new_phone_number and new_manager_name:
                    manager.append(cell_A)
                    new_manager_name = False
                    continue
                else:
                    manager_data.append([cell_A, cell_B, cell_C])
                    continue
            else:
                manager.append(manager_data)
                managers_data.append(manager)
                manager = []
                manager_data = []
                new_phone_number = True
                new_manager_name = True
                free_cell += 1
                continue
        return managers_data


class BaseBugBonus(BaseOneFileCabinet):

    def __init__(self, file, bonus_count):
        super().__init__(file, bonus_count)
        self.work_report = self.get_work_report()
        # cabinet_report = get_cabinet_report()

    def get_work_report(self):
        work_book = openpyxl.Workbook()
        work_sheet = work_book.active
        work_sheet['B1'] = 'Номенклатурный код'
        work_sheet['C1'] = 'Тоннаж'
        work_sheet['D1'] = 'Вес единицы продукта'
        work_sheet['E1'] = 'Количество мешков'
        work_sheet['F1'] = 'Бонус за 1 мешок'
        work_sheet['G1'] = 'Сумма бонуса'
        iteration = 1

        for manager in self.data:
            iteration += 1
            telephone_number = manager[0]
            if not telephone_number:
                break
            work_sheet[f'A{iteration}'] = telephone_number
            iteration += 1
            manager_name = manager[1]
            work_sheet[f'A{iteration}'] = manager_name
            iteration += 1

            for manager_data in manager[2]:

                nomenclature = manager_data[0]
                nomenclature_code = manager_data[1]
                tons = float(manager_data[2])
                product_mass = utils.get_product_mass(nomenclature)

                work_sheet[f'A{iteration}'] = nomenclature
                work_sheet[f'B{iteration}'] = nomenclature_code
                work_sheet[f'C{iteration}'] = tons
                work_sheet[f'D{iteration}'] = product_mass
                work_sheet[f'E{iteration}'] = tons * 1000 / product_mass
                work_sheet[f'F{iteration}'] = self.bonus_count
                work_sheet[f'G{iteration}'] = tons * 1000 / product_mass * self.bonus_count

                iteration += 1
        return work_book


'''
Кейсы для utils
'''


class CaseCabinetTonsBagbonus(BaseBugBonus):
    pass
