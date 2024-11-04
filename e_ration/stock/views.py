from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from stock.models import Stock
from Ration_product.models import RationProduct
from ration_registration.models import Shopkeeper

# Create your views here.

def Rskp(request):
    stock_id = request.session.get("uid")
    shop_instance = Shopkeeper.objects.filter(pk=stock_id).first()

    if request.method == 'POST':
        # Get the selected values from the form
        selected_card_type = request.POST.get('card_type')
        selected_card_color = request.POST.get('card_color')
        selected_product_name = request.POST.get('product_name')
        stock_quantity = request.POST.get('quantity')

        # Fetch the RationProduct based on the selected values
        ration_products = RationProduct.objects.filter(
            card_type=selected_card_type,
            card_color=selected_card_color,
            product_name=selected_product_name
        )

        if ration_products.exists():
            # Select the first RationProduct if multiple exist
            obk = ration_products.first()

            # Check if the same product already exists in stock for the shop
            if Stock.objects.filter(shop=shop_instance, rationproduct=obk).exists():
                msg = "This product is already in stock for your shop."
            else:
                # Create and save a new Stock object with the shop instance
                stock_item = Stock(
                    shop=shop_instance,  # Associate Stock with the selected Shopkeeper
                    rationproduct=obk,   # Associate Stock with the selected RationProduct
                    stock_quantity=stock_quantity,
                )
                stock_item.save()
                msg = "Product stock added successfully!"
        else:
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
    # Get the shopkeeper ID from the session
    shopkeeper_id = request.session.get("uid")

    # Retrieve the shopkeeper instance
    shop_instance = Shopkeeper.objects.filter(pk=shopkeeper_id).first()

    # Retrieve all stock items for the specific shopkeeper
    if shop_instance:
        stock_items = Stock.objects.filter(shop=shop_instance)  # Filter stock by shop
    else:
        stock_items = Stock.objects.none()  # No stock if shopkeeper not found

    context = {
        'dd': stock_items  # Pass only the stock items for the shopkeeper
    }
    
    return render(request, 'stock/mng_rp.html', context)

def update_stock(request, idd):
    obj = Stock.objects.get(stock_id=idd)
    
    if request.method == "POST":
        obj.stock_quantity = request.POST.get('stock_quantity')
        #obj.stock_price = request.POST.get('stock_price')
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