from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.product_list, name="product_list"),path("products/add/", views.add_product, name="add_product"),path("products/edit/<int:id>/", views.edit_product, name="edit_product"),path("products/delete/<int:id>/", views.delete_product, name="delete_product"),path("login/", views.user_login, name="login"),path("logout/", views.user_logout, name="logout"),path("add-order/", views.add_order, name="add_order"),path("view-orders/", views.view_orders, name="view_orders"),path("delete-order/<int:id>/", views.delete_order, name="delete_order"),path("edit-order/<int:id>/", views.edit_order, name="edit_order"),path("dashboard/", views.dashboard, name="dashboard"),path("view-products/", views.view_products, name="view_products"),path('invoice/<int:id>/', views.invoice, name='invoice'),path('profile/', views.profile, name='profile'),

]