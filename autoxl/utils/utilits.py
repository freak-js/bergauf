from django.shortcuts import render, HttpResponse
from .error_messages import *
from typing import Union
import re
from . import constants
from .cases import CaseCabinetTonsBagbonus


"""
Модуль вспомогательных утилит
"""


def redirect_to_error_page(request: HttpResponse, context: str = '') -> HttpResponse:
    """Функция редиректа на страницу уведомления об ошибках
    """
    return render(request, 'autoxl/notice.html', {'context': f'Произошла ошибка {context}'})


def get_product_mass(string: str) -> Union[int, bool]:
    pattern = r'([1-9][0-9]?)[\sкл][\sкгл][кг]?'
    result = re.findall(pattern, string)
    if result:
        kilograms = result[0]
        if kilograms in constants.PRODUCT_MASS:
            return int(kilograms)
    return False


def validate_phone_number(raw_phone_number: Union[str, int]) -> bool:
    phone_number = str(raw_phone_number)
    if len(phone_number) < 7 or len(phone_number) > 18:
        return False
    for symbol in phone_number:
        if symbol not in constants.TELEPHONE_NUMBER_VALID_SYMBOLS:
            return False
    return True


def validate_manager_name(manager_name: str) -> bool:
    for symbol in manager_name:
        if not symbol.isalpha() and symbol not in (' ', '.'):
            return False
        return True if len(manager_name) > 5 else False


def validate_tons_value(tons: str) -> bool:
    try: float(tons) * 1000
    except Exception: return False
    return True


def validate_division(nomenclature: str, tons: str) -> bool:
    product_mass = get_product_mass(nomenclature)
    bags_count = float(tons) * 1000 % product_mass
    return False if bags_count else True


def validate_cell_value(cell_a, cell_c) -> dict:
    if not get_product_mass(cell_a.value):
        return {'error': [cell_a.row, cell_a.value, cell_a.coordinate, PRODUCT_MASS_VALIDATION_ERROR]}

    if not validate_tons_value(cell_c.value):
        return {'error':[cell_c.row, cell_c.value, cell_c.coordinate, MASS_VALIDATION_ERROR]}

    if not validate_division(cell_a.value, cell_c.value):
        return {'error': [cell_c.row, cell_c.value, cell_c.coordinate, MASS_DIVISION_VALIDATION_ERROR]}
    return {'validate': True}


def get_case(request: HttpResponse):
    post = request.POST
    file1 = request.FILES.get('file_1')
    file2 = request.FILES.get('file_2')

    if post['variant_compensation_selectbox'] == '1':

        if post['report_format_selectbox'] == '1':
            if post['sales_units_selectbox'] == '1':
                if post['bonus_type_selectbox'] == '1':
                    bonus_count = int(post['bonus_count_input'])
                    case = CaseCabinetTonsBagbonus(file1, bonus_count)
                    return case
                if post['bonus_type_selectbox'] == '2':
                    if post['fixed_bonus_selectbox'] == '1':
                        if post['action_checkbox'] == '':
                            pass
                        if post['action_checkbox'] == 'on':
                            pass
                    if post['fixed_bonus_selectbox'] == '2':
                        if post['action_checkbox'] == '':
                            pass
                        if post['action_checkbox'] == 'on':
                            pass
                    if post['fixed_bonus_selectbox'] == '3':
                        if post['action_checkbox'] == '':
                            pass
                        if post['action_checkbox'] == 'on':
                            pass
            else:
                redirect_to_error_page(request, SALES_UNITS_ERROR)

        if post['report_format_selectbox'] == '2':
            pass

        if post['report_format_selectbox'] == '3':
            pass

    if post['variant_compensation_selectbox'] == '2':
        pass


