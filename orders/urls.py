from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('sepet/', views.cart_detail, name='cart_detail'),
    path('sepet/ekle/<int:product_id>/', views.cart_add, name='cart_add'),
    path('tamamla/', views.checkout, name='checkout'), # Yeni eklenen rota
]
