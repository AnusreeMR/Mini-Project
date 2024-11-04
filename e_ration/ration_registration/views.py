from django.shortcuts import render, redirect
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
            obj = Shopkeeper(
                shop_id=shop_id,
                shop_name=request.POST.get('shopname'),
                shopkeeper_name=request.POST.get('shopkeeper_name'),
                address=request.POST.get('address'),
                email=email,
                muncipality=request.POST.get('muncipality'),
                status="Pending"  # Set status as pending when registering
            )
            obj.save()
            obk = "Successfully registered with status pending"
    
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

    obb = Login()
    new_password = generate_random_password()
    obb.username = obj.shop_id
    obb.password = make_password(new_password) 
    obb.type = 'shopkeeper'
    obb.uid = obj.shop_id
    obb.save()
    
    # Send an email with the new password
    send_mail(
        'Registration Successful',
        f'Hello {obj.shopkeeper_name},\n\nYour Ration shop account has been accepted. Here are your login credentials:\n\nUsername: {obj.shop_id}\nPassword: {new_password}\n\nPlease note down the password for future reference.',
        'admin@yourorganization.com',
        [obj.email],  
        fail_silently=False,
    )

    # Redirect to manage page after acceptance
    return mr(request)

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

def reject_rationshop(request, idd):
    # Get the Shopkeeper object or return 404 if not found
    obj = get_object_or_404(Shopkeeper, shop_id=idd)

    if obj.status == "Pending":
        # Send an email with the rejection message
        send_mail(
            'Registration Rejected',
            f'Dear {obj.shopkeeper_name},\n\nWe regret to inform you that your Ration Shop account registration has been rejected.\n\nBest regards,\nAdmin Team',
            'admin@yourorganization.com',  # Replace with your "from" email
            [obj.email],  # Send to the shopkeeper's email
            fail_silently=False,
        )

        # Now delete the object to remove it from the database
        obj.delete()

    return redirect('mr')  # Redirect to the page that lists the requests

    
    # Optionally, you could add a message in the template to notify the admin that the rejection email was sent

def mr(request):
    # Get the search query from the request
    search_query = request.GET.get('shop_id', '')  # Default to empty string if not provided
    if search_query:
        # Filter the Shopkeeper objects based on the shop_id
        obj = Shopkeeper.objects.filter(shop_id__icontains=search_query)
    else:
        # If no search query, retrieve all Shopkeeper objects
        obj = Shopkeeper.objects.all()

    context = {
        'dd': obj,
        'search_query': search_query  # Pass the search query back to the template
    }
    return render(request, 'rationregistration/manage_rreg.html', context)

#def mr(request):
 #   obj=Shopkeeper.objects.all()
  #  context={
   #     'dd':obj
    #}
    #return render(request,'rationregistration/manage_rreg.html',context)

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