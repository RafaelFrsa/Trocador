from django.shortcuts import render
from dupl_tubo import *
from .models import Trocador
from django.http.response import HttpResponse

# Create your views here.
def  index(request):
	return render(request, 'trocador/index.html',)

def calcular(request):
    form= formcalculator()
    if request.method == 'POST':
        f1=eval(request.POST['fluido1'])
        f2=eval(request.POST['fluido2'])
        m1=eval(request.POST['material'])
        return HttpResponse(reynolds_tube(f1,f2))
    return render(request,'index.html',{'form':form})
