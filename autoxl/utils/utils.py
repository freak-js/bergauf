from django.shortcuts import render


'''
Модуль вспомогательных утилит
'''

def redirect_to_error_page(request, context=''):
    '''
    redirect_to_error_page - функция обработки контекста ошибок.

    Parameters
    ----------
    request - объект запрса Django принимаемый во views.
    context - текстовое описание ошибки передаваемой на экран notice.

    Returns
    -------
    None, рендерит экран уведомдлений.
    '''
    return render(request, 'autoxl/notice.html', {'context': f'Произошла ошибка {context}'})