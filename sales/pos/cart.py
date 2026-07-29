import json
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder
from django.core.cache import cache
from inventory.models import Product


class Cart:
    """Shopping cart stored in cache"""

    def __init__(self, user_id):
        self.user_id = user_id
        self.cache_key = f'cart_{user_id}'
        self._load()

    def _load(self):
        """Load cart from cache"""
        self.items = cache.get(self.cache_key, [])

    def _save(self):
        """Save cart to cache"""
        cache.set(self.cache_key, self.items, timeout=86400)  # 24 hours

    def add_item(self, product_id, product_name, quantity, unit_price,
                 original_price=None, batch_id=None, batch_number=None,
                 expiry_date=None, category='', stock_available=None, **kwargs):
        """Add item to cart or update quantity if exists"""

        # Check if product already in cart
        for i, item in enumerate(self.items):
            if item['product_id'] == product_id:
                # Update quantity
                self.items[i]['quantity'] += quantity
                self.items[i]['subtotal'] = self.items[i]['quantity'] * self.items[i]['unit_price']
                self._save()
                return

        # Add new item
        new_item = {
            'product_id': product_id,
            'product_name': product_name,
            'quantity': quantity,
            'unit_price': float(unit_price),
            'original_price': float(original_price) if original_price else float(unit_price),
            'batch_id': batch_id,
            'batch_number': batch_number,
            'expiry_date': expiry_date,
            'category': category,
            'subtotal': quantity * float(unit_price),
        }
        # Optionally store stock_available if needed (but not required)
        if stock_available is not None:
            new_item['stock_available'] = stock_available

        self.items.append(new_item)
        self._save()

    def update_quantity(self, index, quantity):
        """Update item quantity"""
        if 0 <= index < len(self.items):
            if quantity <= 0:
                self.remove_item(index)
            else:
                self.items[index]['quantity'] = quantity
                self.items[index]['subtotal'] = quantity * self.items[index]['unit_price']
                self._save()

    def remove_item(self, index):
        """Remove item from cart"""
        if 0 <= index < len(self.items):
            self.items.pop(index)
            self._save()

    def clear(self):
        """Clear all items from cart"""
        self.items = []
        self._save()

    @property
    def total(self):
        """Calculate cart total"""
        return sum(item['subtotal'] for item in self.items)

    @property
    def item_count(self):
        """Total number of items in cart"""
        return sum(item['quantity'] for item in self.items)

    @property
    def is_empty(self):
        """Check if cart is empty"""
        return len(self.items) == 0

    def get_items(self):
        """Return items as objects with attribute access"""
        # For compatibility with existing code that expects dot notation
        class Item:
            pass

        items = []
        for item in self.items:
            obj = Item()
            for key, value in item.items():
                setattr(obj, key, value)
            items.append(obj)
        return items