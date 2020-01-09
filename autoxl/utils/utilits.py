from django.shortcuts import render, HttpResponse
from .error_messages import *
from typing import Union
import re
from . import constants
from .cases import (CaseCabinetTonsBugBonus, CaseCabinetTonsFixedBonusPalette, CaseCabinetTonsFixedBonusBugs,
                    CaseCabinetTonsFixedBonusTons, CaseManagersTonsBugBonus)
from django.core.files.uploadedfile import InMemoryUploadedFile

"""
Модуль вспомогательных утилит
"""


def redirect_to_error_page(request=None, context='') -> HttpResponse:
    """Функция редиректа на страницу уведомления об ошибках.
    """
    return render(request, 'autoxl/notice.html', {'context': f'{context}'})


def validate_id(raw_id: str) -> Union[bool, int]:
    """Функция валидации id, взвращает int в случае успешного прохождения
    валидации, или False в ином другом.
    """
    try:
        id = int(raw_id)
    except Exception:
        return False
    if id < 1:
        return False
    return id


def get_product_mass(nomenclature: str) -> Union[int, bool]:
    """Функция получения массы продукта из номенклатуры продукта на основе
    регулярного выражения, работает для варинтов с 'к', 'кг', 'л' идущими
    после искомого числового значения.
    """
    pattern = r'([1-9][0-9]?)[\sкл][\sкгл][кг]?'
    if result := re.findall(pattern, nomenclature):
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


def validate_tons_value(tons: Union[int, float]) -> bool:
    try:
        float(tons) * 1000
    except ValueError:
        return False
    return True


def validate_division(nomenclature: str, tons: Union[int, float]) -> bool:
    product_mass = get_product_mass(nomenclature)
    bags_count = float(tons) * 1000 % product_mass
    return False if bags_count else True


def validate_cell_value(cell_nomenclature, cell_mass) -> dict:
    """Валидирование входных данных из ячеек, где:
    cell_a - ячейка с номенклатурой
    cell_c - ячейка с тоннажом продукции
    Проверяет возможность получения массы продукта из номенклатуры,
    валидирует значение тоннажа и возможность выполнения операции приведения к килограммам,
    проверяет возможность выполнения операции получения колчества единиц проданного
    продукта и отсутсвия остатка при делении (остаток означает ошибку при заполнении ячейки).
    """
    if not get_product_mass(cell_nomenclature.value):
        return {'error': [cell_nomenclature.row, cell_nomenclature.value, cell_nomenclature.coordinate,
                          PRODUCT_MASS_VALIDATION_ERROR]}

    if not validate_tons_value(cell_mass.value):
        return {'error': [cell_mass.row, cell_mass.value, cell_mass.coordinate, MASS_VALIDATION_ERROR]}

    if not validate_division(cell_nomenclature.value, cell_mass.value):
        return {'error': [cell_mass.row, cell_mass.value, cell_mass.coordinate, MASS_DIVISION_VALIDATION_ERROR]}
    return {'validate': True}


def search_telephone_number(external_id: str, manager_name: str, file2_data: list) -> Union[str, int, bool]:
    """Поиск телефонного номера по полному совпадению имени менеджера и внешнего ID дистрибьютора
    в прилагаемом втором файле и базе данных
    """
    for data in file2_data:
        id = str(data[0].value) # Приводим к строке, т.к. в базе хранится в виде строки
        name = data[2].value
        phone_number = data[3].value
        if name == manager_name and id == external_id:
            return phone_number
    return False


def get_report_file(request: HttpResponse):
    """Функция - парсер сценариев, на основе анализа полученных данных выбранных пользователем
    на странице welcome формирует правильный варинат присвоения класса для извлечения и обработки
    данных полученных из файла/файлов формата .xlsx.
    """
    post = request.POST
    file1: InMemoryUploadedFile = request.FILES.get('file_1')
    file2: InMemoryUploadedFile = request.FILES.get('file_2')
    bonus_count = int(post['bonus_count_input'])

    if post['variant_compensation_selectbox'] == '1':  # Способ компенсации: Кабинет 007

        if post['report_format_selectbox'] == '1':  # Формат отчета: Отчет кабинета 007

            if post['sales_units_selectbox'] == '1':  # Продажи, единицы: Тонны

                if post['bonus_type_selectbox'] == '1':  # Тип бонуса: Бонус за мешок
                    return CaseCabinetTonsBugBonus(file1, bonus_count)

                if post['bonus_type_selectbox'] == '2':  # Тип бонуса: Фиксированный бонус

                    if post['fixed_bonus_selectbox'] == '1':  # Фиксированный бонус с: Палетты

                        if post.get('action_checkbox'):
                            product_count_input = int(post['product_count_input'])
                            return CaseCabinetTonsFixedBonusPalette(file1, bonus_count, product_count_input, True)
                        else:
                            product_count_input = int(post['product_count_input'])
                            return CaseCabinetTonsFixedBonusPalette(file1, bonus_count, product_count_input, False)

                    if post['fixed_bonus_selectbox'] == '2':  # Фиксированный бонус с: Мешка

                        if post.get('action_checkbox'):
                            product_count_input = int(post['product_count_input'])
                            return CaseCabinetTonsFixedBonusBugs(file1, bonus_count, product_count_input, True)
                        else:
                            product_count_input = int(post['product_count_input'])
                            return CaseCabinetTonsFixedBonusBugs(file1, bonus_count, product_count_input, False)

                    if post['fixed_bonus_selectbox'] == '3':  # Фиксированный бонус с: Тонны

                        if post.get('action_checkbox'):
                            product_count_input = int(post['product_count_input'])
                            return CaseCabinetTonsFixedBonusTons(file1, bonus_count, product_count_input, True)
                        else:
                            product_count_input = int(post['product_count_input'])
                            return CaseCabinetTonsFixedBonusTons(file1, bonus_count, product_count_input, False)

        if post['report_format_selectbox'] == '2':  # Формат отчета: Отчет с менеджерами

                if post['bonus_type_selectbox'] == '1':  # Тип бонуса: Бонус за мешок

                    if post['sales_units_selectbox'] == '1':  # Продажи, единицы: Тонны
                        distributor_name_input = post['distributor_name_input']
                        return CaseManagersTonsBugBonus(file1, file2, bonus_count, distributor_name_input, bugs=False)

                    if post['sales_units_selectbox'] == '2':  # Продажи, единицы: Мешки
                        distributor_name_input = post['distributor_name_input']
                        return CaseManagersTonsBugBonus(file1, file2, bonus_count, distributor_name_input, bugs=True)

                if post['bonus_type_selectbox'] == '2':  # Тип бонуса: Фиксированный бонус
                    pass

        if post['report_format_selectbox'] == '3':  # Формат отчета: Отчет без менеджеров
            pass

    else:  # Способ компенсации: Карты
        pass
