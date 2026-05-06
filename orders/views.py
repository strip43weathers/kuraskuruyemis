import openpyxl
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db import transaction
from decimal import Decimal
from products.models import Product
from .models import Order, OrderItem
from .cart import Cart
from .forms import OrderExportForm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse


@require_POST
@login_required(login_url='/login/')
def cart_add(request, product_id):
    """Form üzerinden gelen miktar (KG) ile sepete ürün ekler."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    # HTML formundan gelecek 'quantity' değerini alıyoruz
    quantity = request.POST.get('quantity')

    if quantity:
        try:
            qty = int(float(quantity))

            # KONTROL 1: Minimum sipariş miktarının altında mı?
            if qty < product.minimum_order_quantity:
                messages.error(request,
                               f"{product.name} için minimum sipariş miktarı {product.minimum_order_quantity | floatformat:'0'} kg'dır.")
                return redirect(request.META.get('HTTP_REFERER', 'orders:cart_detail'))

            # KONTROL 2: Girilen miktar, ürünün satış katına tam bölünmüyorsa hata ver
            if qty % product.unit_step != 0:
                messages.error(request,
                               f"{product.name} ürünü sadece {product.unit_step} kg ve katları şeklinde sipariş edilebilir.")
                return redirect(request.META.get('HTTP_REFERER', 'orders:cart_detail'))

            # Sorun yoksa sepete ekle
            cart.add(product=product, quantity=qty)
            messages.success(request, f"{product.name} ({qty} kg) sepete eklendi.")

        except ValueError:
            messages.error(request, "Geçersiz bir miktar girdiniz.")
            return redirect(request.META.get('HTTP_REFERER', 'orders:cart_detail'))

    return redirect('orders:cart_detail')


@login_required(login_url='/login/')
def cart_detail(request):
    """Sepet içeriğini görüntüler."""
    cart = Cart(request)
    # Şablonu bir sonraki adımda oluşturacağız
    return render(request, 'orders/cart_detail.html', {'cart': cart})


@login_required(login_url='/login/')
def checkout(request):
    """Siparişi tamamlar ve stoktan güvenli bir şekilde düşer."""
    cart = Cart(request)

    if not cart.cart:
        messages.warning(request, "Sepetiniz boş. Lütfen ürün ekleyin.")
        return redirect('products:b2b_list')

    if request.method == 'POST':
        # Müşteri siparişi onayladı. transaction.atomic ile bu bloktaki işlemlerden
        # biri bile hata verirse (örneğin stok yetmezse) hiçbir şey veritabanına yazılmaz (rollback).
        try:
            with transaction.atomic():
                # 1. Sipariş kaydını oluştur
                order = Order.objects.create(
                    user=request.user,
                    status='RECEIVED',
                    order_note=request.POST.get('order_note', '')
                )

                total_amount = Decimal('0.00')

                # 2. Sepetteki ürünleri dön ve stok kontrolü yap
                for item_id, item_data in cart.cart.items():
                    # select_for_update(): Bu satırı okurken kilitler, başka bir işlem buraya müdahale edemez.
                    product = Product.objects.select_for_update().get(id=item_id)
                    quantity = Decimal(item_data['quantity'])
                    price = Decimal(item_data['price'])

                    # Stok kontrolü
                    if product.stock_quantity < quantity:
                        # Eğer stok yetersizse hata fırlat, transaction.atomic tüm süreci iptal etsin
                        raise ValueError(
                            f"{product.name} için yeterli stok yok! Kalan stok: {product.stock_quantity} kg")

                    # 3. Stoktan miktarı düş ve kaydet
                    product.stock_quantity -= quantity
                    product.save()

                    # 4. Sipariş kalemini oluştur
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        unit_price=price,
                        total_price=quantity * price
                    )

                    total_amount += (quantity * price)

                # 5. Toplam tutarı siparişe yaz
                order.total_amount = total_amount
                order.save()

                # 6. İşlem bitti, sepeti boşalt
                cart.clear()
                messages.success(request, f"Siparişiniz başarıyla alındı! Sipariş No: #{order.id}")

                # Başarılı olunca ürünler sayfasına geri dön
                return redirect('products:b2b_list')

        except ValueError as e:
            # Stok hatası mesajını müşteriye göster ve sepetine geri yolla
            messages.error(request, str(e))
            return redirect('orders:cart_detail')

        except Exception as e:
            # Beklenmeyen bir hata (veritabanı bağlantısı kopması vb.)
            messages.error(request, "Sipariş işlenirken bir hata oluştu. Lütfen tekrar deneyin.")
            return redirect('orders:cart_detail')

    # Eğer GET isteği ise, müşteriye sipariş öncesi "Onay" sayfasını göster
    return render(request, 'orders/checkout.html', {'cart': cart})


@login_required(login_url='/login/')
def order_list(request):
    """Müşterinin geçmiş tüm siparişlerini listeler."""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required(login_url='/login/')
def order_detail(request, order_id):
    """Belirli bir siparişin içeriğini gösterir."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@require_POST
@login_required(login_url='/login/')
def cart_remove(request, product_id):
    """Müşterinin seçtiği ürünü sepetten siler."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    # Yeni eklediğimiz remove metodunu çağırıyoruz
    cart.remove(product)

    messages.success(request, f"{product.name} sepetinizden çıkarıldı.")
    return redirect('orders:cart_detail')


@staff_member_required
def export_orders_to_excel(request):
    if request.method == 'POST':
        form = OrderExportForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']

            # Belirlenen aralıktaki siparişleri çek (İçindeki kalemlerle birlikte)
            orders = Order.objects.filter(created_at__range=(start, end)).prefetch_related('items__product', 'user')

            # Excel Çalışma Kitabı Oluştur
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Sipariş Raporu"

            # Başlık Satırı
            headers = ['Sipariş No', 'Tarih', 'Müşteri', 'Ürün', 'Miktar (KG)', 'Birim Fiyat', 'Toplam Tutar', 'Durum']
            ws.append(headers)

            # Verileri Doldur
            for order in orders:
                for item in order.items.all():
                    ws.append([
                        order.id,
                        order.created_at.replace(tzinfo=None),  # Excel için timezone temizliği
                        order.user.username,
                        item.product.name,
                        item.quantity,
                        item.unit_price,
                        item.total_price,
                        order.get_status_display()
                    ])

            # HTTP Yanıtı Hazırla
            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
            response['Content-Disposition'] = f'attachment; filename=Siparis_Raporu_{start.date()}_{end.date()}.xlsx'

            wb.save(response)
            return response
    else:
        form = OrderExportForm()

    return render(request, 'orders/admin/export_form.html', {'form': form})