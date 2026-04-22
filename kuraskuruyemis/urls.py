from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings # Yeni
from django.conf.urls.static import static # Yeni

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('urunler/', include('products.urls', namespace='products')),
    path('siparis/', include('orders.urls', namespace='orders')),
]

# Geliştirme ortamında medya dosyalarını sunmak için:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
