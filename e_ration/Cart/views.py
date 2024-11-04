from django.shortcuts import render, redirect

# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from Cart.models import Cart
from Cart_product.models import CartProduct
from customer.models import CustomerRegistration

from Supplyco_product.models import SupplycoProduct

from ration_registration.models import Shopkeeper


from django.db.models import Sum, F


def checkout(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')

        try:
            # Fetch the customer by card_no
            customer = CustomerRegistration.objects.get(card_no=customer_id)
            # Get the customer's cart
            cart = Cart.objects.filter(customer=customer).first()  # Get the first cart for this customer

            if cart:
                # Get the cart products for the customer's cart
                cart_products = CartProduct.objects.filter(cart=cart)
                
                # Check if there are any products in the cart
                if cart_products.exists():
                    # Get the shop from the first cart product (assuming all products are from the same shop)
                    shop = cart_products.first().shop
                    
                    # Filter cart products by the shop if needed
                    cart_products = cart_products.filter(shop=shop)  # Only products from the specific shop
                else:
                    cart_products = []  # No products in the cart
                    shop = None  # No shop

                # Calculate total amount and add price for each item
                total_amount = 0
                for item in cart_products:
                    item.price = item.supplycoproduct.available_price * item.quantity  # Calculate total price for each item
                    total_amount += item.price  # Sum total amount

                # Update the cart's total amount if needed
                cart.total_amount = total_amount  # Update the cart's total amount
                cart.save()  # Save the updated cart

                return render(request, 'Cart/checkout.html', {
                    'customer': customer,
                    'cart_products': cart_products,
                    'total_amount': total_amount,
                })

            else:
                return render(request, 'Cart/checkout.html', {'error': 'No cart found for this customer.'})

        except CustomerRegistration.DoesNotExist:
            return render(request, 'Cart/checkout.html', {'error': 'Customer not found.'})

    # Redirect or handle GET requests as needed
    return redirect('shopkeeper_cart')









def shopkeeper_cart(request):
    # Retrieve the shopkeeper's ID from the session
    shop_id = request.session.get("uid")

    # Check if the shopkeeper exists; if not, return a 404 error
    shop_instance = get_object_or_404(Shopkeeper, pk=shop_id)

    # Initialize search query
    search_query = request.GET.get('search', '').strip()

    # Fetch all customers who added products to the cart for this specific ration shop
    cart_products = CartProduct.objects.filter(shop=shop_instance).select_related('customer', 'supplycoproduct')

    # Organize data by customer
    customer_data = {}
    for cart_product in cart_products:
        customer = cart_product.customer
        if customer.customer_id not in customer_data:
            customer_data[customer.customer_id] = {
                'card_no': customer.card_no,  # Should be a string
                'name': customer.name,         # Should be a string
                'contact': customer.contact,    # Should be a string
                'items': [],
                'total_amount': 0              # Initialize total amount for the customer
            }
        # Add product details to the customer's items
        customer_data[customer.customer_id]['items'].append({
            'product': cart_product.supplycoproduct.supplycoproduct_name,
            'quantity': cart_product.quantity,
            'price': cart_product.supplycoproduct.available_price,
        })

        # Update the total amount for the customer
        customer_data[customer.customer_id]['total_amount'] += cart_product.quantity * cart_product.supplycoproduct.available_price

    # Filter customers based on search query
    if search_query:
        customer_data = {
            cust_id: details for cust_id, details in customer_data.items()
            if (search_query.lower() in details['name'].lower() or 
                search_query in str(details['card_no']))  # Convert card_no to string
        }

    context = {
        'customer_details': customer_data,
        'search_query': search_query,  # Include the search query in context for display
    }

    return render(request, 'Cart/shopkeeper_cart.html', context)


def view_cart(request):
    # Ensure the user is logged in and fetch their cart
    customer_id = request.session.get("uid")
    if not customer_id:
        return redirect('login')

    # Get the logged-in customer
    customer_instance = get_object_or_404(CustomerRegistration, pk=customer_id)

    # Get or create the user's cart
    user_cart, created = Cart.objects.get_or_create(
        customer=customer_instance,
        defaults={'total_amount': 0.00, 'date': timezone.now()}
    )

    # Calculate the expiration time (24 hours ago)
    expiration_time = timezone.now() - timedelta(hours=24)

    # Delete cart products that were added more than 24 hours ago
    CartProduct.objects.filter(cart=user_cart, date_added__lt=expiration_time).delete()

    # Fetch remaining valid cart items and calculate total for each item
    cart_items = CartProduct.objects.filter(cart=user_cart)
    for item in cart_items:
        item.total_price = item.quantity * item.supplycoproduct.available_price  # Calculated total per item

    # Calculate total amount by summing available_price * quantity for each item
    total_amount = sum(item.total_price for item in cart_items)

    # Update total_amount if it differs from the current cart total
    if user_cart.total_amount != total_amount:
        user_cart.total_amount = total_amount
        user_cart.save()

    # Pass the cart items and total amount to the template
    return render(request, 'Cart/view_cart.html', {'cart_items': cart_items, 'total_amount': total_amount})



def remove_from_cart(request, idd):
    # Find the CartProduct item by its ID
    cart_product = CartProduct.objects.filter(cart_product_id=idd).first()
    
    if cart_product:
        # Restore stock quantity for the removed item
        supplyco_product = cart_product.supplycoproduct
        supplyco_product.supplyco_quantity += cart_product.quantity  # Restore stock by the quantity in cart
        supplyco_product.save()

        # Remove the cart product from the cart
        cart_product.delete()  # Directly remove from cart

    # Redirect to the view cart page after removal
    return redirect('view_cart')

def increase_quantity(request, idd):
    cart_product = CartProduct.objects.filter(cart_product_id=idd).first()
    if cart_product:
        # Increase the quantity in the cart
        cart_product.quantity += 1
        cart_product.save()

        # Reduce the stock quantity
        supplyco_product = cart_product.supplycoproduct
        if supplyco_product.supplyco_quantity > 0:
            supplyco_product.supplyco_quantity -= 1
            supplyco_product.save()

    return redirect('view_cart')

def decrease_quantity(request, idd):
    cart_product = CartProduct.objects.filter(cart_product_id=idd).first()
    if cart_product:
        if cart_product.quantity > 1:
            # Decrease the quantity in the cart
            cart_product.quantity -= 1
            cart_product.save()

            # Restore stock quantity for one item
            supplyco_product = cart_product.supplycoproduct
            supplyco_product.supplyco_quantity += 1
            supplyco_product.save()
        else:
            # If the quantity is 1, remove the item from the cart
            supplyco_product = cart_product.supplycoproduct
            supplyco_product.supplyco_quantity += 1  # Restore stock
            supplyco_product.save()
            cart_product.delete()  # Remove from cart

    return redirect('view_cart')