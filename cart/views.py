from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):
    # initialize th cart object
    cart = Cart(request)
    # get the products, quantities, and total from the cart
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    # render the html with the cart data
    return render(
        request,
        "cart_summary.html",
        {"cart_products": cart_products, "quantities": quantities, "totals": totals},
    )


def cart_add(request):
    # initialize th cart object
    cart = Cart(request)
    # check if the request method is 'POST' and the action is 'post'
    if request.POST.get("action") == "post":
        # get product ID and qty from the POST data
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))

        # lookup product in database, or return 404 if not found
        product = get_object_or_404(Product, id=product_id)

        # add the product to the cart with the specified quantity (save to session)
        cart.add(product=product, quantity=product_qty)

        # get cart quantity
        cart_quantity = cart.__len__()

        # return response
        # response = JsonResponse({"Product Name: ": product.name})
        # return json with updated cart qty, and give success message
        response = JsonResponse({"qty": cart_quantity})
        messages.success(request, ("Product Added To Cart..."))
        return response


def cart_delete(request):
    # initialize th cart object
    cart = Cart(request)

    # check if the request method is 'POST' and the action is 'post'
    if request.POST.get("action") == "post":
        # get product ID from the POST data
        product_id = int(request.POST.get("product_id"))

        cart.delete(product=product_id)

        # return a JSON response with the ID of the deleted product, and a success message
        response = JsonResponse({"product": product_id})
        messages.success(request, ("Item Deleted From Cart..."))
        return response


def cart_update(request):
    # initialize th cart object
    cart = Cart(request)

    # check if the request method is 'POST' and the action is 'post'
    if request.POST.get("action") == "post":
        # get product ID and qty from the POST data
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))

        cart.update(product=product_id, quantity=product_qty)

        # return a JSON response with updated qty, and a success message
        response = JsonResponse({"qty": product_qty})
        messages.success(request, ("Your Cart Has Been Updated..."))
        return response
