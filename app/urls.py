from django.urls import path
from app import views
urlpatterns = [
    path('', views.ProductView.as_view(), name="home"),
    path('product_details/<int:pk>', views.product_details, name="product-details"),
    path('add_to_cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart, name="pluscart"),
    path('minuscart/', views.minus_cart, name="minuscart"),
    path('remove_item/', views.remove_item, name="remove-item"),
    path('buy/', views.buy_now, name='buy-now'),
    path('customer_address/', views.CustomerView.as_view(), name='customer_address'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('changepassword/', views.change_password, name='changepassword'),
    path('ware/', views.ware, name='wares'),
    path('ware/<slug:data>', views.ware, name='ware'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('accounts/login/', views.Userlogin.as_view(), name='login'),
    path('logout/', views.userlogout,name='logout'),
    path('registration/', views.Registration.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('mulytic/', views.mulytic_view, name='mulytic'),
    path('pro_quantity_check', views.pro_quantity_check, name='pro-quantity-check'),
    path('pdf', views.render_pdf_view, name='pdf'),
    # path('pdfcheck', views.convert_to, name='pdfcheck')
]