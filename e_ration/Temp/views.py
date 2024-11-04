from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request,'Temp/home.html')

def admin(request):
    return render(request,'Temp/admin.html')

def shopkeeper(request):
    return render(request,'Temp/shopkeeper.html')

def customer(request):
    return render(request,'Temp/user.html')

def register(request):
    return render(request,'Temp/register.html')

