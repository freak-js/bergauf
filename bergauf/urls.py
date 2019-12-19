from django.contrib import admin
from django.urls import path
from autoxl import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('get_report/', views.get_report, name='get_report'),
    path('notice/', views.notice, name='notice'),
    path('distributor/', views.distributor, name='distributor'),
    path('distributors/', views.distributors, name='distributors'),
    path('save_distributor/', views.save_distributor, name='save_distributor'),
    path('delete_distributor/', views.delete_distributor, name='delete_distributor'),
    path('change_distributor/', views.change_distributor, name='change_distributor'),
]
