from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from .models import Distributor
from django.contrib.auth.forms import AuthenticationForm
from .utils.utilits import redirect_to_error_page, get_case
from .utils.error_messages import *
from openpyxl.writer.excel import save_virtual_workbook
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


@login_required
def auth(request):
    if request.method == 'POST':
        AuthenticationForm(request.POST)
    form = AuthenticationForm
    return render(request, 'autoxl/auth.html', {'form': form})


@login_required
def welcome(request):
    distributors = Distributor.objects.all().filter(active=True)
    distributors_names = [distributor.name for distributor in distributors]
    return render(request, 'autoxl/welcome.html', {'distributors_names': distributors_names})


@login_required
def notice(request):
    return render(request, 'autoxl/notice.html')


@login_required
def distributor(request):
    return render(request, 'autoxl/distributor.html')


@login_required
def distributors(request):
    distributors = Distributor.objects.all().filter(active=True).order_by('-add_date')
    return render(request, 'autoxl/distributors.html', {'distributors': distributors})


def logout_views(request):
    logout(request)
    return redirect('login')


@login_required
@require_POST
def save_distributor(request):
    distributor = Distributor.save_distributor(request)
    if name := distributor.get('name'):
        return redirect_to_error_page(request, f'{UNIQUE_EXTERNAL_ID_ERROR} {name}')
    elif distributor.get('successfully'):
        return redirect('distributors')
    return redirect_to_error_page(request, UNKNOWN_ERROR)


@login_required
@require_POST
def delete_distributor(request):
    try:
        distributor_id = int(request.POST.get('id_delete_distributor'))
    except TypeError:
        return redirect_to_error_page(request)
    distributor = get_object_or_404(Distributor, pk=distributor_id)
    distributor.kill()
    return redirect('distributors')


@login_required
@require_POST
def change_distributor(request):
    id_editable_distributor = request.POST.get('id_editable_distributor')
    id_from_hidden_input = request.POST.get('hidden_distributor_id')
    pk = id_editable_distributor or id_from_hidden_input
    distributor = get_object_or_404(Distributor, pk=pk)

    if id_editable_distributor:
        return render(request, 'autoxl/change_distributor.html', {'distributor': distributor})

    if id_from_hidden_input:
        try:
            distributor.change(request)
        except Exception:
            return redirect_to_error_page(request, CHANGE_DISTRIBUTOR_SAVE_ERROR)
        return redirect('distributors')


@login_required
@require_POST
def get_report(request):
    report = get_case(request)
    if report.errors:
        return render(request, 'autoxl/notice.html', {'errors': report.errors})
    report.get_work_report()
    report.get_cabinet_report()
    response = HttpResponse(
        save_virtual_workbook(report.report_file),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=report.xlsx'
    return response
