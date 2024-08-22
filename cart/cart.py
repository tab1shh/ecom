from store.models import Product, Profile


class Cart:
    def __init__(self, request):
        # initalize the session object
        self.session = request.session

        # get request
        self.request = request

        # get the current cart from the session or create a new cart if none exists
        cart = self.session.get("session_key")

        # if cart doesnt exist in the session, create an empty cart
        if "session_key" not in request.session:
            cart = self.session["session_key"] = {}

        # make sure cart is on all pages of site by assigning to instance var
        self.cart = cart

    def db_add(self, product, quantity):
        # convert to str for consistency
        product_id = str(product)
        product_qty = str(quantity)

        # if the product is already in the cart, do nothing
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {"price": str(product.price)}
            # add the product to the cart with the specified quantity
            self.cart[product_id] = int(product_qty)
        # mark the session as modified to save changes
        self.session.modified = True

        # deal with logged in user
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("'", '"')
            current_user.update(old_cart=str(carty))

    def add(self, product, quantity):
        # convert to str for consistency
        product_id = str(product.id)
        product_qty = str(quantity)

        # if the product is already in the cart, do nothing
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {"price": str(product.price)}
            # add the product to the cart with the specified quantity
            self.cart[product_id] = int(product_qty)
        # mark the session as modified to save changes
        self.session.modified = True

        # deal with logged in user
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("'", '"')
            current_user.update(old_cart=str(carty))

    # returns number of items in cart
    def __len__(self):
        return len(self.cart)

    def cart_total(self):
        # get product IDs from cart
        product_ids = self.cart.keys()

        # lookup products in DB using the IDs
        products = Product.objects.filter(id__in=product_ids)

        # get quantities
        quantities = self.cart

        # starting counting at 0
        total = 0

        # calc the total cost in cart
        for key, value in quantities.items():
            # convert key(ID) string to int
            key = int(key)
            for product in products:
                if product.id == key:
                    # calc cost based on if product is on sale or not
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total

    def get_prods(self):
        # get ids from cart
        product_ids = self.cart.keys()

        # use ids to lookup products in data base model
        products = Product.objects.filter(id__in=product_ids)

        # return looked up products
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # update cart with new quantity for the product
        ourcart = self.cart

        # update cart/dict
        ourcart[product_id] = product_qty

        # mark the session as modified to save changes
        self.session.modified = True

        # deal with logged in user
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("'", '"')
            current_user.update(old_cart=str(carty))

        # return the updated cart
        return self.cart

    def delete(self, product):
        product_id = str(product)

        # remove item from cart
        if product_id in self.cart:
            del self.cart[product_id]

        # mark the session as modified to save changes
        self.session.modified = True

        # deal with logged in user
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("'", '"')
            current_user.update(old_cart=str(carty))
