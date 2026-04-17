# cart.py
from decimal import Decimal
from django.conf import settings
from products.models import Product


class Cart:
    def __init__(self, request):
        """Sepeti session'dan yükle veya yeni sepet oluştur."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        """Sepete ürün ekle veya miktarını güncelle."""
        product_id = str(product.id)
        # Decimal'i JSON'da saklayabilmek için string'e çeviriyoruz
        quantity_str = str(quantity)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': quantity_str,
                'price': str(product.wholesale_price)
            }
        else:
            # Var olan miktarın üzerine ekle
            current_qty = Decimal(self.cart[product_id]['quantity'])
            new_qty = current_qty + Decimal(quantity_str)
            self.cart[product_id]['quantity'] = str(new_qty)

        self.save()

    def save(self):
        """Session'ı güncellendi olarak işaretle."""
        self.session.modified = True

    def clear(self):
        """Sipariş tamamlanınca sepeti boşalt."""
        del self.session[settings.CART_SESSION_ID]
        self.save()
