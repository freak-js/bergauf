from django.shortcuts import render


def redirect_to_error_page(request):
    return render(request, 'autoxl/notice.html', {'context': 'Произошла ошибка'})