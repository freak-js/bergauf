from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Distributor
from .utils.utils import redirect_to_error_page
from .utils.error_messages import *
# from .utils import get_work_sheet, generate_report
# from django.http import HttpResponse
# from openpyxl.writer.excel import save_virtual_workbook



def index(request):
    distributors = Distributor.objects.all().filter(active=True)
    distributors_names = [distributor.name for distributor in distributors]
    return render(request, 'autoxl/index.html', {'distributors_names': distributors_names})


def notice(request):
    return render(request, 'autoxl/notice.html')


def distributor(request):
    return render(request, 'autoxl/distributor.html')


def distributors(request):
    distributors = Distributor.objects.all().filter(active=True).order_by('-add_date')
    return render(request, 'autoxl/distributors.html', {'distributors': distributors})


@require_POST
def save_distributor(request):
    distributor = Distributor.save_distributor(request)
    if isinstance(distributor, str):
        return redirect_to_error_page(request, f'{UNIQUE_EXTERNAL_ID_ERROR} {distributor}')
    if distributor:
        return redirect('distributors')
    return redirect_to_error_page(request)


@require_POST
def delete_distributor(request):
    try:
        distributor_id = int(request.POST.get('id_delete_distributor'))
    except TypeError:
        return redirect_to_error_page(request)

    distributor = get_object_or_404(Distributor, pk=distributor_id)
    distributor.kill()
    return redirect('distributors')


@require_POST
def change_distributor(request):
    id_editable_distributor = request.POST.get('id_editable_distributor')
    hidden_distributor_id = request.POST.get('hidden_distributor_id')

    if not any([id_editable_distributor, hidden_distributor_id]):
        #log
        return redirect_to_error_page(request, CHANGE_DISTRIBUTOR_ID_ERROR)

    if all([id_editable_distributor, hidden_distributor_id]):
        #log
        return redirect_to_error_page(request)

    distributor = get_object_or_404(
        Distributor,
        pk=id_editable_distributor if id_editable_distributor else hidden_distributor_id
    )

    if id_editable_distributor:
        return render(request, 'autoxl/change_distributor.html', {'distributor': distributor})

    if hidden_distributor_id:
        try:
            distributor.change(request)
        except Exception:
            return redirect_to_error_page(request, CHANGE_DISTRIBUTOR_SAVE_ERROR)
        return redirect('distributors')


def go(request):
    pass



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