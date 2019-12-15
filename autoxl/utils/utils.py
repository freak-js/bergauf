from django.shortcuts import render


def redirect_to_error_page(request, context=''):
    return render(request, 'autoxl/notice.html', {'context': f'Произошла ошибка {context}'})