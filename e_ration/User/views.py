from django.shortcuts import render
from User.models import User

# Create your views here.

def vuser(request):
    search_query = request.GET.get('search', '')
    if search_query:
        # Filter based on card_id or head_name
        obj = User.objects.filter(card_id__icontains=search_query) | User.objects.filter(head_name__icontains=search_query)
    else:
        obj = User.objects.all()
        
    context = {
        'dd': obj
    }
    return render(request, 'User/view_user.html', context)


def mu(request):
    # Get search parameters from the request
    card_id = request.GET.get('card_id')
    head_name = request.GET.get('head_name')
    
    # Filter the User objects based on the search parameters
    if card_id or head_name:
        obj = User.objects.all()
        if card_id:
            obj = obj.filter(card_id__icontains=card_id)
        if head_name:
            obj = obj.filter(head_name__icontains=head_name)
    else:
        obj = User.objects.all()

    # Pass the filtered objects to the template
    context = {
        'dd': obj
    }
    return render(request, 'user/manage user.html', context)



def update(request,idd):
    obj = User.objects.get(user_id=idd)
    context = {
        'dd': obj
    }
    if request.method=="POST":
        obj=User.objects.get(user_id=idd)
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
    return mu(request)