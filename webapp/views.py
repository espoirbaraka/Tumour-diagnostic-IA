from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

def BASE(request):
    template = loader.get_template('base.html')
    return HttpResponse(template.render())

def tumour(request):
    template = loader.get_template('tumour.html')
    return HttpResponse(template.render())

def cancer(request):
    template = loader.get_template('cancer.html')
    return HttpResponse(template.render())

def calcium(request):
    template = loader.get_template('calcium.html')
    return HttpResponse(template.render())

def headache(request):
    template = loader.get_template('headache.html')
    return HttpResponse(template.render())
# Create your views here.
