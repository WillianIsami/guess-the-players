from django.urls import path
from .views import IndexView
from django.urls import re_path

urlpatterns = [
    # path('endereço/', minhaview.as_view(), name='nome-da-url'),
    path('', IndexView.as_view(), name='home'),
]
