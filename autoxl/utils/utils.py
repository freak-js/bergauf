from django.shortcuts import render
from .constants import PRODUCT_MASS
# from .error_messages import *
import re


"""
Модуль вспомогательных утилит
"""


def redirect_to_error_page(request=None, context: str = ''):
    """
    redirect_to_error_page - функция обработки контекста ошибок.

    Parameters
    ----------
    request - объект запрса Django принимаемый во views.
    context - текстовое описание ошибки передаваемой на экран notice.

    Returns
    -------
    None, рендерит экран уведомдлений.
    """
    return render(request, 'autoxl/notice.html', {'context': f'Произошла ошибка {context}'})


def get_product_mass(string: str):
    """
    get_product_mass - функция распарсивания ячейки "Номенклатура" и получения веса продукта в соответсвии со списком
    валидных значений из PRODUCT_MASS модуля constants.

    Parameters
    ----------
    string - данные из ячейки для обработки в строковом формате.

    Returns
    -------
    Вес продукта, или рендер страницы уведомлдения об ошибке.
    """
    pattern = r'([1-9][0-9]?)[\sк][кг][кг]?'
    result = re.findall(pattern, string)[0]
    if result in PRODUCT_MASS:
        return int(result)
    return False


def validate_phone_number(phone_number):  # TODO
    pass


def get_kilograms_from_tons(tons):
    try:
        kilograms = float(tons) * 1000
    except ValueError:
        return False
    return kilograms
