from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

def BASE(request):
    template = loader.get_template('base.html')
    return HttpResponse(template.render())
# Create your views here.
