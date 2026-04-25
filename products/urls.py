from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('katalog/', views.public_product_list, name='public_list'), # Yeni vitrin rotası
    path('katalog/urun/<int:pk>/', views.public_product_detail, name='public_detail'),
    path('b2b-portal/', views.b2b_product_list, name='b2b_list'),
]
