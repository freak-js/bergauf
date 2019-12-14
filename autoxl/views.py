from django.shortcuts import render, redirect
from .utils import get_work_sheet, generate_report
from django.http import HttpResponse
from openpyxl.writer.excel import save_virtual_workbook
from django.views.decorators.http import require_POST
from .models import Distributor


def index(request):
    return render(request, 'autoxl/index.html')


def distributor(request):
    return render(request, 'autoxl/distributor.html')


def distributors(request):
    distributors = Distributor.objects.all().filter(active=True)
    return render(request, 'autoxl/distributors.html', {'distributors': distributors})

@require_POST
def save_distributor(request):
    distributor = Distributor.save_distributor(request)
    return redirect('distributors') if distributor else redirect('notice', {'context': 'Произошла ошибка'})


def notice(request):
    return render(request, 'autoxl/notice.html')




# def go(request):
#     work_sheet = get_work_sheet(request)
#     bonus_count = int(request.POST.get('number'))
#
#     if work_sheet:
#         report = generate_report(work_sheet, bonus_count)
#
#         if isinstance(report, list):
#             return render(request, 'autoxl/notice.html', {'errors': report})
#
#         response = HttpResponse(
#             save_virtual_workbook(report),
#             content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#         )
#         response['Content-Disposition'] = 'attachment; filename=report.xlsx'
#         return response
#     return render(request, 'autoxl/notice.html', {'context': 'Произошла ошибка'})