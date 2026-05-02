from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('sepet/', views.cart_detail, name='cart_detail'),
    path('sepet/ekle/<int:product_id>/', views.cart_add, name='cart_add'),
    path('tamamla/', views.checkout, name='checkout'),
    path('gecmis/', views.order_list, name='order_list'), # Yeni
    path('gecmis/<int:order_id>/', views.order_detail, name='order_detail'),
    path('admin/excel-aktar/', views.export_orders_to_excel, name='export_excel'),
    path('sepet/cikar/<int:product_id>/', views.cart_remove, name='cart_remove'),
]
