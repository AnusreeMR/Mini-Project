from django.shortcuts import render, redirect
from customer.models import CustomerRegistration
from login.models import Login
import random
import string
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password

def custreg(request):
    obk = ""
    if request.method == "POST":
        obj = CustomerRegistration()
        obj.card_no = request.POST.get('card_no')
        obj.name = request.POST.get('name')
        obj.address = request.POST.get('address')
        obj.gender = request.POST.get('gen')
        obj.age = request.POST.get('age')
        obj.contact = request.POST.get('contact')
        obj.email = request.POST.get('email')
        obj.save()

        ob = Login()
        new_password = generate_random_password()
        ob.username = obj.email  # Using email as the username for login
        ob.password = make_password(new_password) 
        ob.type = 'customer'
        ob.uid = obj.customer_id
        ob.save()

        send_mail(
            'Registration Successful',
            f'Hello {obj.name},\n\nYour request has been accepted. Here are your login credentials:\n\nUsername: {obj.email}\nPassword: {new_password}\n\nPlease note down the password for future reference.',
            'admin@yourorganization.com',
            [obj.email],  
            fail_silently=False,
        )
        obk = "Successfully registered"
        
    context = {
        'msg': obk
    }
    return render(request, 'customer/customer_reg.html', context)

def generate_random_password(length=12):
    """Generate a random password with letters and digits."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

