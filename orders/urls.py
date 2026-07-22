from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("products/", views.product_list, name="product_list"),
    path("products/add/", views.add_product, name="add_product"),
    path("products/edit/<int:id>/", views.edit_product, name="edit_product"),
    path("products/delete/<int:id>/", views.delete_product, name="delete_product"),

    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    path("add-order/", views.add_order, name="add_order"),
    path("view-orders/", views.view_orders, name="view_orders"),
    path("delete-order/<int:id>/", views.delete_order, name="delete_order"),
    path("edit-order/<int:id>/", views.edit_order, name="edit_order"),

    path("dashboard/", views.dashboard, name="dashboard"),
    path("view-products/", views.view_products, name="view_products"),

    path("invoice/<int:id>/", views.invoice, name="invoice"),
    path("profile/", views.profile, name="profile"),

    path("welcome/", views.welcome, name="welcome"),
    path("admin-login/", views.admin_login, name="admin_login"),

    path("create-account/", views.create_account, name="create_account"),
    path("user-dashboard/", views.user_dashboard, name="user_dashboard"),

    path("cart/", views.cart, name="cart"),
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove-from-cart/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("increase-cart/<int:product_id>/", views.increase_cart_quantity, name="increase_cart_quantity"),
    path("decrease-cart/<int:product_id>/", views.decrease_cart_quantity, name="decrease_cart_quantity"),
    path("place-order/", views.place_order, name="place_order"),
    path("my-orders/", views.my_orders, name="my_orders"),
    path("track-order/<int:id>/",views.track_order,name="track_order"),
    path("users/",views.user_list,name="user_list"),
    path("users/toggle/<int:id>/",views.toggle_user_status,name="toggle_user_status"),
]