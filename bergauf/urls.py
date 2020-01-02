from django.contrib import admin
from django.urls import path
from autoxl import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='autoxl/index.html',
                                          redirect_authenticated_user=True), name="login"),
    path('login/', auth_views.LoginView.as_view(template_name='autoxl/index.html',
                                                redirect_authenticated_user=True), name="login"),
    path('logout/', views.logout_views, name='logout_views'),
    path('welcome/', views.welcome, name='welcome'),
    path('get_report/', views.get_report, name='get_report'),
    path('notice/', views.notice, name='notice'),
    path('add_distributor/', views.add_distributor, name='add_distributor'),
    path('distributors/', views.distributors, name='distributors'),
    path('save_distributor/', views.save_distributor, name='save_distributor'),
    path('delete_distributor/', views.delete_distributor, name='delete_distributor'),
    path('change_distributor_form/', views.change_distributor_form, name='change_distributor_form'),
    path('change_distributor/', views.change_distributor, name='change_distributor'),
]
