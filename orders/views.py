from django.shortcuts import render, redirect
from .models import Product, Order
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

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
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")   # We'll create this URL if it doesn't exist
        else:
            return render(request, "login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "login.html") 

def home(request):
    return render(request, "home.html") 

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
    order = get_object_or_404(Order, id=id)

    if request.method == "POST":
        order.customer_name = request.POST["customer_name"]
        order.product = Product.objects.get(id=request.POST["product"])
        order.quantity = request.POST["quantity"]
        order.save()

        return redirect("view_orders")

    products = Product.objects.all()

    return render(request, "orders/edit_order.html", {
        "order": order,
        "products": products
    })

from django.db.models import F, Sum
from .models import Product, Order

def dashboard(request):
    total_products = Product.objects.count()
    total_orders = Order.objects.count()

    total_revenue = (
        Order.objects
        .annotate(total=F("quantity") * F("product__price"))
        .aggregate(total_revenue=Sum("total"))["total_revenue"]
        or 0
    )

    low_stock = Product.objects.filter(quantity__lt=5)

    recent_orders = Order.objects.all().order_by('-id')[:5]
    
    products = Product.objects.all()

    product_names = []
    product_quantities = []

    for product in products:
      product_names.append(product.name)
      product_quantities.append(product.quantity)
    context = {
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
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

def invoice(request, id):
    order = Order.objects.get(id=id)

    total = order.quantity * order.product.price

    context = {
        "order": order,
        "total": total,
    }

    return render(request, "orders/invoice.html", context)

def profile(request):
    return render(request, "orders/profile.html")