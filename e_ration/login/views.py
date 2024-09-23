from django.http import HttpResponseRedirect
from django.shortcuts import render
from login.models import Login
# Create your views here.
def login(request):
    if request.method == "POST":
        objlist=''
        uname = request.POST.get("user")
        passw = request.POST.get("password")
        obj =  Login.objects.filter(username=uname, password=passw)
        tp = ""
        for ob in obj:
            tp = ob.type
            uid = ob.uid
            if tp == "admin":
                request.session["uid"] = uid
                return HttpResponseRedirect('/Temp/admin/')
            #elif tp =="police":
                #request.session["uid"] = uid
                #return HttpResponseRedirect('/temp/police/')
            elif tp =="user":
                request.session["uid"] = uid
                return HttpResponseRedirect('/Temp/user/')
            # elif tp == "friend":
            #   request.session["uid"] uid
            #   return render(request, 'temp/Friends.home.html')
        else:
            objlist = "username or password incorrect... Please try again..!"
            context ={
                'msg' :objlist,
            }
            return render(request,'login/login.html',context)
    return render(request,'login/login.html')



