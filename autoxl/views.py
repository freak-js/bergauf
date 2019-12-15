from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Distributor
from .utils.utils import redirect_to_error_page
# from .utils import get_work_sheet, generate_report
# from django.http import HttpResponse
# from openpyxl.writer.excel import save_virtual_workbook



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
    if distributor:
        return redirect('distributors')
    return redirect_to_error_page(request)


@require_POST
def delete_distributor(request):
    try:
        distributor_id = int(request.POST.get('delete_id'))
    except TypeError:
        return redirect_to_error_page(request)

    distributor = get_object_or_404(Distributor, pk=distributor_id)
    distributor.kill()
    return redirect('distributors')


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