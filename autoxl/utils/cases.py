import openpyxl
from . import utils


"""
ГЕНАРТОРЫ ДАННЫХ
"""


class BaseOneFileCabinet:


    def __init__(self, file, bonus_count):
        self.bonus_count = bonus_count
        self.work_book = openpyxl.load_workbook(file)
        self.work_sheet = self.work_book.get_sheet_by_name(self.work_book.get_sheet_names()[0])
        self.data = self.get_managers_data()


    def get_managers_data(self):
        iteration, free_cell = 0, 0
        managers_data, manager, manager_data = [], [], []
        new_phone_number, new_manager_name = True, True
        while free_cell < 2:
            iteration += 1
            cell_a = self.work_sheet[f'A{iteration}'].value
            cell_b = self.work_sheet[f'B{iteration}'].value
            cell_c = self.work_sheet[f'C{iteration}'].value
            if cell_a:
                free_cell = 0
                if new_phone_number:
                    manager.append(cell_a)
                    new_phone_number = False
                    continue
                if not new_phone_number and new_manager_name:
                    manager.append(cell_a)
                    new_manager_name = False
                    continue
                else:
                    manager_data.append([cell_a, cell_b, cell_c])
                    continue
            else:
                manager.append(manager_data)
                managers_data.append(manager)
                manager, manager_data = [], []
                new_phone_number, new_manager_name = True, True
                free_cell += 1
                continue
        return managers_data


"""
ОБРАБОТЧИКИ ДАННЫХ
"""


class BaseBugBonus(BaseOneFileCabinet):


    def __init__(self, file, bonus_count):
        super().__init__(file, bonus_count)
        self.report_file = openpyxl.Workbook()


    def get_cabinet_report(self):
        work_sheet = self.report_file.create_sheet('Отчет для сдачи', 1)
        iteration = 1

        for manager in self.data:
            total_tons_for_this_manager = 0
            if not self.set_telephone_and_name_in_cabinet_report(work_sheet, iteration, manager):
                break
            iteration += 2

            for manager_data in manager[2]:
                total_tons_for_this_manager += self.get_bonus_sum(manager_data)

            work_sheet[f'B{iteration}'] = total_tons_for_this_manager / 200
            iteration += 2


    def set_telephone_and_name_in_cabinet_report(self, work_sheet, iteration, manager):
        telephone_number = manager[0]
        if not telephone_number:
            return False
        work_sheet[f'A{iteration}'] = telephone_number
        iteration += 1
        manager_name = manager[1]
        work_sheet[f'A{iteration}'] = manager_name
        iteration += 1
        work_sheet[f'A{iteration}'] = '00208'
        return True


    def get_bonus_sum(self, manager_data):
        nomenclature = manager_data[0]
        tons = float(manager_data[2])
        product_mass = utils.get_product_mass(nomenclature)
        bags_count = tons * 1000 / product_mass
        bonus_sum = bags_count * self.bonus_count
        return bonus_sum


    def get_work_report(self):
        work_sheet = self.report_file.create_sheet('Рабочий отчет', 0)
        self.set_work_report_title(work_sheet)
        iteration = 1
        total_bags_count, total_bonus_sum = 0, 0
        for manager in self.data:
            if not self.set_telephone_and_name_in_work_report(work_sheet, iteration, manager):
                break
            iteration += 3
            for manager_data in manager[2]:
                calculation = self.get_calculations_for_manager_data(manager_data)
                total_bags_count += calculation['bags_count']
                total_bonus_sum += calculation['bonus_sum']
                self.set_work_report_cell_value(work_sheet, iteration, calculation)
                iteration += 1
            self.summarize(work_sheet, iteration, total_bags_count, total_bonus_sum)


    def summarize(self, work_sheet, iteration, total_bags_count, total_bonus_sum):
        iteration +=1
        work_sheet[f'A{iteration}'] = 'Итого:'
        work_sheet[f'E{iteration}'] = total_bags_count
        work_sheet[f'G{iteration}'] = total_bonus_sum


    def set_telephone_and_name_in_work_report(self, work_sheet, iteration, manager):
        telephone_number = manager[0]
        if not telephone_number:
            return False
        manager_name = manager[1]
        iteration += 1
        work_sheet[f'A{iteration}'] = telephone_number
        iteration += 1
        work_sheet[f'A{iteration}'] = manager_name
        return True


    def set_work_report_title(self, work_sheet):
        work_sheet['B1'] = 'Номенклатурный код'
        work_sheet['C1'] = 'Тоннаж'
        work_sheet['D1'] = 'Вес единицы продукта'
        work_sheet['E1'] = 'Количество мешков'
        work_sheet['F1'] = 'Бонус за 1 мешок'
        work_sheet['G1'] = 'Сумма бонуса'


    def set_work_report_cell_value(
            self, work_sheet, iteration, calculation):
        work_sheet[f'A{iteration}'] = calculation['nomenclature']
        work_sheet[f'B{iteration}'] = calculation['nomenclature_code']
        work_sheet[f'C{iteration}'] = calculation['tons']
        work_sheet[f'D{iteration}'] = calculation['product_mass']
        work_sheet[f'E{iteration}'] = calculation['bags_count']
        work_sheet[f'F{iteration}'] = calculation['bonus_count']
        work_sheet[f'G{iteration}'] = calculation['bonus_sum']


    def get_calculations_for_manager_data(self, manager_data):
        nomenclature = manager_data[0]
        nomenclature_code = manager_data[1]
        tons = float(manager_data[2])
        product_mass = utils.get_product_mass(nomenclature)
        bags_count = tons * 1000 / product_mass
        bonus_count = self.bonus_count
        bonus_sum = bags_count * bonus_count
        return {'nomenclature': nomenclature, 'nomenclature_code': nomenclature_code,
                'tons': tons, 'product_mass': product_mass, 'bags_count': bags_count,
                'bonus_count': bonus_count, 'bonus_sum': bonus_sum}


'''
Кейсы для utils
'''


class CaseCabinetTonsBagbonus(BaseBugBonus):
    pass
