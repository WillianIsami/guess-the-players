from django.urls import path
from . import views
from django.urls import re_path

urlpatterns = [
    # path('endereço/', minhaview.as_view(), name='nome-da-url'),
    path('', views.IndexView.as_view(), name='home'),
    path('login/', views.login_view, name='login'),   
    path('example/', views.example_view, name='example'),

]
