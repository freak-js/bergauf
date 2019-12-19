from django.shortcuts import render, HttpResponse
from .error_messages import *
from .cases import CaseCabinet007TonsBagbonus


"""
Модуль вспомогательных утилит
"""


def redirect_to_error_page(request: HttpResponse, context: str = '') -> HttpResponse:
    return render(request, 'autoxl/notice.html', {'context': f'Произошла ошибка {context}'})


def get_case(request):
    post = request.POST
    file1 = request.FILES.get('file_1')
    file2 = request.FILES.get('file_2')

    if post['variant_compensation_selectbox'] == '1':

        if post['report_format_selectbox'] == '1':
            if post['sales_units_selectbox'] == '1':
                if post['bonus_type_selectbox'] == '1':
                    bonus_count = post['bonus_count_input']
                    case = CaseCabinet007TonsBagbonus(file1, bonus_count)
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


