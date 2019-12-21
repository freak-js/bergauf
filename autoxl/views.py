from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from .models import Distributor
from .utils.utils import redirect_to_error_page, get_case
from .utils.error_messages import *
from openpyxl.writer.excel import save_virtual_workbook
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login


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


def logout_view(request):
    logout(request)
    return redirect('login')


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
    distributor_id_from_hidden_input = request.POST.get('hidden_distributor_id')

    if not any([id_editable_distributor, distributor_id_from_hidden_input]):
        return redirect_to_error_page(request, CHANGE_DISTRIBUTOR_ID_ERROR)

    if all([id_editable_distributor, distributor_id_from_hidden_input]):
        return redirect_to_error_page(request)
    distributor = get_object_or_404(
        Distributor,
        pk=id_editable_distributor if id_editable_distributor else distributor_id_from_hidden_input
    )

    if id_editable_distributor:
        return render(request, 'autoxl/change_distributor.html', {'distributor': distributor})

    if distributor_id_from_hidden_input:
        try:
            distributor.change(request)
        except Exception:
            return redirect_to_error_page(request, CHANGE_DISTRIBUTOR_SAVE_ERROR)
        return redirect('distributors')


def get_report(request):
    report = get_case(request)
    report.get_work_report()
    report.get_cabinet_report()
    response = HttpResponse(
        save_virtual_workbook(report.report_file),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=report.xlsx'
    return response

