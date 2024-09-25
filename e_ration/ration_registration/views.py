from django.shortcuts import render
from ration_registration.models import Shopkeeper
from login.models import Login
import random
import string
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
# Create your views here.


def rreg(request):
    obk = ""
    shopid_error = ""
    email_error = ""
    
    if request.method == "POST":
        shop_id = request.POST.get('shopid')
        email = request.POST.get('email')
        
        # Check if Shop ID or Email already exists
        if Shopkeeper.objects.filter(shop_id=shop_id).exists():
            shopid_error = "Shop ID already exists"
        elif Shopkeeper.objects.filter(email=email).exists():
            email_error = "Email already exists"
        else:
            # If validation passes, save the shopkeeper and login details
            obj = Shopkeeper()
            obj.shop_id = shop_id
            obj.shop_name = request.POST.get('shopname')
            obj.shopkeeper_name = request.POST.get('shopkeeper_name')
            obj.address = request.POST.get('address')
            obj.email = email
            obj.muncipality = request.POST.get('muncipality')
            obj.save()


            obk = "Successfully registered"
    
    # Pass messages and error flags to the template
    context = {
        'msg': obk,
        'shopid_error': shopid_error,
        'email_error': email_error
    }
    return render(request, 'rationregistration/rationreg.html', context)


def generate_random_password(length=8):
    """Generate a random password with letters and digits."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def accept(request, idd):
    obj = Shopkeeper.objects.get(shop_id=idd)
    obj.status = "Accepted"
    
    obj.save()

    obb=Login()
    new_password = generate_random_password()
    obb.username = obj.shopkeeper_name
    # Hash the password before saving (Django stores hashed passwords)
    obb.password = make_password(new_password) 
    obb.type = 'shopkeeper'
    obb.uid = obj.shop_id
    obb.save()
    
    # Send an email with the new password
    send_mail(
        'Registration Successfull',
        f'Hello {obj.shopkeeper_name},\n\nYour Rationshop account has been accepted. Here are your login credentials:\n\nUsername: {obj.shopkeeper_name}\nPassword: {new_password}\n\nPlease change your password after logging in.',
        'admin@yourorganization.com',  # Replace with your "from" email
        [obj.email],  # Send to the volunteer's email
        fail_silently=False,
    )
    
    return rreg(request)

def mr(request):
    obj=Shopkeeper.objects.all()
    context={
        'dd':obj
    }
    return render(request,'rationregistration/manage_rreg.html',context)

#def approve(request,idd) :
   #obj=Shopkeeper.objects.get(shop_id=idd)
   #obj.status='Approved'
   #obj.save()
   #return rreg(request)




#def viewr(request) :
 #   obj=UserRegistration.objects.all()
 #   context={
 #       'bb':obj
 #   }
 #   return render(request,'user_registration/view user_registration view_rshop.html',context)