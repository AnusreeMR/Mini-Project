from django.shortcuts import render,redirect
from ration_registration.models import Shopkeeper
from product.models import Product
from Supplyco_product.models import SupplycoProduct
from Ration_product.models import RationProduct
from django.utils import timezone
from Cart_product.models import CartProduct
from Cart.models import Cart
from customer.models import CustomerRegistration
from stock.models import Stock
from Supplyco_product.models import SupplycoProduct
# Create your views here.

def remove_old_cart_items():
    # Calculate the threshold time
    threshold = timezone.now() - timezone.timedelta(hours=24)
    # Remove products older than 24 hours
    CartProduct.objects.filter(date_added__lt=threshold).delete()



def add_to_cart(request, idd):
    # Retrieve the customer ID from the session
    customer_id = request.session.get("uid")
    if not customer_id:
        return redirect('login')

    # Fetch the customer instance
    customer_instance = CustomerRegistration.objects.get(pk=customer_id)

    # Retrieve the supplyco product based on the provided ID
    supplyco_product = SupplycoProduct.objects.get(supplycoproduct_id=idd)

    # Check if the product is available in stock
    if supplyco_product.supplyco_quantity <= 0:
        # Handle the case where the product is out of stock
        return redirect('view_cart')  # Or show an error message

    # Retrieve or create a cart for this customer with default values
    user_cart, created = Cart.objects.get_or_create(
        customer=customer_instance,
        defaults={'total_amount': 0.00, 'date': timezone.now().date()}
    )

    # Check if the product is already in the cart
    cart_product = CartProduct.objects.filter(cart=user_cart, supplycoproduct=supplyco_product).first()

    if cart_product:  # If the product already exists in the cart
        cart_product.quantity += 1
        cart_product.save()
    else:
        # Create a new cart product entry if it does not exist
        CartProduct.objects.create(
            cart=user_cart,
            supplycoproduct=supplyco_product,
            quantity=1,
            shop=supplyco_product.shop,  # Add the shop if applicable
            customer=customer_instance,  # Ensure customer is associated
            date_added=timezone.now()  # Add the date
        )

    # Reduce the stock quantity by 1
    supplyco_product.supplyco_quantity -= 1
    supplyco_product.save()

    # Redirect to the view cart page
    return redirect('view_cart')






def product_search(request):
    product_name = request.GET.get('product_name', '').strip()
    shops = []

    if product_name:
        # Search for Supplyco products
        supplyco_products = SupplycoProduct.objects.filter(supplycoproduct_name__icontains=product_name)
        supplyco_product_ids = supplyco_products.values_list('supplycoproduct_id', flat=True)

        # Search for Ration products
        ration_products = RationProduct.objects.filter(product_name__icontains=product_name)
        ration_product_ids = ration_products.values_list('rationproduct_id', flat=True)

        # Find shops for Supplyco products
        if supplyco_product_ids:
            supplyco_shops = Shopkeeper.objects.filter(supplycoproduct__in=supplyco_product_ids)
            shops.extend(supplyco_shops)  # Use extend to add multiple shops

        # Find shops for Ration products
        if ration_product_ids:
            ration_shops = Shopkeeper.objects.filter(stock__rationproduct__in=ration_product_ids)
            shops.extend(ration_shops)  # Use extend to add multiple shops

    # Remove duplicates from shops
    shops = list(set(shops))

    return render(request, 'product/product_search.html', {'shops': shops, 'product_name': product_name})

def search_ration_shop(request):
    # Fetch only accepted shopkeepers
    shops = Shopkeeper.objects.filter(status='accepted')
    dd = []  # Changed from products to dd
    card_types = []
    card_colors = []
    
    shop_id = request.GET.get('shop_id')
    product_type = request.GET.get('product_type')
    selected_card_type = request.GET.get('card_type')
    selected_card_color = request.GET.get('card_color')

    if request.method == 'GET' and shop_id and product_type:
        if product_type == 'ration':
            # Fetch ration products related to the selected shop
            ration_products = RationProduct.objects.filter(stock__shop__shop_id=shop_id)

            # Fetch unique card types and card colors for the selected shop
            card_types = ration_products.values_list('card_type', flat=True).distinct()
            card_colors = ration_products.values_list('card_color', flat=True).distinct()

            # Filter products based on selected card type if provided
            if selected_card_type:
                ration_products = ration_products.filter(card_type=selected_card_type)

            # Filter products based on selected card color if provided
            if selected_card_color:
                ration_products = ration_products.filter(card_color=selected_card_color)

            # Format products for display including product name, card type, card color, quantity, and price
            for i in ration_products:  # Changed from product to i
                stock_item = i.stock_set.filter(shop__shop_id=shop_id).first()  # Changed product to i
                quantity = stock_item.stock_quantity if stock_item else 0  # Handle case when no stock is found
                price = i.price  # Assuming you have a price attribute in your RationProduct model
                dd.append({  # Changed from products to dd
                    'name': i.product_name,  # Changed from product to i
                    'card_type': i.card_type,  # Changed from product to i
                    'card_color': i.card_color,  # Changed from product to i
                    'quantity': quantity,
                    'price': price,
                })

        elif product_type == 'supplyco':
            # Fetch Supplyco products related to the selected shop
            supplyco_products = SupplycoProduct.objects.filter(shop__shop_id=shop_id)
            # Format products for display including product name, quantity, actual price, and available price
            for i in supplyco_products:  # Changed from product to i
                dd.append({  # Changed from products to dd
                    'name': i.supplycoproduct_name,  # Changed from product to i
                    'quantity': i.supplyco_quantity,
                    'actual_price': i.actual_price,
                    'available_price': i.available_price,
                    'supplycoproduct_id': i.supplycoproduct_id,
                })

    context = {
        'shops': shops,
        'dd': dd,  # Changed from products to dd
        'card_types': card_types,
        'card_colors': card_colors,
        'shop_id': shop_id,
        'product_type': product_type,
        'selected_card_type': selected_card_type,
        'selected_card_color': selected_card_color,
    }

    return render(request, 'product/search_ration_shop.html', context)


