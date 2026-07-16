from django.shortcuts import render
from django.db.models import Sum, F, Count
from orders.models import Product, Order


def chat(request):

    response = ""

    if request.method == "POST":

        question = request.POST.get("question").lower()

        if "revenue" in question:

          revenue = (
            Order.objects
            .annotate(total=F("quantity") * F("product__price"))
            .aggregate(total_revenue=Sum("total"))["total_revenue"]
            or 0
          )

          response = f"Total Revenue: ₹{revenue}"

        elif "best" in question:

            product = (
            Order.objects
            .values("product__name")
            .annotate(total_sold=Sum("quantity"))
            .order_by("-total_sold")
            .first()
             )

            if product:
               response = (
               f"Best Selling Product:\n\n"
               f"{product['product__name']}\n"
               f"Total Sold: {product['total_sold']} units"
               )

            else:
                response = "No sales data available."
                
        elif "stock" in question:

            products = Product.objects.filter(quantity__lt=5)

            if products.exists():

                response = "Low Stock Products:\n"

                for product in products:
                    response += f"{product.name} - {product.quantity} units\n"

            else:
                response = "No low stock products."


        elif "total order" in question:

            count = Order.objects.count()

            response = f"Total Orders: {count}"

        elif "status" in question:

            found = False

            for order in Order.objects.all():

                if order.customer_name.lower() in question:

                    response = (
                     f"Customer: {order.customer_name}\n"
                     f"Product: {order.product.name}\n"
                     f"Status: {order.status}"
                     )

                    found = True
                    break

            if not found:
                  response = "Please enter customer name with status."

        elif "history" in question:

          found = False

          response = "Order History:\n\n"

          for order in Order.objects.all():

             if order.customer_name.lower() in question:

                 response += (
                f"Product: {order.product.name}\n"
                f"Quantity: {order.quantity}\n"
                f"Date: {order.order_date}\n"
                f"Status: {order.status}\n\n"
                 )

             found = True


          if not found:
             response = "No order history found."

        elif "order" in question:

            orders = Order.objects.all()

            if orders.exists():

                response = "Recent Orders:\n"

                for order in orders:
                    response += (
                        f"Customer: {order.customer_name},\n"
                        f"Product: {order.product.name},\n"
                        f"Quantity: {order.quantity}\n\n"
                    )

            else:
                response = "No orders found."

        elif "product" in question:

            products = Product.objects.all()

            response = "Available Products:\n"

            for product in products:
                response += f"{product.name} - ₹{product.price}\n"


        else:

          response = (
         "Hello! I am your Order Management Assistant.\n\n"
         "You can ask me:\n"
         "- Product details\n"
         "- Order status\n"
         "- Order history\n"
         "- Total revenue\n"
         "- Low stock products"
         )

    return render(request, "chatbot/chat.html", {
        "response": response
    })