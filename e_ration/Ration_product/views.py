from django.shortcuts import render
from Ration_product.models import RationProduct


# Create your views here.

def Ration_product(request):
    obk=""
    if request.method=="POST":
        obj=RationProduct()
        obj.card_type=request.POST.get('Card Type')
        obj.card_color=request.POST.get('Card Color')
        obj.product_name=request.POST.get('product Name')
        obj.quantity=request.POST.get('Quantity')
        obj.price=request.POST.get('price')
       
        obj.save()
        obk = "successfully Added"
    context = {
            'msg': obk
    }
    return render(request,'Ration_product/Ration_product.html',context)