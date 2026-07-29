# sales/models.py

import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal
from django.db.models import F, Sum


class Customer(models.Model):
    """Customer management"""
    CUSTOMER_TYPES = (
        ('regular', 'Regular'),
        ('wholesale', 'Wholesale'),
        ('vip', 'VIP'),
        ('corporate', 'Corporate'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_code = models.CharField(max_length=50, unique=True, blank=True)

    # Personal Information
    first_name = models.CharField(max_length=100, unique=True)
    last_name = models.CharField(max_length=100)
    tin = models.CharField(max_length=50, unique=True, verbose_name='TIN')
    fin = models.CharField(max_length=50, unique=True, verbose_name='FIN')
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, unique=True)
    phone_number_2 = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    # Address
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)

    # Customer Type
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPES, default='regular')
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    current_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Loyalty Program
    loyalty_points = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Additional
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='customers_created')

    class Meta:
        ordering = ['-total_spent']
        indexes = [
            models.Index(fields=['customer_code']),
            models.Index(fields=['phone_number']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.get_full_name()} ({self.customer_code})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.customer_code:
            year = timezone.now().strftime('%Y')
            last_customer = Customer.objects.filter(
                customer_code__startswith=f'CUST{year}'
            ).order_by('-customer_code').first()

            if last_customer:
                last_number = int(last_customer.customer_code[-6:])
                new_number = last_number + 1
            else:
                new_number = 1

            self.customer_code = f"CUST{year}{new_number:06d}"
        super().save(*args, **kwargs)

    def add_loyalty_points(self, points):
        """Add loyalty points to customer"""
        self.loyalty_points += points
        self.save()

    def redeem_loyalty_points(self, points):
        """Redeem loyalty points"""
        if points <= self.loyalty_points:
            self.loyalty_points -= points
            self.save()
            return True
        return False


class Sale(models.Model):
    """Sale & Proforma transaction"""
    STATUS_CHOICES = (
        ('proforma', 'Proforma Invoice'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('unpaid', 'Unpaid'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_number = models.CharField(max_length=50, unique=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='sales')

    # Store walk-in customer name when no Customer record exists
    customer_name = models.CharField(max_length=200, blank=True, default='', help_text="Walk-in customer name when not linked to a Customer record")

    # Sale Details
    sale_date = models.DateTimeField(default=timezone.now)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Payment
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    change_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')

    # Credit tracking
    credit_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Outstanding credit amount for this sale")
    has_credit = models.BooleanField(default=False)

    # Prescription
    prescription_required = models.BooleanField(default=False)
    prescription_number = models.CharField(max_length=100, blank=True)
    prescription_image = models.ImageField(upload_to='prescriptions/', blank=True, null=True)

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)

    # Tracking
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='sales_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-sale_date']
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['status']),
            models.Index(fields=['sale_date']),
            models.Index(fields=['has_credit']),
        ]

    def __str__(self):
        prefix_str = "Proforma" if self.status == 'proforma' else "Invoice"
        return f"{prefix_str} {self.invoice_number} - TSh {self.total_amount}"

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            year = timezone.now().strftime('%Y')
            month = timezone.now().strftime('%m')
            prefix = "PRF" if self.status == 'proforma' else "INV"

            last_sale = Sale.objects.filter(
                invoice_number__startswith=f'{prefix}{year}{month}'
            ).order_by('-invoice_number').first()

            if last_sale:
                last_number = int(last_sale.invoice_number[-6:])
                new_number = last_number + 1
            else:
                new_number = 1

            self.invoice_number = f"{prefix}{year}{month}{new_number:06d}"

        super().save(*args, **kwargs)

    def get_display_customer_name(self):
        """Return the customer name for display – linked record or walk-in name"""
        if self.customer:
            return self.customer.get_full_name()
        return self.customer_name

    def calculate_totals(self):
        """Calculate sale totals"""
        items = self.items.all()
        self.subtotal = sum(item.subtotal for item in items)

        # Apply discount
        if self.discount_percent > 0:
            discount_percent_decimal = Decimal(str(self.discount_percent))
            self.discount_amount = self.subtotal * (discount_percent_decimal / Decimal('100'))

        # Calculate tax
        taxable_amount = self.subtotal - self.discount_amount
        self.tax_amount = Decimal('0')

        # Total
        self.total_amount = taxable_amount + self.tax_amount

        # Calculate credit
        self.credit_amount = max(Decimal('0'), self.total_amount - self.amount_paid)
        self.has_credit = self.credit_amount > 0

        # Update payment status
        if self.amount_paid >= self.total_amount:
            self.payment_status = 'paid'
            self.change_amount = self.amount_paid - self.total_amount
        elif self.amount_paid > 0:
            self.payment_status = 'partial'
        else:
            self.payment_status = 'unpaid'

        self.save(update_fields=['subtotal', 'discount_amount', 'tax_amount', 'total_amount', 'credit_amount', 'has_credit', 'payment_status', 'change_amount'])

        # Proformas NEVER complete automatically upon payment
        if self.status != 'proforma' and self.payment_status == 'paid' and self.status != 'completed':
            self.complete_sale()

    def complete_sale(self):
        """Complete the sale and update stock"""
        if self.status == 'proforma':
            raise ValueError("Proforma invoices must be converted to sales before completion.")

        if self.status != 'completed':
            # Validate stock availability before completing
            for item in self.items.all():
                if item.product.current_stock < item.quantity:
                    raise ValueError(f"Insufficient stock for {item.product.name}. Available: {item.product.current_stock}")

            self.status = 'completed'
            self.save()

            # Update customer loyalty points (1 point per 1000 TSh)
            if self.customer:
                points_earned = int(self.total_amount / 1000)
                self.customer.add_loyalty_points(points_earned)
                self.customer.total_spent += self.total_amount
                self.customer.save()

            # Deduct stock for each item when stock has not been adjusted yet
            from inventory.models import StockMovement
            if not StockMovement.objects.filter(reference_type='Sale', reference_id=str(self.id)).exists():
                for item in self.items.all():
                    product = item.product
                    previous_qty = product.current_stock          # CAPTURE BEFORE
                    new_qty = previous_qty - item.quantity        # CALCULATE AFTER

                    product.current_stock = F('current_stock') - item.quantity
                    product.save(update_fields=['current_stock'])

                    StockMovement.objects.create(
                        product=product,
                        movement_type='sale',
                        quantity=item.quantity,
                        previous_quantity=previous_qty,            # FIXED
                        new_quantity=new_qty,                      # FIXED
                        unit_price=item.unit_price,
                        total_amount=item.subtotal,
                        reference_type='Sale',
                        reference_id=str(self.id),
                        created_by=self.created_by,
                        notes=f"Sale {self.invoice_number}"
                    )

    def convert_to_sale(self, user=None, payment_amount=Decimal('0'), payment_method='cash'):
        """Converts a Proforma Invoice to an active Sale, deducting stock and creating credit/payment records."""
        from django.db import transaction
        if self.status != 'proforma':
            raise ValueError("Only proforma invoices can be converted to sales.")

        with transaction.atomic():
            # 1. Check Stock for all items
            stock_errors = []
            for item in self.items.all():
                if item.product.current_stock < item.quantity:
                    stock_errors.append(
                        f"{item.product.name}: Available ({item.product.current_stock}), Required ({item.quantity})"
                    )

            if stock_errors:
                raise ValueError(f"Insufficient stock to convert proforma: {', '.join(stock_errors)}")

            # 2. Change status to pending
            self.status = 'pending'
            if user:
                self.created_by = user
            self.save(update_fields=['status', 'created_by'])

            # 3. Handle payment during conversion if provided
            payment_amount = Decimal(str(payment_amount))
            if payment_amount > 0:
                self.add_payment(payment_amount, payment_method)

            # 4. Handle Credit or Completion
            credit_amount = max(Decimal('0'), self.total_amount - self.amount_paid)

            if credit_amount > 0:
                self.has_credit = True
                self.credit_amount = credit_amount
                self.payment_status = 'partial' if self.amount_paid > 0 else 'unpaid'
                self.save(update_fields=['has_credit', 'credit_amount', 'payment_status'])

                CreditRecord.objects.create(
                    sale=self,
                    customer=self.customer,
                    customer_name=self.customer_name or (self.customer.get_full_name() if self.customer else ''),
                    credit_amount=credit_amount,
                    amount_paid=self.amount_paid,
                    remaining_balance=credit_amount,
                    notes=f"Auto-recorded upon Proforma conversion ({self.invoice_number}).",
                    created_by=user or self.created_by,
                )

                if self.customer:
                    self.customer.current_balance += credit_amount
                    self.customer.save()

                # Deduct stock for credit sale
                from inventory.models import StockMovement
                if not StockMovement.objects.filter(reference_type='Sale', reference_id=str(self.id)).exists():
                    for item in self.items.all():
                        product = item.product
                        previous_qty = product.current_stock          # CAPTURE BEFORE
                        new_qty = previous_qty - item.quantity        # CALCULATE AFTER

                        product.current_stock = F('current_stock') - item.quantity
                        product.save(update_fields=['current_stock'])

                        StockMovement.objects.create(
                            product=product,
                            movement_type='sale',
                            quantity=item.quantity,
                            previous_quantity=previous_qty,            # FIXED
                            new_quantity=new_qty,                      # FIXED
                            unit_price=item.unit_price,
                            total_amount=item.subtotal,
                            reference_type='Sale',
                            reference_id=str(self.id),
                            created_by=user or self.created_by,
                            notes=f"Converted Sale {self.invoice_number}"
                        )
            else:
                self.complete_sale()

    def add_payment(self, amount, payment_method, reference=None):
        """Add payment to sale"""
        amount = Decimal(str(amount))

        self.amount_paid += amount
        self.save()

        # Create payment record
        payment_kwargs = {
            'sale': self,
            'amount': amount,
            'payment_method': payment_method,
            'created_by': self.created_by
        }

        if reference:
            payment_kwargs['reference_number'] = reference
        else:
            payment_kwargs['reference_number'] = f"CASH-{timezone.now().strftime('%Y%m%d%H%M%S')}"

        Payment.objects.create(**payment_kwargs)
        self.calculate_totals()

    def update_payment(self, payment_id, new_amount, payment_method=None, reference=None):
        """Update an existing payment"""
        try:
            payment = Payment.objects.get(id=payment_id, sale=self)
            old_amount = payment.amount

            payment.amount = Decimal(str(new_amount))
            if payment_method:
                payment.payment_method = payment_method
            if reference:
                payment.reference_number = reference
            payment.save()

            self.amount_paid = self.amount_paid - old_amount + Decimal(str(new_amount))
            self.save()

            self.calculate_totals()

            credit_record = self.credit_records.filter(status__in=['pending', 'partial']).first()
            if credit_record:
                credit_record.amount_paid = self.amount_paid
                credit_record.save()

            from core.models import ActivityLog
            ActivityLog.objects.create(
                user=self.created_by,
                action='update',
                model_name='Payment',
                object_id=str(payment.id),
                object_repr=f"Updated payment from {old_amount} to {new_amount} for {self.invoice_number}",
                ip_address=None
            )

            return True
        except Payment.DoesNotExist:
            return False

    def add_partial_payment(self, amount, payment_method, reference=None, notes=""):
        """Add a partial payment to an existing sale"""
        amount = Decimal(str(amount))
        self.add_payment(amount, payment_method, reference)

        from core.models import ActivityLog
        ActivityLog.objects.create(
            user=self.created_by,
            action='update',
            model_name='Sale',
            object_id=str(self.id),
            object_repr=f"Partial payment of {amount} added to {self.invoice_number}",
            ip_address=None
        )

        credit_record = self.credit_records.filter(status__in=['pending', 'partial']).first()
        if credit_record:
            credit_record.amount_paid = self.amount_paid
            credit_record.save()

        return True

    def get_remaining_balance(self):
        """Get remaining balance for the sale"""
        return max(Decimal('0'), self.total_amount - self.amount_paid)


class SaleItem(models.Model):
    """Items in sale - No batch reference"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('inventory.Product', on_delete=models.CASCADE, related_name='sale_items')

    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    batch_number = models.CharField(max_length=100, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    pack_size = models.CharField(max_length=100, blank=True, null=True)

    original_price = models.DecimalField(max_digits=12, decimal_places=2, default=0,
                                        help_text="Product's original selling price at time of sale")

    prescription_required = models.BooleanField(default=False)
    prescription_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['sale', 'product']),
        ]

    def __str__(self):
        return f"{self.sale.invoice_number} - {self.product.name}"

    def clean(self):
        """Validate that selling price is not lower than 70% of original"""
        from django.core.exceptions import ValidationError

        unit_price = Decimal(str(self.unit_price))
        original_price = Decimal(str(self.original_price))

        min_allowed = original_price * Decimal('0.70')

        if original_price > 0 and unit_price < min_allowed:
            raise ValidationError(
                f"Selling price (TSh {unit_price}) cannot be lower than "
                f"70% of original price (TSh {min_allowed}). "
                f"Maximum discount allowed is 30%."
            )

    def save(self, *args, **kwargs):
        if self.original_price == 0 and self.product_id:
            self.original_price = self.product.selling_price

        unit_price = Decimal(str(self.unit_price))
        self.unit_price = unit_price

        self.subtotal = self.quantity * unit_price

        if self.discount_percent > 0:
            discount_percent_decimal = Decimal(str(self.discount_percent))
            self.discount_amount = self.subtotal * (discount_percent_decimal / Decimal('100'))

        taxable_amount = self.subtotal - self.discount_amount
        self.tax_amount = taxable_amount * Decimal('0.18')

        super().save(*args, **kwargs)

    @property
    def discount_percent_applied(self):
        """Percentage discount applied to the original price"""
        if self.original_price > 0:
            return round((1 - self.unit_price / self.original_price) * 100, 2)
        return 0


class Payment(models.Model):
    """Payment records"""
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('mobile_money', 'Mobile Money'),
        ('bank_transfer', 'Bank Transfer'),
        ('loyalty_points', 'Loyalty Points'),
        ('credit', 'Credit'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='payments')
    payment_number = models.CharField(max_length=50, unique=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_number} - TSh {self.amount}"

    def save(self, *args, **kwargs):
        if not self.payment_number:
            self.payment_number = f"PAY{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)


class SaleReturn(models.Model):
    """Sales return/refund"""
    RETURN_REASONS = (
        ('damaged', 'Damaged Product'),
        ('wrong_item', 'Wrong Item'),
        ('expired', 'Expired'),
        ('customer_request', 'Customer Request'),
        ('quality_issue', 'Quality Issue'),
        ('other', 'Other'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    return_number = models.CharField(max_length=50, unique=True, blank=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='returns')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)

    return_date = models.DateTimeField(default=timezone.now)
    reason = models.CharField(max_length=20, choices=RETURN_REASONS)
    notes = models.TextField(blank=True)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    status = models.CharField(max_length=20, default='pending')
    refund_processed = models.BooleanField(default=False)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='sale_returns_created')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='sale_returns_approved')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Return {self.return_number} - Invoice {self.sale.invoice_number}"

    def save(self, *args, **kwargs):
        if not self.return_number:
            self.return_number = f"SRET{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)


class SaleReturnItem(models.Model):
    """Items returned"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sale_return = models.ForeignKey(SaleReturn, on_delete=models.CASCADE, related_name='items')
    sale_item = models.ForeignKey(SaleItem, on_delete=models.CASCADE, related_name='return_items')
    product = models.ForeignKey('inventory.Product', on_delete=models.CASCADE)

    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reason = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class CreditRecord(models.Model):
    """Credit records for sales – tracks outstanding amounts owed by customers"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    credit_number = models.CharField(max_length=50, unique=True, blank=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='credit_records')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='credit_records')

    customer_name = models.CharField(max_length=200, blank=True, default='')

    credit_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    remaining_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['due_date']),
            models.Index(fields=['customer']),
        ]

    def __str__(self):
        return f"Credit {self.credit_number} - TSh {self.credit_amount}"

    def save(self, *args, **kwargs):
        if not self.credit_number:
            self.credit_number = f"CRED{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"

        self.remaining_balance = self.credit_amount - self.amount_paid

        if self.remaining_balance <= 0:
            self.status = 'paid'
            self.remaining_balance = Decimal('0')
        elif self.amount_paid > 0:
            self.status = 'partial'
        elif self.due_date and timezone.now().date() > self.due_date:
            self.status = 'overdue'
        else:
            self.status = 'pending'

        super().save(*args, **kwargs)

    def get_customer_display(self):
        """Return customer name for display"""
        if self.customer:
            return self.customer.get_full_name()
        return self.customer_name

    def add_payment(self, amount, payment_method='cash', reference=None):
        """Add a payment toward this credit"""
        if amount <= 0:
            return False
        if amount > self.remaining_balance:
            amount = self.remaining_balance

        self.amount_paid += amount
        self.save()

        Payment.objects.create(
            sale=self.sale,
            amount=amount,
            payment_method=payment_method,
            reference_number=reference,
            notes=f"Credit repayment for {self.credit_number}",
            created_by=self.created_by
        )

        self.sale.amount_paid += amount
        self.sale.calculate_totals()

        if self.customer:
            self.customer.current_balance = max(
                Decimal('0'),
                self.customer.current_balance - amount
            )
            self.customer.save()

        if self.sale.payment_status == 'paid' and self.sale.status != 'completed':
            self.sale.complete_sale()

        return True


class LoyaltyCard(models.Model):
    """Loyalty card management"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    card_number = models.CharField(max_length=50, unique=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='loyalty_card')

    points_balance = models.IntegerField(default=0)
    points_earned = models.IntegerField(default=0)
    points_redeemed = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    issued_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Card {self.card_number} - {self.customer.get_full_name()}"

    def earn_points(self, points):
        """Earn loyalty points"""
        self.points_balance += points
        self.points_earned += points
        self.save()

    def redeem_points(self, points):
        """Redeem loyalty points"""
        if points <= self.points_balance:
            self.points_balance -= points
            self.points_redeemed += points
            self.save()
            return True
        return False


class LoyaltyTransaction(models.Model):
    """Loyalty points transactions"""
    TRANSACTION_TYPES = (
        ('earn', 'Points Earned'),
        ('redeem', 'Points Redeemed'),
        ('expire', 'Points Expired'),
        ('adjust', 'Adjusted'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    loyalty_card = models.ForeignKey(LoyaltyCard, on_delete=models.CASCADE, related_name='transactions')
    sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, null=True, blank=True)

    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    points = models.IntegerField()
    balance_after = models.IntegerField()

    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.loyalty_card.card_number} - {self.transaction_type} - {self.points} points"