from django.shortcuts import render
from Supplyco_product.models import SupplycoProduct

# Create your views here.

def Supplyco_product(request):
    obk=""
    if request.method=="POST":
        obj=SupplycoProduct()
        obj.supplycoproduct_name=request.POST.get('Product Name')
        obj.expiry_date=request.POST.get('Expiry Date')
        obj.manufacture_date=request.POST.get('Manufacture Date')
        obj.quantity=request.POST.get('Quantity')
        obj.actual_price=request.POST.get('Actual price')
        obj.available_price=request.POST.get('Available price')
       
        obj.save()
        obk = "successfully Added"
    context = {
            'msg': obk
    }
    return render(request,'Supplyco_product/Supplyco_product.html',context)

def msp(request):
    obj=SupplycoProduct.objects.all()
    context={
        'dd':obj
    }
    return render(request,'Supplyco_product/manage_supplycop.html',context)


def update(request,idd):
    obj = SupplycoProduct.objects.get(supplycoproduct_id=idd)
    context = {
        'dd': obj
    }
    if request.method=="POST":
        obj=SupplycoProduct.objects.get(supplycoproduct_id=idd)
        obj.supplycoproduct_name=request.POST.get('sp')
        obj.manufacture_date=request.POST.get('md')
        obj.expiry_date=request.POST.get('ed')
        obj.quantity=request.POST.get('qt')
        obj.actual_price =request.POST.get('acp')
        obj.available_price =request.POST.get('avp')
        obj.save()
        return  msp(request)
    return render(request,'Supplyco_product/update.html',context)

def delete(request,idd):
    obj=SupplycoProduct.objects.get(supplycoproduct_id=idd)
    obj.delete()
    return  msp(request)