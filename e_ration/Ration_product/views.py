from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
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

def mrp(request):
    obj=RationProduct.objects.all()
    context={
        'dd':obj
    }
    return render(request,'Ration_product/manage_Rationp.html',context)

def update(request,idd):
    obj = RationProduct.objects.get(rationproduct_id=idd)
    context = {
        'dd': obj
    }
    if request.method=="POST":
        obj=RationProduct.objects.get(rationproduct_id=idd)
        obj.card_type=request.POST.get('ct')
        obj.card_color=request.POST.get('cc')
        obj.product_name=request.POST.get('pn')
        obj.quantity=request.POST.get('qt')
        obj.price =request.POST.get('pc')
        obj.save()
        return  mrp(request)
    return render(request,'Ration_product/update.html',context)


def delete(request, idd):
    # Use get_object_or_404 to handle object retrieval
    obj = get_object_or_404(RationProduct, rationproduct_id=idd)
    
    # Delete the object
    obj.delete()
    return mrp(request)
    # Redirect to a success page or list view
    #return redirect('Ration_product/manage_Rationp.html')  # Update with your actual view name
