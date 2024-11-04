from django.shortcuts import render
from Supplyco_product.models import SupplycoProduct
from ration_registration.models import Shopkeeper
from django.utils import timezone
from datetime import datetime
# Create your views here.

from django.shortcuts import render
from django.utils import timezone
from ration_registration.models import Shopkeeper
from .models import SupplycoProduct

def Supplyco_product(request):
    date_time = timezone.now().strftime("%Y-%m-%d")

    # Get the shopkeeper ID from the session
    supplycoproduct_id = request.session.get("uid")
    error_product_name = ""

    # Check if the shopkeeper exists
    shop_instance = Shopkeeper.objects.filter(pk=supplycoproduct_id).first()

    if not shop_instance:
        # If shop_instance is None, display an error message to the user
        context = {
            'dt': date_time,
            'error_product_name': "Invalid shopkeeper. Please check your session data or log in again.",
        }
        return render(request, 'Supplyco_product/Supplyco_product.html', context)

    if request.method == "POST":
        # Get the product details from the form
        supplycoproduct_name = request.POST.get('product_name')
        expiry_date = request.POST.get('expiry_date')
        manufacture_date = request.POST.get('manufacture_date')
        quantity = request.POST.get('quantity')
        actual_price = request.POST.get('actual_price')
        available_price = request.POST.get('available_price')

        # Check if the product with the same name already exists for the current shop
        if SupplycoProduct.objects.filter(shop=shop_instance, supplycoproduct_name=supplycoproduct_name).exists():
            error_product_name = "This product has already been added to your shop."
        else:
            # Save the new product if it doesn't exist
            obj = SupplycoProduct(
                shop=shop_instance,
                supplycoproduct_name=supplycoproduct_name,
                expiry_date=expiry_date,
                manufacture_date=manufacture_date,
                supplyco_quantity=quantity,
                actual_price=actual_price,
                available_price=available_price
            )
            obj.save()
            msg = "Product successfully added."
            return render(request, 'Supplyco_product/Supplyco_product.html', {'msg': msg, 'dt': date_time})

    # Render the form with any error messages if applicable
    context = {
        'dt': date_time,
        'error_product_name': error_product_name,
    }
    return render(request, 'Supplyco_product/Supplyco_product.html', context)




#def Supplyco_product(request):
 #   date_time = timezone.now().strftime("%Y-%m-%d")
  # if request.method=="POST":
   #     obj=SupplycoProduct()
    #    obj.supplycoproduct_name=request.POST.get('product_name')
     #   obj.expiry_date=request.POST.get('expiry_date')
      #  obj.manufacture_date=request.POST.get('manufacture_date')
       # obj.supplyco_quantity=request.POST.get('quantity')
       # obj.actual_price=request.POST.get('actual_price')
        #obj.available_price=request.POST.get('available_price')
       
        #obj.save()
        #obk = "successfully Added"
    #context = {
     #       'msg': obk,
      #      'dt' : date_time
    #}
    #return render(request,'Supplyco_product/Supplyco_product.html',context)

from django.shortcuts import render
from ration_registration.models import Shopkeeper
from .models import SupplycoProduct

def mscop(request):
    # Get the shopkeeper ID from the session
    supplycoproduct_id = request.session.get("uid")

    # Check if the shopkeeper exists
    shop_instance = Shopkeeper.objects.filter(pk=supplycoproduct_id).first()

    # Fetch only the SupplycoProducts belonging to the current shopkeeper
    if shop_instance:
        obj = SupplycoProduct.objects.filter(shop=shop_instance)
    else:
        obj = SupplycoProduct.objects.none()  # If the shopkeeper doesn't exist, return an empty queryset

    context = {
        'dd': obj
    }
    
    return render(request, 'Supplyco_product/manage_supplycop.html', context)



from django.shortcuts import render, get_object_or_404

def update(request, idd):
    obj = get_object_or_404(SupplycoProduct, supplycoproduct_id=idd)    
    now = timezone.now().strftime("%Y-%m-%d")
    error_product_name = ""

    if request.method == "POST":
        supplycoproduct_name = request.POST.get('sp')
        manufacture_date = request.POST.get('md')
        expiry_date = request.POST.get('ed')
        quantity = request.POST.get('qt')
        actual_price = request.POST.get('acp')
        available_price = request.POST.get('avp')

        # Check for duplicate product name (excluding the current object)
        if SupplycoProduct.objects.filter(supplycoproduct_name=supplycoproduct_name).exclude(supplycoproduct_id=idd).exists():
            error_product_name = "Product name already exists."
        else:
            # Update the object
            obj.supplycoproduct_name = supplycoproduct_name
            obj.manufacture_date = manufacture_date
            obj.expiry_date = expiry_date
            obj.supplyco_quantity = quantity
            obj.actual_price = actual_price
            obj.available_price = available_price
            obj.save()
            
            return mscop(request)

    # Render with error message if there's a duplicate
    context = {
        'dd': obj,
        'dt': now,
        'error_product_name': error_product_name,
    }
    
    return render(request, 'Supplyco_product/update.html', context)


def delete(request,idd):
    obj=SupplycoProduct.objects.get(supplycoproduct_id=idd)
    obj.delete()
    return  mscop(request)