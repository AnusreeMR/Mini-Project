from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from stock.models import Stock
from Ration_product.models import RationProduct

# Create your views here.

def Rskp(request):
    if request.method == 'POST':
        # Get the selected values from the form
        selected_card_type = request.POST['card_type']
        selected_card_color = request.POST['card_color']
        selected_product_name = request.POST['product_name']

        # Fetch the RationProduct based on the selected values, using filter to handle multiple results
        ration_products = RationProduct.objects.filter(
            card_type=selected_card_type,
            card_color=selected_card_color,
            product_name=selected_product_name
        )

        if ration_products.exists():
            # Select the first RationProduct if multiple exist
            obk = ration_products.first()

            # Create and save a new Stock object
            obj = Stock()
            obj.rationproduct = obk  # Associate Stock with the selected RationProduct
            obj.stock_quantity = request.POST['quantity']
            obj.stock_price = request.POST['price']
            obj.save()

            msg = "Product stock added successfully!"
        else:
            # Handle the case when no matching RationProduct is found
            msg = "No matching product found!"

        # Render the template with the form and message
        return render(request, 'stock/add_rp.html', {
            'msg': msg,
            'selected_card_type': selected_card_type,
            'selected_card_color': selected_card_color,
            'selected_product_name': selected_product_name,
            'card_types': RationProduct.objects.values_list('card_type', flat=True).distinct(),
            'card_colors': RationProduct.objects.values_list('card_color', flat=True).distinct(),
            'products': RationProduct.objects.values_list('product_name', flat=True).distinct(),
        })

    else:
        # Fetch distinct values from the database for dropdowns
        card_types = RationProduct.objects.values_list('card_type', flat=True).distinct()
        card_colors = RationProduct.objects.values_list('card_color', flat=True).distinct()
        products = RationProduct.objects.values_list('product_name', flat=True).distinct()

        return render(request, 'stock/add_rp.html', {
            'card_types': card_types,
            'card_colors': card_colors,
            'products': products,
            'msg': '',
            'selected_card_type': '',
            'selected_card_color': '',
            'selected_product_name': ''
        })


#def Rskp(request):
    #obk=""
    #if request.method=="POST":
        #obj=Stock()
        #obj.card_type=request.POST.get('Card Type')
        #obj.card_color=request.POST.get('Card Color')
        #obj.product_name=request.POST.get('product Name')
        #obj.quantity=request.POST.get('Quantity')
        #obj.price=request.POST.get('price')
       
        #obj.save()
        #obk = "Stock Successfully Added"
    #context = {
            #'msg': obk
    #}
    #return render(request,'stock/add_rp.html',context)

def mrskp(request):
    obj=Stock.objects.all()
    context={
        'dd':obj
    }
    return render(request,'stock/mng_rp.html',context)

def update_stock(request, idd):
    obj = Stock.objects.get(stock_id=idd)
    
    if request.method == "POST":
        obj.stock_quantity = request.POST.get('stock_quantity')
        obj.stock_price = request.POST.get('stock_price')
        obj.save()
        return mrskp(request) 
    context = {
        'dd': obj, 
        'card_type': obj.rationproduct.card_type,  
        'card_color': obj.rationproduct.card_color, 
        'product_name': obj.rationproduct.product_name, 
    }
    
    return render(request, 'stock/updt_rp.html', context)


def delete(request,idd):
    obj=Stock.objects.get(stock_id=idd)
    obj.delete()
    return mrskp(request)