from django.shortcuts import render
from Supplyco_product.models import SupplycoProduct
from django.utils import timezone
from datetime import datetime
# Create your views here.

def Supplyco_product(request):
    date_time = timezone.now().strftime("%Y-%m-%d")
    obk = ""
    
    if request.method == "POST":
        # Get the product details from the form
        product_name = request.POST.get('product_name')
        expiry_date = request.POST.get('expiry_date')
        manufacture_date = request.POST.get('manufacture_date')
        quantity = request.POST.get('quantity')
        actual_price = request.POST.get('actual_price')
        available_price = request.POST.get('available_price')
        
        # Check if the product with the same name already exists
        if SupplycoProduct.objects.filter(supplycoproduct_name=product_name).exists():
            obk = f"Product '{product_name}' already exists. Cannot add the same product again."
        else:
            # If the product doesn't exist, save the new product
            obj = SupplycoProduct(
                supplycoproduct_name=product_name,
                expiry_date=expiry_date,
                manufacture_date=manufacture_date,
                supplyco_quantity=quantity,
                actual_price=actual_price,
                available_price=available_price
            )
            obj.save()
            obk = "Product successfully added."
    
    context = {
        'msg': obk,
        'dt': date_time
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

def mscop(request):
    obj=SupplycoProduct.objects.all()
    context={
        'dd':obj
    }
    return render(request,'Supplyco_product/manage_supplycop.html',context)


def update(request,idd):
    obj = SupplycoProduct.objects.get(supplycoproduct_id=idd)    
    now = timezone.now().strftime("%Y-%m-%d")
    if request.method=="POST":
       # obj=SupplycoProduct.objects.get(supplycoproduct_id=idd)
       
        obj.supplycoproduct_name=request.POST.get('sp')
        obj.manufacture_date=request.POST.get('md')
        obj.expiry_date=request.POST.get('ed')
        obj.supplyco_quantity=request.POST.get('qt')
        obj.actual_price =request.POST.get('acp')
        obj.available_price =request.POST.get('avp')
        obj.save()
    
        return  mscop(request)
    context = {
        'dd': obj,
        'dt' : now
    }
    return render(request,'Supplyco_product/update.html',context)

def delete(request,idd):
    obj=SupplycoProduct.objects.get(supplycoproduct_id=idd)
    obj.delete()
    return  mscop(request)