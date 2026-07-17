from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home(request):
    return redirect('dashboard')
    
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('orders.urls')),
    path('chatbot/', include('chatbot.urls')),
]