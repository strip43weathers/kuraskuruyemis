from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
# YENİ: Eklediğimiz sayfaları içe aktarıyoruz
from products.views import public_product_list, about_us, faq, contact

urlpatterns = [
    path('', public_product_list, name='home'),

    path('fabrika-tanitim/', TemplateView.as_view(template_name='pages/fabrika_tanitim.html'), name='fabrika_tanitim'),
    path('hakkimizda/', about_us, name='about'),
    path('blog/', include('blog.urls', namespace='blog')),
    path('sss/', faq, name='faq'),
    path('iletisim/', contact, name='contact'),
    path('bayimiz-ol/', TemplateView.as_view(template_name='pages/bayimiz_ol.html'), name='bayimiz_ol'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('urunler/', include('products.urls', namespace='products')),
    path('siparis/', include('orders.urls', namespace='orders')),
    path('subeler/', include('branches.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
