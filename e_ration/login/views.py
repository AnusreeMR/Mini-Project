from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from login.models import Login

def login(request):
    if request.method == "POST":
        uname = request.POST.get("user")
        passw = request.POST.get("password")
        
        try:
            # Use filter to handle potential multiple objects and retrieve the first match
            obj = Login.objects.filter(username=uname).first()
            
            if obj is not None:
                # Use Django's check_password to compare the hashed password
                if check_password(passw, obj.password):  # This checks the hashed password
                    tp = obj.type
                    uid = obj.uid
                    # Use session to store uid and redirect based on user type
                    request.session["uid"] = uid
                    
                    if tp == "admin":
                        return HttpResponseRedirect('/Temp/admin/')
                    elif tp == "shopkeeper":
                        return HttpResponseRedirect('/Temp/shopkeeper/')
                else:
                    # Incorrect password case
                    context = {
                        'msg': "Username or password incorrect. Please try again!"
                    }
                    return render(request, 'login/login.html', context)
            else:
                # If the username is not found (None returned from filter)
                context = {
                    'msg': "Username or password incorrect. Please try again!"
                }
                return render(request, 'login/login.html', context)
        
        except Exception as e:
            # Optionally log the error or handle specific exceptions
            print(e)  # For debugging, replace with proper logging in production
            
            context = {
                'msg': "An unexpected error occurred. Please try again!"
            }
            return render(request, 'login/login.html', context)
    
    return render(request, 'login/login.html')
