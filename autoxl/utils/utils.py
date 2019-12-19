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
    return render(request, 'autoxl/notice.html', {'context': f'Произошла ошибка {context}'})

def get_product_mass(string: str) -> Union[int, bool]:
    pattern = r'([1-9][0-9]?)[\sк][кг][кг]?'
    result = re.findall(pattern, string)[0]
    if result in constants.PRODUCT_MASS:
        return int(result)
    return False

def validate_phone_number(phone_number: str) -> Union[bool, str]:
    if len(phone_number) < 7 or len(phone_number) > 18:
        return False
    for symbol in phone_number:
        if symbol not in constants.TELEPHONE_NUMBER_VALID_SYMBOLS:
            return False
    return phone_number

def get_kilograms_from_tons(tons: str) -> Union[bool, float]:
    try:
        kilograms = float(tons) * 1000
    except ValueError:
        return False
    return kilograms

def get_case(request):
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


