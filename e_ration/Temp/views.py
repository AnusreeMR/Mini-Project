from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request,'Temp/home.html')

def admin(request):
    return render(request,'Temp/admin.html')



def register(request):
    return render(request,'Temp/register.html')