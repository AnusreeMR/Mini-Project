from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import check_password
from login.models import Login

def login(request):
    if request.method == "POST":
        uname = request.POST.get("user")
        passw = request.POST.get("password")
        
        try:
            # Get the Login object by username
            obj = Login.objects.get(username=uname)
            
            # Use Django's check_password to compare the hashed password
            if check_password(passw, obj.password):  # This checks the hashed password
                tp = obj.type
                uid = obj.uid
                # Use session to store uid and redirect based on user type
                request.session["uid"] = uid
                
                if tp == "admin":
                    return HttpResponseRedirect('/Temp/admin/')
                elif tp == "shopkeeper":
                    return HttpResponseRedirect('/Temp/user/')
            else:
                # Incorrect password case
                context = {
                    'msg': "Username or password incorrect. Please try again!"
                }
                return render(request, 'login/login.html', context)
        
        except Login.DoesNotExist:
            # If the username is not found
            context = {
                'msg': "Username or password incorrect. Please try again!"
            }
            return render(request, 'login/login.html', context)
    
    return render(request, 'login/login.html')
