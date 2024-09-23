from django.shortcuts import render
from User.models import User
# Create your views here.

def vuser(request):
    obj=User.objects.all()
    context={
        'dd':obj
    }
    return render(request,'User/view_user.html',context)

def mu(request):
    obj=User.objects.all()
    context={
        'dd':obj
    }
    return render(request,'user/manage user.html',context)


def update(request,idd):
    obj = User.objects.get(user_id=idd)
    context = {
        'dd': obj
    }
    if request.method=="POST":
        obj=User.objects.get(user_id=idd)
       # obj.user_id=request.POST.get('jd')
        #obj.card_id=request.POST.get('mn')
        obj.card_type=request.POST.get('ct')
        obj.card_color=request.POST.get('cc')
        obj.head_name=request.POST.get('hn')
        obj.annual_income=request.POST.get('ai')
        obj.occupation=request.POST.get('oc')
        obj.age=request.POST.get('ag')
        obj.no_of_family_member=request.POST.get('nf')
        obj.no_of_adults=request.POST.get('na')
        obj.no_of_family_children=request.POST.get('nc')
        obj.address=request.POST.get('ad')
        obj.mobile_number=request.POST.get('mn')
        obj.save()
        return mu(request)
    return render(request,'user/update.html',context)

def delete(request,idd):
    obj=User.objects.get(user_id=idd)
    obj.delete()
    return vuser(request)