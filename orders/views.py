from django.shortcuts import render, redirect
from .models import Product, Order, Cart
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def home(request):
    return redirect("dashboard")


def product_list(request):
    search = request.GET.get("search")

    if search:
        products = Product.objects.filter(name__icontains=search)
    else:
        products = Product.objects.all()

    return render(request, "orders/product_list.html", {"products": products})

    
def add_product(request):
    if request.method == "POST":
        name = request.POST["name"]
        price = request.POST["price"]
        quantity = request.POST["quantity"]

        Product.objects.create(
            name=name,
            price=price,
            quantity=quantity
        )

        return redirect("product_list")

    return render(request, "orders/add_product.html")

def edit_product(request, id):
    product = Product.objects.get(id=id)

    if request.method == "POST":
        product.name = request.POST["name"]
        product.price = request.POST["price"]
        product.quantity = request.POST["quantity"]
        product.save()

        return redirect("product_list")

    return render(request, "orders/edit_product.html", {"product": product})    

def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect("product_list")  

def user_login(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("user_dashboard")

        else:

            return render(
                request,
                "orders/login.html",
                {
                    "error": "Invalid username or password!"
                }
            )

    return render(request, "orders/login.html")


from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    return redirect("login")


def add_order(request):
    if request.method == "POST":
        customer_name = request.POST["customer_name"]
        product_id = request.POST["product"]
        quantity = int(request.POST["quantity"])
        status = request.POST.get("status")

        product = Product.objects.get(id=product_id)

        if product.quantity >= quantity:

            Order.objects.create(
                customer_name=customer_name,
                product=product,
                quantity=quantity,
                status=status
            )

            # Reduce stock
            product.quantity -= quantity
            product.save()

            return redirect("view_orders")

        else:
            products = Product.objects.all()
            return render(request, "orders/add_order.html", {
                "products": products,
                "error": "Not enough stock available!"
            })

    products = Product.objects.all()
    return render(request, "orders/add_order.html", {
        "products": products
    })

def view_orders(request):
    search = request.GET.get("search")

    if search:
        orders = Order.objects.filter(customer_name__icontains=search)
    else:
        orders = Order.objects.all()

    return render(request, "orders/view_orders.html", {
        "orders": orders
    })

def delete_order(request, id):
    order = Order.objects.get(id=id)

    if request.method == "POST":
        order.delete()
        return redirect('view_orders')

    return render(request, "orders/delete_order.html", {
        "order": order
    })

from django.shortcuts import get_object_or_404

def delete_product(request, id):
    product = Product.objects.get(id=id)

    if request.method == "POST":
        product.delete()
        return redirect('view_products')

    return render(request, "orders/delete_product.html", {
        "product": product
    })


def edit_order(request, id):
    order = get_object_or_404(
        Order,
        id=id
    )

    if request.method == "POST":
        order.customer_name = request.POST["customer_name"]

        order.product = Product.objects.get(
            id=request.POST["product"]
        )

        order.quantity = request.POST["quantity"]

        order.status = request.POST["status"]

        order.save()

        return redirect("view_orders")

    products = Product.objects.all()

    return render(
        request,
        "orders/edit_order.html",
        {
            "order": order,
            "products": products
        }
    )

from django.db.models import F, Sum
from .models import Product, Order

@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect("user_dashboard")

    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.filter(is_staff=False).count()
    pending_orders = Order.objects.filter(status="Pending").count()
    confirmed_orders = Order.objects.filter(status="Confirmed").count()
    processing_orders = Order.objects.filter(status="Processing").count()
    shipped_orders = Order.objects.filter(status="Shipped").count()
    delivered_orders = Order.objects.filter(status="Delivered").count()
    total_revenue = (
        Order.objects
        .annotate(total=F("quantity") * F("product__price"))
        .aggregate(total_revenue=Sum("total"))["total_revenue"]
        or 0
    )

    
    low_stock = Product.objects.filter(quantity__lt=5)
    recent_orders = Order.objects.all().order_by("-id")[:5]

    for order in recent_orders:
      order.total_price = order.product.price * order.quantity


    products = Product.objects.all()

    product_names = []
    product_quantities = []

    for product in products:
        product_names.append(product.name)
        product_quantities.append(product.quantity)

    context = {
        "total_products": total_products,
        "total_orders": total_orders,
        "total_users": total_users,
        "total_revenue": total_revenue,

        "pending_orders": pending_orders,
        "confirmed_orders": confirmed_orders,
        "processing_orders": processing_orders,
        "shipped_orders": shipped_orders,
        "delivered_orders": delivered_orders,

        "low_stock": low_stock,
        "recent_orders": recent_orders,
        "product_names": product_names,
        "product_quantities": product_quantities,
    }

    return render(request, "orders/dashboard.html", context)

def view_products(request):
    search = request.GET.get("search")

    if search:
        products = Product.objects.filter(name__icontains=search)
    else:
        products = Product.objects.all()

    return render(request, "orders/view_products.html", {
        "products": products
    })

@login_required
def invoice(request, id):

    order = Order.objects.filter(id=id).first()

    if order is None:
        return redirect("my_orders")

    if not request.user.is_staff:
        if order.user != request.user:
            return redirect("my_orders")

    total = order.quantity * order.product.price

    return render(
        request,
        "orders/invoice.html",
        {
            "order": order,
            "total": total,
        }
    )

def profile(request):
    return render(request, "orders/profile.html")

def welcome(request):
    return render(request, "orders/welcome.html")

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request=request,
            username=username,
            password=password
        )

        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect("dashboard")
            else:
                return render(
                    request,
                    "orders/admin_login.html",
                    {
                        "error": "This account is not an admin account."
                    }
                )

        else:
            return render(
                request,
                "orders/admin_login.html",
                {
                    "error": "Invalid username or password."
                }
            )

    return render(request, "orders/admin_login.html")

def create_account(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():

            return render(request, "orders/create_account.html", {
                "error": "Username already exists!"
            })

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect("login")

    return render(request, "orders/create_account.html")

from django.contrib.auth.decorators import login_required


@login_required
def user_dashboard(request):
    products = Product.objects.all()

    return render(
        request,
        "orders/user_dashboard.html",
        {
            "products": products
        }
    )
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

def cart(request):
   cart_items = request.session.get('cart', [])

   
   items = []
   total_amount = 0

   for item in cart_items:
    try:
        product = Product.objects.get(id=item['product_id'])
        quantity = item['quantity']
        total = product.price * quantity

        items.append({
            'product': product,
            'quantity': quantity,
            'total': total
        })

        total_amount += total

    except Product.DoesNotExist:
        pass

   return render(request, 'orders/cart.html', {
    'cart_items': items,
    'total_amount': total_amount
  })

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    cart = request.session.get('cart', [])

    found = False

    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] += 1
            found = True
            break

    if not found:
        cart.append({
            'product_id': product_id,
            'quantity': 1
        })

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])

    cart = [
        item for item in cart
        if item['product_id'] != product_id
    ]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')

def increase_cart_quantity(request, product_id):
    cart = request.session.get('cart', [])

    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] += 1
            break

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def decrease_cart_quantity(request, product_id):
    cart = request.session.get('cart', [])

    for item in cart:
        if item['product_id'] == product_id:
            if item['quantity'] > 1:
                item['quantity'] -= 1
            break

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')

@login_required
def place_order(request):
    if request.method == "POST":
        customer_name = request.POST.get("customer_name")

        cart = request.session.get("cart", [])

        for item in cart:
            try:
                product = Product.objects.get(
                    id=item["product_id"]
                )

                quantity = item["quantity"]

                if quantity <= product.quantity:

                    Order.objects.create(
                        user=request.user,
                        customer_name=customer_name,
                        product=product,
                        quantity=quantity
                    )

                    product.quantity -= quantity
                    product.save()

            except Product.DoesNotExist:
                pass

        request.session["cart"] = []
        request.session.modified = True

        return redirect("my_orders")

    return render(
        request,
        "orders/place_order.html"
    )
    return render(request, 'orders/place_order.html')

@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-id")

    for order in orders:
        order.total_price = (
            order.product.price * order.quantity
        )

    return render(
        request,
        "orders/my_orders.html",
        {
            "orders": orders
        }
    )
@login_required
def track_order(request, id):

    order = get_object_or_404(
        Order,
        id=id
    )

    if not request.user.is_staff:
        if order.user != request.user:
            return redirect("my_orders")

    return render(
        request,
        "orders/track_order.html",
        {
            "order": order
        }
    )

@login_required
def user_list(request):

    if not request.user.is_staff:
        return redirect("user_dashboard")

    search = request.GET.get("search")

    if search:
        users = User.objects.filter(
            is_staff=False,
            username__icontains=search
        ).order_by("-date_joined")

    else:
        users = User.objects.filter(
            is_staff=False
        ).order_by("-date_joined")

    return render(
        request,
        "orders/user_list.html",
        {
            "users": users,
            "search": search
        }
    )

@login_required
def toggle_user_status(request, id):

    if not request.user.is_staff:
        return redirect("user_dashboard")

    user = get_object_or_404(
        User,
        id=id
    )

    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True

    user.save()

    return redirect("user_list")