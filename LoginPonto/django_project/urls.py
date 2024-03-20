from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view),
    path('home/', views.home_view, name='home'),
    path('login/', views.login_view, name='login_view'),
    path('cadastro/', views.cadastro_view, name='cadastro_view'),
    path('logout', views.logout_view, name='logout_view'),
    path('registro/', views.registro_view, name='registro_view'),
    path('registro_confirmado/', views.registro_confirmado_view, name='registro_confirmado_view'),
    path('registro_atual/', views.registro_atual_view, name='registro_atual_view'),
    path('check-ip/', views.check_ip, name='check_ip'),

]
