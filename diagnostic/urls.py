from django.urls import path
from . import views

app_name = 'diagnostic'
urlpatterns = [
    path('tumour_result', views.tumour_result, name='tumour_result'),

    path('cancer_result', views.cancer_result, name='cancer_result'),

    path('calcium_result', views.calcium_result, name='calcium_result'),

    path('headache_result', views.headache_result, name='headache_result'),
]