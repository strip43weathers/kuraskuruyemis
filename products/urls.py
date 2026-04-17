from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('b2b-portal/', views.b2b_product_list, name='b2b_list'),
]
