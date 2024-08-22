from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product
import datetime


def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST["shipping_status"]
            if status == "true":
                # get the order
                order = Order.objects.filter(id=pk)
                # update status
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                # get the order
                order = Order.objects.filter(id=pk)
                # update status
                order.update(shipped=False)
            messages.success(request, "Shipping Status Updated")
            return redirect("home")

        return render(request, "payment/orders.html", {"order": order, "items": items})

    else:
        messages.success(request, "Access Denied")
        return redirect("home")


def not_shipped_dash(request):

    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST["shipping_status"]
            num = request.POST["num"]
            order = Order.objects.filter(id=num)

            now = datetime.datetime.now()
            order.update(shipped=True, date_shipped=now)

            messages.success(request, "Shipping Status Updated")
            return redirect("/payment/not_shipped_dash")

        return render(request, "payment/not_shipped_dash.html", {"orders": orders})
    else:
        messages.success(request, "Access Denied")
        return redirect("home")


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST["shipping_status"]
            num = request.POST["num"]
            order = Order.objects.filter(id=num)

            now = datetime.datetime.now()
            order.update(shipped=False)

            messages.success(request, "Shipping Status Updated")
            return redirect("/payment/shipped_dash")

        return render(request, "payment/shipped_dash.html", {"orders": orders})
    else:
        messages.success(request, "Access Denied")
        return redirect("home")


def process_order(request):
    if request.POST:
        cart = Cart(request)
        # get the products, quantities, and total from the cart
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # get billing info from last page
        payment_form = PaymentForm(request.POST or None)
        # get shipping session data
        my_shipping = request.session.get("my_shipping")

        full_name = my_shipping["shipping_full_name"]
        email = my_shipping["shipping_email"]

        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}\n"
        amount_paid = totals

        # create order
        if request.user.is_authenticated:
            user = request.user
            create_order = Order(
                user=user,
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=amount_paid,
            )
            create_order.save()
            # get order ID and product info
            order_id = create_order.pk
            for product in cart_products():
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                # get qty
                for key, value in quantities().items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(
                            order_id=order_id,
                            product_id=product_id,
                            user=user,
                            quantity=value,
                            price=price,
                        )
                        create_order_item.save()
                        # delete cart
                for key in list(request.session.keys()):
                    if key == "session_key":
                        del request.session[key]
            messages.success(request, "Order Placed")
            return redirect("home")
        else:
            create_order = Order(
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=amount_paid,
            )
            create_order.save()

            order_id = create_order.pk
            for product in cart_products():
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                # get qty
                for key, value in quantities().items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(
                            order_id=order_id,
                            product_id=product_id,
                            quantity=value,
                            price=price,
                        )
                        create_order_item.save()

            # delete cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            messages.success(request, "Order Placed")
            return redirect("home")
    else:
        messages.success(request, "Access Denied")
        return redirect("home")


def billing_info(request):
    if request.POST:
        cart = Cart(request)
        # get the products, quantities, and total from the cart
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        my_shipping = request.POST
        request.session["my_shipping"] = my_shipping

        # check if user is logged in
        if request.user.is_authenticated:
            billing_form = PaymentForm
            return render(
                request,
                "payment/billing_info.html",
                {
                    "cart_products": cart_products,
                    "quantities": quantities,
                    "totals": totals,
                    "shipping_info": request.POST,
                    "billing_form": billing_form,
                },
            )
        else:
            billing_form = PaymentForm
            return render(
                request,
                "payment/billing_info.html",
                {
                    "cart_products": cart_products,
                    "quantities": quantities,
                    "totals": totals,
                    "shipping_info": request.POST,
                    "billing_form": billing_form,
                },
            )

        shipping_form = request.POST

        return render(
            request,
            "payment/billing_info.html",
            {
                "cart_products": cart_products,
                "quantities": quantities,
                "totals": totals,
                "shipping_form": shipping_form,
            },
        )
    else:
        messages.success(request, "Access Denied")
        return redirect("home")


def payment_success(request):
    return render(request, "payment/payment_success.html", {})


def checkout(request):
    cart = Cart(request)
    # get the products, quantities, and total from the cart
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    # cehckout as logged in user
    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(
            request,
            "payment/checkout.html",
            {
                "cart_products": cart_products,
                "quantities": quantities,
                "totals": totals,
                "shipping_form": shipping_form,
            },
        )
    else:

        # checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(
            request,
            "payment/checkout.html",
            {
                "cart_products": cart_products,
                "quantities": quantities,
                "totals": totals,
                "shipping_form": shipping_form,
            },
        )
