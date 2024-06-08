from django.urls import path
from . import views

app_name = 'diagnostic'
urlpatterns = [
    path('tumour_result', views.tumour_result, name='tumour_result')
]