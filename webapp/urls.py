from django.urls import path
from . import views

urlpatterns = [
    path('', views.BASE, name='BASE'),

    path('tumour', views.tumour, name='tumour'),

    path('cancer', views.cancer, name='cancer'),

    path('calcium', views.calcium, name='calcium'),

    path('headache', views.headache, name='headache')
]