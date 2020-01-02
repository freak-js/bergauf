from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from .models import Distributor
from django.contrib.auth.forms import AuthenticationForm
from .utils.utilits import redirect_to_error_page, get_report_file, validate_id
from .utils.error_messages import *
from openpyxl.writer.excel import save_virtual_workbook
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


@login_required
def index(request):
    if request.method == 'POST':
        AuthenticationForm(request.POST)
    return render(request, 'autoxl/index.html', {'form': AuthenticationForm})


@login_required
def welcome(request):
    active_distributors = Distributor.objects.all().filter(active=True)
    distributors_names = [distributor.name for distributor in active_distributors]
    return render(request, 'autoxl/welcome.html', {'distributors_names': distributors_names})


@login_required
def notice(request):
    return render(request, 'autoxl/notice.html')


@login_required
def add_distributor(request):
    return render(request, 'autoxl/add_distributor.html')


@login_required
def distributors(request):
    active_distributors = Distributor.objects.all().filter(active=True).order_by('-add_date')
    return render(request, 'autoxl/distributors.html', {'distributors': active_distributors})


def logout_views(request):
    logout(request)
    return redirect('login')


@login_required
@require_POST
def save_distributor(request):
    save_result = Distributor.save_distributor(request)
    if name := save_result.get('name'):
        return redirect_to_error_page(request, f'{UNIQUE_EXTERNAL_ID_ERROR} {name}')
    elif save_result.get('successfully'):
        return redirect('distributors')
    return redirect_to_error_page(request, UNKNOWN_ERROR)


@login_required
@require_POST
def delete_distributor(request):
    if distributor_id := validate_id(request.POST.get('distributor_id')):
        distributor = get_object_or_404(Distributor, pk=distributor_id)
        distributor.kill()
        return redirect('distributors')
    return redirect_to_error_page(request, ID_VALIDATE_ERROR)


@login_required
@require_POST
def change_distributor_form(request):
    if distributor_id := validate_id(request.POST.get('distributor_id')):
        distributor = get_object_or_404(Distributor, pk=distributor_id)
        return render(request, 'autoxl/change_distributor.html', {'distributor': distributor})
    return redirect_to_error_page(request, ID_VALIDATE_ERROR)


@login_required
@require_POST
def change_distributor(request):
    if distributor_id := validate_id(request.POST.get('distributor_id')):
        distributor = get_object_or_404(Distributor, pk=distributor_id)
        try:
            distributor.change(request)
        except Exception:
            return redirect_to_error_page(request, CHANGE_DISTRIBUTOR_SAVE_ERROR)
        return redirect('distributors')
    return redirect_to_error_page(request, ID_VALIDATE_ERROR)


@login_required
@require_POST
def get_report(request):
    report = get_report_file(request)
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
