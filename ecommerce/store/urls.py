from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from store.views import *

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('',store, name='store'),
    path('cart/',cart, name='cart'),
    path('register/',registration_form, name='register'),
    path('login/',login_view,name="login"),
    path('logout/',logout_view,name="logout"),
    path('delete/<int:id>/',delete, name='delete'),
    path('checkout/<int:order_id>/<int:customer_id>/', checkout, name='checkout'),
    #path('checkout/',check,name="check"),
    path('addTocart/<int:id>/', addTocart, name='addTocart'),
    path('addTocart_increase/<int:order_id>/<int:product_id>/', increase_count, name='increase'),
    path('addTocart_decrease/<int:order_id>/<int:product_id>/', decrease_count, name='decrease'),
    path('checkout/<int:cus_id>/<int:ord_id>', checkoutform, name='checkoutform'),
    

]

