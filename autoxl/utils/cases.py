import openpyxl
from typing import Union
import re
from .constants import *


class BaseMethodClass:

    def validate_phone_number(phone_number: str) -> Union[bool, str]:
        if len(phone_number) < 7 or len(phone_number) > 18:
            return False
        for symbol in phone_number:
            if symbol not in TELEPHONE_NUMBER_VALID_SYMBOLS:
                return False
        return phone_number

    def get_kilograms_from_tons(tons: str) -> Union[bool, float]:
        try:
            kilograms = float(tons) * 1000
        except ValueError:
            return False
        return kilograms


class BaseOneFileCase007():

    def __init__(self, file, bonus_count):
        self.bonus_count = bonus_count
        self.work_book = openpyxl.load_workbook(file)
        self.first_sheet = self.work_book.get_sheet_names()[0]
        self.work_sheet = self.work_book.get_sheet_by_name(self.first_sheet)
        self.data = self.get_managers_data()

    def get_product_mass(self, string: str) -> Union[int, bool]:
        pattern = r'([1-9][0-9]?)[\sк][кг][кг]?'
        result = re.findall(pattern, string)[0]
        if result in PRODUCT_MASS:
            return int(result)
        return False

    def get_managers_data(self):
        iteration = 0
        free_cell = 0
        managers_data = []
        manager = []
        new_phone_number = True
        new_manager_name = True
        work_sheet = self.work_sheet
        while free_cell < 2:
            iteration += 1
            cell_A = work_sheet[f'A{iteration}'].value
            cell_B = work_sheet[f'B{iteration}'].value
            cell_C = work_sheet[f'C{iteration}'].value
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
                    manager.append([self.get_product_mass(cell_A), cell_B, cell_C])
                    continue
            else:
                managers_data.append(manager)
                manager = []
                new_phone_number = True
                new_manager_name = True
                free_cell += 1
                continue
        return managers_data

class CaseCabinet007TonsBagbonus(BaseOneFileCase007):

    pass
