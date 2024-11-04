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
        obj.quantity=request.POST.get('quantity')
        obj.unit=request.POST.get('unit') 
        obj.price=request.POST.get('price')
       
        obj.save()
        obk = "successfully Added"
    context = {
            'msg': obk
    }
    return render(request,'Ration_product/Ration_product.html',context)

from django.shortcuts import render
from .models import RationProduct

def mrp(request):
    # Get search parameters from the request
    card_type = request.GET.get('card_type', '')
    card_color = request.GET.get('card_color', '')
    product_name = request.GET.get('product_name', '')

    # Filter the queryset based on the search parameters
    obj = RationProduct.objects.all()
    if card_type:
        obj = obj.filter(card_type__icontains=card_type)
    if card_color:
        obj = obj.filter(card_color__icontains=card_color)
    if product_name:
        obj = obj.filter(product_name__icontains=product_name)

    # Pass the filtered results to the template
    context = {
        'dd': obj
    }
    return render(request, 'Ration_product/manage_Rationp.html', context)


def update(request,rationproduct_id):
    obj = RationProduct.objects.get(rationproduct_id=rationproduct_id)
    context = {
        'dd': obj
    }
    if request.method=="POST":
        obj=RationProduct.objects.get(rationproduct_id=rationproduct_id)
        obj.card_type=request.POST.get('ct')
        obj.card_color=request.POST.get('cc')
        obj.product_name=request.POST.get('pn')
        obj.quantity=request.POST.get('qt')
        obj.price =request.POST.get('pc')
        obj.unit =request.POST.get('ut')
        obj.save()
        return  mrp(request)
    return render(request,'Ration_product/update.html',context)

def vcard(request):
    card_type_query = request.GET.get('card_type', '')
    card_color_query = request.GET.get('card_color', '')
    
    if card_type_query and card_color_query:
        # Filter based on both card_type and card_color
        obj = RationProduct.objects.filter(card_type__iexact=card_type_query, card_color__iexact=card_color_query)
    else:
        obj = RationProduct.objects.all()
        
    context = {
        'dd': obj
    }
    return render(request, 'Ration_product/view_ration.html', context)


def delete(request, rationproduct_id):
    # Use get_object_or_404 to handle object retrieval
    obj = get_object_or_404(RationProduct, rationproduct_id=rationproduct_id)
    
    # Delete the object
    obj.delete()
    return mrp(request)
    # Redirect to a success page or list view
    #return redirect('Ration_product/manage_Rationp.html')  # Update with your actual view name
