from django.shortcuts import render, HttpResponse
from .constants import *
from .error_messages import *
from typing import Union
import re


"""
Модуль вспомогательных утилит
"""


def redirect_to_error_page(request: HttpResponse, context: str = '') -> HttpResponse:
    return render(request, 'autoxl/notice.html', {'context': f'Произошла ошибка {context}'})


def get_product_mass(string: str) -> Union[int, bool]:
    pattern = r'([1-9][0-9]?)[\sк][кг][кг]?'
    result = re.findall(pattern, string)[0]
    if result in PRODUCT_MASS:
        return int(result)
    return False


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
