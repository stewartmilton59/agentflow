# sales/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count, F
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db import transaction
from decimal import Decimal
import json
import csv
import logging
from datetime import timedelta

from accounts.decorators import role_required
from .models import (
    Customer, Sale, SaleItem, Payment,
    SaleReturn, SaleReturnItem, LoyaltyCard, LoyaltyTransaction,
    CreditRecord
)
from .forms import (
    CustomerForm, SaleForm, PaymentForm, SaleReturnForm,
    POSCheckoutForm, CreditRecordForm, CreditPaymentForm,
    ConvertProformaForm
)
from .pos.cart import Cart
from inventory.models import Product, StockAlert, Category, StockMovement
from core.models import ActivityLog, Company

# Setup logger
logger = logging.getLogger(__name__)

MIN_PRICE_RATIO = Decimal('0.70')

def get_company():
    from django.core.cache import cache
    company = cache.get('company_data')
    if company is None:
        company = Company.objects.only(
            'id', 'name', 'favicon', 'logo', 'phone', 'email', 'address',
            'location', 'p_o_box', 'tax_id'
        ).first()
        cache.set('company_data', company, 300)
    return company


def get_product_from_payload(product_id):
    if product_id in (None, ''):
        raise ValueError('Invalid product_id: missing value')

    try:
        return Product.objects.get(id=product_id, is_active=True)
    except Product.DoesNotExist as exc:
        raise ValueError(f'Invalid product_id: {product_id}') from exc
    except (TypeError, ValueError) as exc:
        raise ValueError(f'Invalid product_id: {product_id}') from exc

# ==================== POS VIEWS ====================

@login_required
def pos_view(request):
    return redirect('sales:pos_table')

@login_required
def pos_table_view(request):
    cart = Cart(request.user.id)
    products = Product.objects.filter(is_active=True).select_related('category').only(
        'id', 'name', 'selling_price', 'wholesale_price', 'current_stock',
        'prescription_required', 'category', 'image', 'sku', 'reorder_level'
    ).order_by('name')
    customers = Customer.objects.filter(is_active=True).only(
        'id', 'first_name', 'last_name', 'phone_number'
    )

    context = {
        'cart': cart,
        'products': products,
        'customers': customers,
        'min_price_ratio': float(MIN_PRICE_RATIO),
        'saler_name': request.user.get_full_name() or request.user.username,
    }
    return render(request, 'sales/pos_table.html', context)

# ==================== SALE SAVE (REAL SALE - Affects Stock) ====================

@login_required
@require_http_methods(["POST"])
@transaction.atomic
def pos_save_sale(request):
    try:
        data = json.loads(request.body)

        customer_id = data.get('customer_id')
        customer_name = data.get('customer_name', '').strip()
        items = data.get('items', [])
        payment_amount = Decimal(str(data.get('payment_amount', 0)))
        payment_method = data.get('payment_method', 'cash')
        notes = data.get('notes', '')

        if not items:
            return JsonResponse({'success': False, 'error': 'No items in cart.'}, status=400)

        customer = None
        if customer_id:
            try:
                customer = Customer.objects.get(id=customer_id)
            except Customer.DoesNotExist:
                pass

        subtotal = Decimal('0')
        item_objects = []

        for item in items:
            try:
                product = get_product_from_payload(item.get('product_id'))
            except ValueError as exc:
                return JsonResponse({'success': False, 'error': str(exc)}, status=400)

            qty = int(item['quantity'])
            price = Decimal(str(item['unit_price']))

            if product.current_stock < qty:
                return JsonResponse({
                    'success': False,
                    'error': f'Insufficient stock for {product.name}. Available: {product.current_stock}'
                }, status=400)

            subtotal += price * qty
            item_objects.append({
                'product': product,
                'quantity': qty,
                'unit_price': price,
                'original_price': product.selling_price,
                'batch_number': product.batch_number or '',
                'expiry_date': product.expiry_date,
                'pack_size': product.pack_size or '1',
            })

        sale = Sale.objects.create(
            customer=customer,
            customer_name=customer_name if not customer else '',
            subtotal=subtotal,
            total_amount=subtotal,
            discount_percent=0,
            tax_amount=0,
            status='pending',
            notes=notes,
            created_by=request.user,
        )

        for item_data in item_objects:
            SaleItem.objects.create(
                sale=sale,
                product=item_data['product'],
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price'],
                original_price=item_data['original_price'],
                batch_number=item_data['batch_number'],
                expiry_date=item_data['expiry_date'],
                pack_size=item_data['pack_size'],
            )

        sale.calculate_totals()

        if payment_amount > 0:
            sale.add_payment(payment_amount, payment_method)

        if sale.payment_status == 'paid':
            sale.complete_sale()
        else:
            remaining = sale.get_remaining_balance()
            if remaining > 0:
                sale.has_credit = True
                sale.credit_amount = remaining
                sale.payment_status = 'partial' if payment_amount > 0 else 'unpaid'
                sale.save(update_fields=['has_credit', 'credit_amount', 'payment_status'])

                CreditRecord.objects.create(
                    sale=sale,
                    customer=customer,
                    customer_name=customer_name if not customer else '',
                    credit_amount=remaining,
                    amount_paid=payment_amount,
                    remaining_balance=remaining,
                    notes=f'Auto-created from sale {sale.invoice_number}',
                    created_by=request.user,
                )

                if customer:
                    customer.current_balance += remaining
                    customer.save()

            for item_data in item_objects:
                product = item_data['product']
                previous_qty = product.current_stock
                product.current_stock -= item_data['quantity']
                product.save(update_fields=['current_stock'])

                StockMovement.objects.create(
                    product=product,
                    movement_type='sale',
                    quantity=item_data['quantity'],
                    previous_quantity=previous_qty,
                    new_quantity=product.current_stock,
                    unit_price=item_data['unit_price'],
                    total_amount=item_data['unit_price'] * item_data['quantity'],
                    reference_type='Sale',
                    reference_id=str(sale.id),
                    created_by=request.user,
                    notes=f"Sale {sale.invoice_number}"
                )

        return JsonResponse({
            'success': True,
            'message': 'Sale completed successfully!',
            'sale_id': str(sale.pk),
            'invoice_number': sale.invoice_number,
            'is_proforma': False,
            'redirect_url': reverse('sales:sale_receipt', kwargs={'pk': sale.pk})
        })

    except Exception as e:
        logger.exception("Failed to save sale in pos_save_sale")  # Will write full traceback to django_errors.log
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


# ==================== PROFORMA SAVE (NO Stock Impact) ====================

@login_required
@require_http_methods(["POST"])
@transaction.atomic
def pos_save_proforma(request):
    try:
        data = json.loads(request.body)

        customer_id = data.get('customer_id')
        customer_name = data.get('customer_name', '').strip()
        items = data.get('items', [])
        notes = data.get('notes', '')
        valid_days = int(data.get('valid_days', 14))

        if not items:
            return JsonResponse({'success': False, 'error': 'No items in cart.'}, status=400)

        if not customer_id and not customer_name:
            return JsonResponse({
                'success': False,
                'error': 'Proforma Invoice requires a customer name or selected customer.'
            }, status=400)

        customer = None
        if customer_id:
            try:
                customer = Customer.objects.get(id=customer_id)
            except Customer.DoesNotExist:
                pass

        subtotal = Decimal('0')
        item_objects = []

        for item in items:
            try:
                product = get_product_from_payload(item.get('product_id'))
            except ValueError as exc:
                return JsonResponse({'success': False, 'error': str(exc)}, status=400)

            qty = int(item['quantity'])
            price = Decimal(str(item['unit_price']))

            subtotal += price * qty
            item_objects.append({
                'product': product,
                'quantity': qty,
                'unit_price': price,
                'original_price': product.selling_price,
                'batch_number': product.batch_number or '',
                'expiry_date': product.expiry_date,
                'pack_size': product.pack_size or '1',
            })

        sale = Sale.objects.create(
            customer=customer,
            customer_name=customer_name if not customer else '',
            subtotal=subtotal,
            total_amount=subtotal,
            discount_percent=0,
            tax_amount=0,
            status='proforma',
            notes=notes,
            created_by=request.user,
        )

        for item_data in item_objects:
            SaleItem.objects.create(
                sale=sale,
                product=item_data['product'],
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price'],
                original_price=item_data['original_price'],
                batch_number=item_data['batch_number'],
                expiry_date=item_data['expiry_date'],
                pack_size=item_data['pack_size'],
            )

        sale.calculate_totals()

        return JsonResponse({
            'success': True,
            'message': 'Proforma invoice created successfully!',
            'proforma_id': str(sale.pk),
            'invoice_number': sale.invoice_number,
            'is_proforma': True,
            'redirect_url': reverse('sales:proforma_receipt', kwargs={'pk': sale.pk})
        })

    except Exception as e:
        logger.exception("Failed to save proforma in pos_save_proforma")
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

# ==================== PROFORMA VIEWS ====================

@login_required
def proforma_list_view(request):
    proformas = Sale.objects.filter(status='proforma').select_related('customer', 'created_by').order_by('-sale_date')

    search = request.GET.get('search')
    if search:
        proformas = proformas.filter(
            Q(invoice_number__icontains=search) |
            Q(customer__first_name__icontains=search) |
            Q(customer__last_name__icontains=search) |
            Q(customer_name__icontains=search)
        )

    paginator = Paginator(proformas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'proformas': page_obj}
    return render(request, 'sales/proforma_list.html', context)

@login_required
def proforma_receipt_view(request, pk):
    proforma = get_object_or_404(Sale.objects.select_related('customer', 'created_by'), id=pk, status='proforma')
    items = proforma.items.select_related('product').all()
    company = get_company()

    receipt_items = []
    for idx, item in enumerate(items, start=1):
        product = item.product
        batch_val = item.batch_number or (getattr(product, 'batch_number', 'N/A') if product else 'N/A')
        expiry_val = item.expiry_date or (getattr(product, 'expiry_date', None) if product else None)
        exp_str = expiry_val.strftime('%d/%m/%Y') if hasattr(expiry_val, 'strftime') else (str(expiry_val) if expiry_val else 'N/A')
        pack = item.pack_size or (getattr(product, 'pack_size', '1') if product else '1')
        line_total = item.unit_price * item.quantity

        receipt_items.append({
            's_no': idx,
            'name': getattr(product, 'name', 'Unknown Item'),
            'quantity': item.quantity,
            'price': item.unit_price,
            'pack': pack,
            'batch': batch_val,
            'exp': exp_str,
            'total': line_total,
        })

    if proforma.customer:
        customer_obj = proforma.customer
        customer_name = customer_obj.get_full_name()
        customer_phone = getattr(customer_obj, 'phone_number', '')
        customer_tin = getattr(customer_obj, 'tin', 'N/A')
    else:
        customer_name = proforma.customer_name or 'Walk-in Customer'
        customer_phone = ''
        customer_tin = 'N/A'

    pharmacy_info = {
        'name': company.name if company else 'Robby One Pharmacy',
        'p_o_box': getattr(company, 'p_o_box', '') if company else '',
        'address': (f"P.O.BOX {company.p_o_box} {company.location}" if company and company.p_o_box and company.location else
                    getattr(company, 'address', '') if company else ''),
        'phone': getattr(company, 'phone', '') if company else '',
        'email': getattr(company, 'email', '') if company else '',
        'tin': getattr(company, 'tax_id', '') if company else '',
        'location': getattr(company, 'location', '') if company else '',
    }

    bank_accounts = list(
        company.payment_methods.filter(is_active=True).values('bank_name', 'account_name', 'account_number')
        if company else []
    )

    context = {
        'sale': proforma,
        'items': receipt_items,
        'company': company,
        'pharmacy_info': pharmacy_info,
        'saler_name': proforma.created_by.get_full_name() if proforma.created_by else 'N/A',
        'customer_name': customer_name,
        'customer_phone': customer_phone,
        'customer_tin': customer_tin,
        'grand_total': proforma.total_amount,
        'invoice_number': proforma.invoice_number,
        'sale_date': proforma.sale_date.strftime('%d/%m/%Y'),
        'sale_type_status': 'PROFORMA INVOICE',
        'tin_number': pharmacy_info['tin'],
        'bank_accounts': bank_accounts,
        'footer_message': 'This is a quotation invoice, valid for 30 days. Items subject to stock availability upon payment.',
    }
    return render(request, 'sales/proforma_receipt.html', context)

@login_required
def convert_proforma_to_sale_view(request, pk):
    proforma = get_object_or_404(Sale.objects.select_related('customer', 'created_by'), id=pk, status='proforma')
    proforma_items = proforma.items.select_related('product').all()

    if request.method == 'POST':
        form = ConvertProformaForm(request.POST)
        if form.is_valid():
            payment_amount = form.cleaned_data.get('payment_amount') or Decimal('0')
            payment_method = form.cleaned_data.get('payment_method', 'cash')

            try:
                proforma.convert_to_sale(
                    user=request.user,
                    payment_amount=payment_amount,
                    payment_method=payment_method
                )

                ActivityLog.objects.create(
                    user=request.user,
                    action='update',
                    model_name='Sale',
                    object_id=str(proforma.id),
                    object_repr=f"Converted Proforma to Sale {proforma.invoice_number}",
                    ip_address=request.META.get('REMOTE_ADDR')
                )

                messages.success(request, f"Proforma {proforma.invoice_number} successfully converted to Sale!")
                return redirect('sales:sale_receipt', pk=proforma.id)

            except ValueError as ve:
                messages.error(request, str(ve))
                return redirect('sales:convert_proforma', pk=proforma.id)
            except Exception as e:
                messages.error(request, f"Conversion failed: {str(e)}")
                return redirect('sales:convert_proforma', pk=proforma.id)
    else:
        form = ConvertProformaForm()

    stock_status = []
    has_insufficient_stock = False

    for item in proforma.items.select_related('product').all():
        available = item.product.current_stock
        required = item.quantity
        is_enough = available >= required

        if not is_enough:
            has_insufficient_stock = True

        stock_status.append({
            'product_name': item.product.name,
            'required': required,
            'available': available,
            'is_enough': is_enough,
            'required_negative': -required
        })

    context = {
        'proforma': proforma,
        'items': proforma_items,
        'form': form,
        'stock_status': stock_status,
        'has_insufficient_stock': has_insufficient_stock
    }
    return render(request, 'sales/proforma_convert.html', context)

# ==================== CART VIEWS ====================

@login_required
@require_http_methods(["GET"])
def get_cart(request):
    cart = Cart(request.user.id)
    cart_data = []

    for idx, item in enumerate(cart.items):
        cart_data.append({
            'index': idx,
            'product_id': item.product_id,
            'product_name': item.product_name,
            'quantity': item.quantity,
            'unit_price': float(item.unit_price),
            'original_price': float(getattr(item, 'original_price', item.unit_price)),
            'subtotal': float(item.subtotal),
            'category': getattr(item, 'category', ''),
            'stock_available': getattr(item, 'stock_available', 0),
        })

    return JsonResponse({
        'items': cart_data,
        'item_count': cart.item_count,
        'total': float(cart.total)
    })

@login_required
@require_http_methods(["POST"])
def add_to_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        selling_price = data.get('selling_price', None)

        product = get_object_or_404(Product, id=product_id, is_active=True)

        if product.current_stock < quantity:
            return JsonResponse({
                'error': f'Only {product.current_stock} items in stock for {product.name}'
            }, status=400)

        original_price = product.selling_price

        if selling_price is not None:
            selling_price = Decimal(str(selling_price))
        else:
            selling_price = original_price

        min_price = original_price * MIN_PRICE_RATIO

        if selling_price < min_price:
            return JsonResponse({
                'error': f'Selling price cannot be lower than TSh {min_price:.2f} '
                        f'(70% of original price TSh {original_price:.2f})'
            }, status=400)

        cart = Cart(request.user.id)
        cart.add_item(
            product_id=str(product.id),
            product_name=product.name,
            quantity=quantity,
            unit_price=float(selling_price),
            original_price=float(original_price),
            category=product.category.name if product.category else '',
            stock_available=product.current_stock,
        )

        return JsonResponse({
            'success': True,
            'item_count': cart.item_count,
            'total': float(cart.total),
            'selling_price': float(selling_price),
            'original_price': float(original_price),
            'min_price': float(min_price),
            'stock_remaining': product.current_stock - quantity,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@require_http_methods(["POST"])
def update_cart(request):
    try:
        data = json.loads(request.body)
        index = data.get('index')
        quantity = int(data.get('quantity', 0))

        cart = Cart(request.user.id)

        if index < len(cart.items):
            item = cart.items[index]
            product = Product.objects.get(id=item.product_id, is_active=True)
            current_quantity_in_cart = item.quantity

            if quantity > current_quantity_in_cart:
                additional = quantity - current_quantity_in_cart
                if product.current_stock < additional:
                    return JsonResponse({
                        'error': f'Only {product.current_stock} items in stock for {product.name}'
                    }, status=400)

            cart.update_quantity(index, quantity)

            return JsonResponse({
                'success': True,
                'item_count': cart.item_count,
                'total': float(cart.total)
            })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@require_http_methods(["POST"])
def remove_from_cart(request):
    try:
        data = json.loads(request.body)
        index = data.get('index')

        cart = Cart(request.user.id)
        cart.remove_item(index)

        return JsonResponse({
            'success': True,
            'item_count': cart.item_count,
            'total': float(cart.total)
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@require_http_methods(["POST"])
def clear_cart(request):
    cart = Cart(request.user.id)
    cart.clear()

    return JsonResponse({
        'success': True,
        'item_count': 0,
        'total': 0
    })

@login_required
def checkout_view(request):
    cart = Cart(request.user.id)

    if cart.is_empty:
        messages.error(request, 'Cart is empty!')
        return redirect('sales:pos_view')

    stock_errors = []
    for item in cart.items:
        try:
            product = Product.objects.get(id=item.product_id, is_active=True)
            if product.current_stock < item.quantity:
                stock_errors.append(f"{product.name}: Only {product.current_stock} available, but {item.quantity} in cart")
        except Product.DoesNotExist:
            stock_errors.append(f"Product {item.product_name} is no longer available")

    if stock_errors:
        for error in stock_errors:
            messages.error(request, error)
        return redirect('sales:pos_view')

    if request.method == 'POST':
        form = POSCheckoutForm(request.POST)
        if form.is_valid():
            customer_name = form.cleaned_data.get('customer_name', '').strip()
            customer_uuid = form.cleaned_data.get('customer')
            payment_amount = form.cleaned_data.get('payment_amount') or Decimal('0')
            payment_method = form.cleaned_data.get('payment_method', 'cash')
            notes = form.cleaned_data.get('notes', '')

            customer = None
            if customer_uuid:
                try:
                    customer = Customer.objects.get(id=customer_uuid)
                except Customer.DoesNotExist:
                    pass

            sale = Sale.objects.create(
                customer=customer,
                customer_name=customer_name or (customer.get_full_name() if customer else ''),
                discount_percent=0,
                notes=notes,
                created_by=request.user,
            )

            cart_product_ids = [item.product_id for item in cart.items]
            products_map = {}
            for p in Product.objects.filter(id__in=cart_product_ids, is_active=True).only(
                'id', 'name', 'current_stock', 'selling_price', 'batch_number',
                'expiry_date', 'pack_size', 'prescription_required'
            ):
                products_map[str(p.id)] = p

            invalid_items = []
            for item in cart.items:
                product = products_map.get(item.product_id)
                if product is None:
                    invalid_items.append(item.product_name)
                    continue

                if product.current_stock < item.quantity:
                    invalid_items.append(f"{product.name} (insufficient stock)")
                    continue

                sale_item = SaleItem(
                    sale=sale,
                    product=product,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    original_price=getattr(item, 'original_price', product.selling_price),
                    batch_number=product.batch_number or '',
                    expiry_date=product.expiry_date,
                    pack_size=product.pack_size or '1',
                )
                sale_item.save()

                if hasattr(product, 'prescription_required') and product.prescription_required != 'none':
                    sale_item.prescription_required = True
                    sale_item.save(update_fields=['prescription_required'])
                    sale.prescription_required = True
                    sale.save(update_fields=['prescription_required'])

            if invalid_items:
                sale.delete()
                messages.error(
                    request,
                    f'Cannot complete sale: {", ".join(invalid_items)}. '
                    f'Please update your cart and try again.'
                )
                return redirect('sales:pos_view')

            if sale.items.count() == 0:
                sale.delete()
                messages.error(request, 'No valid items in the sale.')
                return redirect('sales:pos_view')

            sale.calculate_totals()

            credit_amount = max(Decimal('0'), sale.total_amount - payment_amount)

            if payment_amount > 0:
                sale.add_payment(payment_amount, payment_method)

            if credit_amount > 0:
                sale.has_credit = True
                sale.credit_amount = credit_amount
                sale.payment_status = 'partial' if payment_amount > 0 else 'unpaid'
                sale.save(update_fields=['has_credit', 'credit_amount', 'payment_status'])

                CreditRecord.objects.create(
                    sale=sale,
                    customer=customer,
                    customer_name=customer_name or (customer.get_full_name() if customer else ''),
                    credit_amount=credit_amount,
                    amount_paid=payment_amount,
                    remaining_balance=credit_amount,
                    notes=f"Auto-recorded from sale {sale.invoice_number}. {notes}",
                    created_by=request.user,
                )

                if customer:
                    customer.current_balance += credit_amount
                    customer.save()

                for item in sale.items.all():
                    product = item.product
                    previous_qty = product.current_stock
                    product.current_stock -= item.quantity
                    product.save(update_fields=['current_stock'])

                    StockMovement.objects.create(
                        product=product,
                        movement_type='sale',
                        quantity=item.quantity,
                        previous_quantity=previous_qty,
                        new_quantity=product.current_stock,
                        unit_price=item.unit_price,
                        total_amount=item.subtotal,
                        reference_type='Sale',
                        reference_id=str(sale.id),
                        created_by=request.user,
                        notes=f"Sale {sale.invoice_number}"
                    )

                ActivityLog.objects.create(
                    user=request.user,
                    action='create',
                    model_name='Sale',
                    object_id=str(sale.id),
                    object_repr=f"{sale.invoice_number} (Credit: TSh {credit_amount})",
                    ip_address=request.META.get('REMOTE_ADDR')
                )

                messages.warning(
                    request,
                    f'Sale completed with credit! Invoice: {sale.invoice_number}. '
                    f'Credit amount: TSh {credit_amount}'
                )
            else:
                sale.complete_sale()

                ActivityLog.objects.create(
                    user=request.user,
                    action='create',
                    model_name='Sale',
                    object_id=str(sale.id),
                    object_repr=sale.invoice_number,
                    ip_address=request.META.get('REMOTE_ADDR')
                )

                messages.success(request, f'Sale completed! Invoice: {sale.invoice_number}')

            cart.clear()
            return redirect('sales:sale_receipt', pk=sale.id)
    else:
        form = POSCheckoutForm()

    has_prescription = False
    for item in cart.items:
        try:
            product = Product.objects.get(id=item.product_id, is_active=True)
            if product.prescription_required != 'none':
                has_prescription = True
        except Product.DoesNotExist:
            pass

    if has_prescription:
        messages.info(request, 'This order contains prescription items. Please upload a valid prescription.')

    context = {
        'cart': cart,
        'form': form,
        'total': cart.total,
    }
    return render(request, 'sales/checkout.html', context)

# ==================== SALE LIST VIEWS ====================

@login_required
def sale_list_view(request):
    sales = Sale.objects.exclude(status='proforma').select_related('customer', 'created_by').all().order_by('-sale_date')

    status = request.GET.get('status')
    if status:
        sales = sales.filter(status=status)

    payment_status = request.GET.get('payment_status')
    if payment_status:
        sales = sales.filter(payment_status=payment_status)

    date_from = request.GET.get('date_from')
    if date_from:
        sales = sales.filter(sale_date__date__gte=date_from)

    date_to = request.GET.get('date_to')
    if date_to:
        sales = sales.filter(sale_date__date__lte=date_to)

    search = request.GET.get('search')
    if search:
        sales = sales.filter(
            Q(invoice_number__icontains=search) |
            Q(customer__first_name__icontains=search) |
            Q(customer__last_name__icontains=search) |
            Q(customer_name__icontains=search)
        )

    paginator = Paginator(sales, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    today_start = timezone.localtime(timezone.now()).replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    today_sales = Sale.objects.filter(
        sale_date__gte=today_start,
        sale_date__lt=today_end,
        status='completed'
    ).aggregate(
        total=Sum('total_amount'),
        count=Count('id')
    )

    credit_payments = Payment.objects.filter(
        created_at__gte=today_start,
        created_at__lt=today_end,
        notes__startswith='Credit repayment'
    ).aggregate(total=Sum('amount'), count=Count('id'))

    today_credit_payments = credit_payments['total'] or Decimal('0')
    today_sales_total = (today_sales['total'] or Decimal('0')) + today_credit_payments
    today_sales_count = (today_sales['count'] or 0) + (credit_payments['count'] or 0)

    context = {
        'sales': page_obj,
        'status_filter': status,
        'payment_status_filter': payment_status,
        'status_choices': [c for c in Sale.STATUS_CHOICES if c[0] != 'proforma'],
        'payment_status_choices': Sale.PAYMENT_STATUS_CHOICES,
        'today_sales_total': today_sales_total,
        'today_sales_count': today_sales_count,
    }
    return render(request, 'sales/sales_list.html', context)

@login_required
def sale_detail_view(request, pk):
    sale = get_object_or_404(Sale.objects.select_related('customer', 'created_by'), id=pk)
    items = sale.items.select_related('product').all()
    payments = sale.payments.all()
    credit_records = sale.credit_records.all()

    context = {
        'sale': sale,
        'items': items,
        'payments': payments,
        'credit_records': credit_records,
        'min_price_ratio': float(MIN_PRICE_RATIO),
    }
    return render(request, 'sales/sale_detail.html', context)

@login_required
def sale_receipt_view(request, pk):
    sale = get_object_or_404(Sale.objects.select_related('customer', 'created_by'), id=pk)
    items = sale.items.select_related('product').all()
    company = get_company()

    receipt_items = []
    for idx, item in enumerate(items, start=1):
        product = item.product
        batch_val = item.batch_number
        if not batch_val and product:
            batch_val = getattr(product, 'batch_number', None)
        batch = str(batch_val).strip() if batch_val and str(batch_val).strip().lower() != 'none' else 'N/A'

        expiry_val = item.expiry_date
        if not expiry_val and product:
            expiry_val = getattr(product, 'expiry_date', None)
        if expiry_val:
            exp_str = expiry_val.strftime('%d/%m/%Y') if hasattr(expiry_val, 'strftime') else str(expiry_val).strip()
        else:
            exp_str = 'N/A'

        pack_val = item.pack_size
        if not pack_val and product:
            pack_val = getattr(product, 'pack_size', None)
        pack = str(pack_val).strip() if pack_val and str(pack_val).strip().lower() != 'none' else '1'

        line_total = item.unit_price * item.quantity

        receipt_items.append({
            's_no': idx,
            'name': getattr(product, 'name', 'Unknown Item'),
            'quantity': item.quantity,
            'price': item.unit_price,
            'pack': pack,
            'batch': batch,
            'exp': exp_str,
            'total': line_total,
        })

    grand_total = sum(i['total'] for i in receipt_items)

    if sale.customer:
        customer_obj = sale.customer
        customer_name = customer_obj.get_full_name() if hasattr(customer_obj, 'get_full_name') and customer_obj.get_full_name() else getattr(customer_obj, 'name', str(customer_obj))
        customer_phone = getattr(customer_obj, 'phone_number', None) or ''
        customer_tin = getattr(customer_obj, 'tin', None) or 'N/A'
    else:
        customer_name = getattr(sale, 'customer_name', None) or 'Walk-in Customer'
        customer_phone = ''
        customer_tin = 'N/A'

    if sale.payment_status == 'paid':
        sale_type_status = 'CASH SALE'
    elif sale.payment_status == 'partial':
        sale_type_status = 'PARTIAL INVOICE'
    else:
        sale_type_status = 'CREDIT INVOICE'

    pharmacy_info = {
        'name': company.name if company else 'Robby One Pharmacy',
        'p_o_box': getattr(company, 'p_o_box', '') if company else '',
        'address': (f"P.O.BOX {company.p_o_box} {company.location}" if company and company.p_o_box and company.location else
                    getattr(company, 'address', '') if company else ''),
        'phone': getattr(company, 'phone', '') if company else '',
        'email': getattr(company, 'email', '') if company else '',
        'tin': getattr(company, 'tax_id', '') if company else '',
        'location': getattr(company, 'location', '') if company else '',
    }

    bank_accounts = list(
        company.payment_methods.filter(is_active=True).values('bank_name', 'account_name', 'account_number')
        if company else []
    )

    context = {
        'sale': sale,
        'items': receipt_items,
        'company': company,
        'pharmacy_info': pharmacy_info,
        'saler_name': sale.created_by.get_full_name() if sale.created_by else 'N/A',
        'customer_name': customer_name,
        'customer_phone': customer_phone,
        'customer_tin': customer_tin,
        'grand_total': grand_total,
        'invoice_number': sale.invoice_number,
        'sale_date': sale.sale_date.strftime('%d/%m/%Y') if sale.sale_date else timezone.now().strftime('%d/%m/%Y'),
        'sale_type_status': sale_type_status,
        'tin_number': pharmacy_info['tin'],
        'bank_accounts': bank_accounts,
        'footer_message': 'Thanks for doing business with us, we are looking forward to working with you.',
    }
    return render(request, 'sales/sale_receipt.html', context)

@login_required
def delivery_note_view(request, pk):
    sale = get_object_or_404(Sale.objects.select_related('customer', 'created_by'), id=pk)
    items = sale.items.select_related('product').all()
    company = get_company()

    delivery_items = []
    for idx, item in enumerate(items, start=1):
        product = item.product
        batch_val = getattr(item, 'batch_number', None) or (getattr(product, 'batch_number', None) if product else None)
        batch = str(batch_val).strip() if batch_val else 'N/A'

        expiry_val = getattr(item, 'expiry_date', None) or (getattr(product, 'expiry_date', None) if product else None)
        exp_str = expiry_val.strftime('%d/%m/%Y') if expiry_val and hasattr(expiry_val, 'strftime') else 'N/A'

        pack = getattr(item, 'pack_size', None) or (getattr(product, 'pack_size', None) if product else None) or '1'

        delivery_items.append({
            's_no': idx,
            'name': getattr(product, 'name', 'Unknown Item'),
            'quantity': item.quantity,
            'pack': pack,
            'batch': batch,
            'exp': exp_str,
            'unit': getattr(product, 'unit', 'Pcs'),
        })

    if sale.customer:
        customer_obj = sale.customer
        customer_name = customer_obj.get_full_name() if hasattr(customer_obj, 'get_full_name') and customer_obj.get_full_name() else str(customer_obj)
        customer_phone = getattr(customer_obj, 'phone_number', '') or ''
        delivery_address = getattr(customer_obj, 'address', '') or 'N/A'
    else:
        customer_name = getattr(sale, 'customer_name', None) or 'Walk-in Customer'
        customer_phone = ''
        delivery_address = 'N/A'

    pharmacy_info = {
        'name': company.name if company else 'Robby One Pharmacy',
        'p_o_box': getattr(company, 'p_o_box', '') if company else '',
        'address': (f"P.O.BOX {company.p_o_box} {company.location}" if company and company.p_o_box and company.location else
                    getattr(company, 'address', '') if company else ''),
        'phone': getattr(company, 'phone', '') if company else '',
        'email': getattr(company, 'email', '') if company else '',
        'tin': getattr(company, 'tax_id', '') if company else '',
        'location': getattr(company, 'location', '') if company else '',
    }

    context = {
        'sale': sale,
        'items': delivery_items,
        'company': company,
        'pharmacy_info': pharmacy_info,
        'delivery_note_number': f"DN-{sale.invoice_number}",
        'dispatched_by': sale.created_by.get_full_name() if sale.created_by else 'N/A',
        'customer_name': customer_name,
        'customer_phone': customer_phone,
        'delivery_address': delivery_address,
        'dispatch_date': timezone.now().strftime('%d/%m/%Y'),
    }
    return render(request, 'sales/delivery_note.html', context)

@login_required
def sale_update_view(request, pk):
    from django.db import transaction

    sale = get_object_or_404(Sale.objects.select_related('customer', 'created_by'), id=pk)

    if not (request.user.is_superuser or sale.status in ['pending', 'proforma']):
        messages.error(request, 'Only superusers or pending/proforma sales can be updated.')
        return redirect('sales:sale_list')

    if request.method == 'POST':
        try:
            with transaction.atomic():
                customer_id = request.POST.get('customer')
                customer_name = request.POST.get('customer_name', '')
                notes = request.POST.get('notes', '')

                if customer_id:
                    sale.customer = Customer.objects.get(id=customer_id)
                    sale.customer_name = ''
                else:
                    sale.customer = None
                    sale.customer_name = customer_name

                sale.notes = notes

                product_ids = request.POST.getlist('product_id[]')
                quantities = request.POST.getlist('quantity[]')
                prices = request.POST.getlist('price[]')

                if not product_ids:
                    messages.error(request, "Order must contain at least one item.")
                    return redirect('sales:sale_update', pk=sale.id)

                if sale.status != 'proforma':
                    for old_item in sale.items.all():
                        prod = old_item.product
                        prod.current_stock += old_item.quantity
                        prod.save(update_fields=['current_stock'])

                sale.items.all().delete()

                for pid, qty_str, price_str in zip(product_ids, quantities, prices):
                    product = Product.objects.get(id=pid)
                    qty = int(qty_str)
                    price = Decimal(price_str)

                    SaleItem.objects.create(
                        sale=sale,
                        product=product,
                        quantity=qty,
                        unit_price=price,
                        original_price=product.selling_price,
                        batch_number=product.batch_number or '',
                        expiry_date=product.expiry_date,
                        pack_size=product.pack_size or '1',
                    )

                    if sale.status != 'proforma':
                        product.current_stock -= qty
                        product.save(update_fields=['current_stock'])

                sale.calculate_totals()

                if sale.status != 'proforma':
                    if sale.amount_paid >= sale.total_amount:
                        sale.payment_status = 'paid'
                    elif sale.amount_paid > 0:
                        sale.payment_status = 'partial'
                    else:
                        sale.payment_status = 'unpaid'
                    sale.save()

                ActivityLog.objects.create(
                    user=request.user,
                    action='update',
                    model_name='Sale',
                    object_id=str(sale.id),
                    object_repr=f"Updated document {sale.invoice_number}",
                    ip_address=request.META.get('REMOTE_ADDR')
                )

                messages.success(request, f'Document {sale.invoice_number} updated successfully!')
                return redirect('sales:proforma_list' if sale.status == 'proforma' else 'sales:sale_list')

        except Exception as e:
            messages.error(request, f"Error updating sale: {str(e)}")
            return redirect('sales:sale_update', pk=sale.id)

    customers = Customer.objects.filter(is_active=True).only(
        'id', 'first_name', 'last_name', 'phone_number'
    )
    all_products = Product.objects.filter(is_active=True).select_related('category').only(
        'id', 'name', 'sku', 'selling_price', 'current_stock', 'category'
    ).order_by('name')

    context = {
        'sale': sale,
        'customers': customers,
        'all_products': all_products,
    }
    return render(request, 'sales/sale_update.html', context)

@login_required
def sale_delete_view(request, pk):
    sale = get_object_or_404(Sale, id=pk)

    if not (request.user.is_superuser or sale.status in ['pending', 'proforma']):
        messages.error(request, 'Only superusers, pending sales, or proformas can be deleted.')
        return redirect('sales:sale_list')

    if request.method == 'POST':
        from django.db import transaction

        with transaction.atomic():
            if sale.status != 'proforma':
                for item in sale.items.all():
                    product = item.product
                    previous_qty = product.current_stock
                    product.current_stock += item.quantity
                    product.save()

                    StockMovement.objects.create(
                        product=product,
                        movement_type='adjustment',
                        quantity=item.quantity,
                        previous_quantity=previous_qty,
                        new_quantity=product.current_stock,
                        notes=f"Restored from deleted sale {sale.invoice_number}",
                        created_by=request.user
                    )

            invoice_number = sale.invoice_number
            is_proforma = sale.status == 'proforma'
            sale.delete()

            ActivityLog.objects.create(
                user=request.user,
                action='delete',
                model_name='Sale',
                object_repr=invoice_number,
                ip_address=request.META.get('REMOTE_ADDR')
            )

            messages.success(request, f'Document {invoice_number} deleted successfully!')
            return redirect('sales:proforma_list' if is_proforma else 'sales:sale_list')

    context = {'sale': sale}
    return render(request, 'sales/sale_confirm_delete.html', context)

@login_required
def sale_payments_view(request, pk):
    sale = get_object_or_404(Sale.objects.select_related('customer', 'created_by'), id=pk)

    if request.user.role == 'cashier' and sale.created_by != request.user:
        messages.error(request, 'You can only manage payments for your own sales.')
        return redirect('sales:sale_list')

    payments = sale.payments.select_related('created_by').all().order_by('-created_at')
    remaining_balance = sale.get_remaining_balance()

    context = {
        'sale': sale,
        'payments': payments,
        'remaining_balance': remaining_balance,
        'payment_methods': Payment.PAYMENT_METHODS,
    }
    return render(request, 'sales/sale_payments.html', context)

@login_required
@require_http_methods(["POST"])
def add_partial_payment(request, pk):
    sale = get_object_or_404(Sale, id=pk)

    if request.user.role == 'cashier' and sale.created_by != request.user:
        messages.error(request, 'You can only add payments to your own sales.')
        return redirect('sales:sale_list')

    try:
        amount = Decimal(request.POST.get('amount', '0'))
        payment_method = request.POST.get('payment_method', 'cash')
        reference = request.POST.get('reference_number', '')
        notes = request.POST.get('notes', '')
        remaining = sale.get_remaining_balance()

        if amount <= 0:
            messages.error(request, 'Payment amount must be greater than zero.')
        elif amount > remaining:
            messages.error(request, f'Payment amount cannot exceed remaining balance of {remaining}.')
        else:
            sale.add_partial_payment(amount, payment_method, reference, notes)
            messages.success(request, f'Partial payment of TSh {amount:,.2f} added successfully!')
            if sale.get_remaining_balance() == 0:
                messages.success(request, 'Sale is now fully paid!')
    except Exception as e:
        messages.error(request, f'Error adding payment: {str(e)}')

    return redirect('sales:sale_payments', pk=pk)

# ==================== CUSTOMER VIEWS ====================

@login_required
def customer_list_view(request):
    customers = Customer.objects.only(
        'id', 'first_name', 'last_name', 'phone_number', 'email',
        'customer_type', 'is_active', 'total_spent', 'credit_limit',
        'current_balance', 'loyalty_points'
    )

    search = request.GET.get('search')
    if search:
        customers = customers.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(phone_number__icontains=search) |
            Q(email__icontains=search)
        )

    customer_type = request.GET.get('type')
    if customer_type:
        customers = customers.filter(customer_type=customer_type)

    paginator = Paginator(customers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'customers': page_obj,
        'customer_types': Customer.CUSTOMER_TYPES,
    }
    return render(request, 'sales/customer_list.html', context)

@login_required
def customer_create_view(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_by = request.user
            customer.save()

            LoyaltyCard.objects.create(
                card_number=f"LOY{str(customer.id)[:8].upper()}",
                customer=customer
            )

            messages.success(request, f'Customer {customer.get_full_name()} created successfully!')
            return redirect('sales:customer_detail', pk=customer.id)
    else:
        form = CustomerForm()

    return render(request, 'sales/customer_form.html', {'form': form, 'title': 'Add New Customer'})

@login_required
def customer_detail_view(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    sales = customer.sales.exclude(status='proforma')[:10]
    loyalty_card = getattr(customer, 'loyalty_card', None)
    credit_records = customer.credit_records.select_related('sale').filter(status__in=['pending', 'partial'])

    context = {
        'customer': customer,
        'sales': sales,
        'loyalty_card': loyalty_card,
        'credit_records': credit_records,
    }
    return render(request, 'sales/customer_detail.html', context)

# ==================== CREDIT VIEWS ====================

@login_required
def credit_list_view(request):
    credits = CreditRecord.objects.select_related('sale', 'customer', 'created_by').all()

    status = request.GET.get('status')
    if status:
        credits = credits.filter(status=status)

    customer_search = request.GET.get('search')
    if customer_search:
        credits = credits.filter(
            Q(customer__first_name__icontains=customer_search) |
            Q(customer__last_name__icontains=customer_search) |
            Q(customer_name__icontains=customer_search) |
            Q(sale__invoice_number__icontains=customer_search)
        )

    paginator = Paginator(credits, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    credit_aggs = CreditRecord.objects.filter(
        status__in=['pending', 'partial', 'overdue']
    ).aggregate(
        total_outstanding=Sum('remaining_balance'),
        pending_count=Count('id', filter=Q(status='pending')),
        overdue_count=Count('id', filter=Q(status='overdue')),
    )

    context = {
        'credits': page_obj,
        'total_outstanding': credit_aggs['total_outstanding'] or 0,
        'pending_count': credit_aggs['pending_count'] or 0,
        'overdue_count': credit_aggs['overdue_count'] or 0,
        'status_filter': status,
    }
    return render(request, 'sales/credit_list.html', context)

@login_required
def credit_detail_view(request, pk):
    credit = get_object_or_404(CreditRecord.objects.select_related('sale', 'customer', 'created_by'), id=pk)
    related_payments = credit.sale.payments.select_related('created_by').all().order_by('created_at')

    context = {
        'credit': credit,
        'related_payments': related_payments,
    }
    return render(request, 'sales/credit_detail.html', context)

@login_required
def credit_payment_view(request, pk):
    credit = get_object_or_404(CreditRecord.objects.select_related('sale', 'customer', 'created_by'), id=pk)

    if credit.status == 'paid':
        messages.warning(request, 'This credit has already been fully paid.')
        return redirect('sales:credit_detail', pk=pk)

    if request.method == 'POST':
        form = CreditPaymentForm(request.POST, remaining_balance=credit.remaining_balance)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            payment_method = form.cleaned_data['payment_method']
            reference = form.cleaned_data.get('reference_number', '')

            success = credit.add_payment(amount, payment_method, reference)

            if success:
                ActivityLog.objects.create(
                    user=request.user,
                    action='create',
                    model_name='CreditPayment',
                    object_id=str(credit.id),
                    object_repr=f"TSh {amount} paid toward {credit.credit_number}",
                    ip_address=request.META.get('REMOTE_ADDR')
                )

                if credit.status == 'paid':
                    messages.success(request, f'Credit {credit.credit_number} fully paid off!')
                else:
                    messages.success(
                        request,
                        f'TSh {amount} recorded. Remaining balance: TSh {credit.remaining_balance}'
                    )
                return redirect('sales:credit_detail', pk=pk)
            else:
                messages.error(request, 'Failed to process payment.')
    else:
        form = CreditPaymentForm(remaining_balance=credit.remaining_balance)

    context = {
        'credit': credit,
        'form': form,
    }
    return render(request, 'sales/credit_payment.html', context)

# ==================== API ENDPOINTS ====================

@login_required
@require_http_methods(["GET"])
def api_products(request):
    category = request.GET.get('category')
    search = request.GET.get('search')

    products = Product.objects.filter(is_active=True, current_stock__gt=0).select_related('category').only(
        'id', 'name', 'sku', 'selling_price', 'current_stock', 'reorder_level', 'category', 'image'
    )

    if category:
        products = products.filter(category_id=category)

    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(sku__icontains=search) |
            Q(barcode__icontains=search)
        )

    products = products[:50]

    data = []
    for product in products:
        min_price = float(product.selling_price * MIN_PRICE_RATIO)
        data.append({
            'id': str(product.id),
            'name': product.name,
            'sku': product.sku,
            'category': product.category.name if product.category else '',
            'price': float(product.selling_price),
            'min_price': min_price,
            'stock': product.current_stock,
            'reorder_level': product.reorder_level,
            'image': product.image.url if product.image else None,
        })

    return JsonResponse(data, safe=False)

@login_required
@require_http_methods(["GET"])
def api_product_stock(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        return JsonResponse({
            'id': str(product.id),
            'name': product.name,
            'current_stock': product.current_stock,
            'selling_price': float(product.selling_price),
            'purchase_price': float(product.purchase_price),
            'is_out_of_stock': product.current_stock <= 0,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# ==================== PAYMENT MANAGEMENT VIEWS ====================

@login_required
def edit_payment_view(request, pk):
    payment = get_object_or_404(Payment.objects.select_related('sale', 'sale__customer', 'created_by'), id=pk)
    sale = payment.sale

    if request.user.role == 'cashier' and sale.created_by != request.user:
        messages.error(request, 'You can only edit payments for your own sales.')
        return redirect('sales:sale_payments', pk=sale.id)

    if request.method == 'POST':
        try:
            old_amount = payment.amount
            new_amount = Decimal(request.POST.get('amount', '0'))
            payment_method = request.POST.get('payment_method')
            reference = request.POST.get('reference_number', '')
            notes = request.POST.get('notes', '')

            if new_amount <= 0:
                messages.error(request, 'Amount must be greater than zero.')
                return redirect('sales:sale_payments', pk=sale.id)

            payment.amount = new_amount
            payment.payment_method = payment_method
            payment.reference_number = reference
            payment.notes = notes
            payment.save()

            sale.amount_paid = sale.amount_paid - old_amount + new_amount
            sale.save()
            sale.calculate_totals()

            credit_record = sale.credit_records.filter(status__in=['pending', 'partial']).first()
            if credit_record:
                credit_record.amount_paid = sale.amount_paid
                credit_record.remaining_balance = credit_record.credit_amount - credit_record.amount_paid
                if credit_record.remaining_balance <= 0:
                    credit_record.status = 'paid'
                elif credit_record.amount_paid > 0:
                    credit_record.status = 'partial'
                credit_record.save()

            messages.success(request, f'Payment updated from TSh {old_amount:,.2f} to TSh {new_amount:,.2f}')
        except Exception as e:
            messages.error(request, f'Error updating payment: {str(e)}')

        return redirect('sales:sale_payments', pk=sale.id)

    context = {
        'payment': payment,
        'sale': sale,
    }
    return render(request, 'sales/edit_payment.html', context)

@login_required
def delete_payment_view(request, pk):
    payment = get_object_or_404(Payment.objects.select_related('sale', 'sale__customer', 'created_by'), id=pk)
    sale = payment.sale

    if request.user.role == 'cashier' and sale.created_by != request.user:
        messages.error(request, 'You can only delete payments for your own sales.')
        return redirect('sales:sale_payments', pk=sale.id)

    if request.method == 'POST':
        payment_amount = payment.amount
        payment_number = payment.payment_number
        payment.delete()

        sale.amount_paid -= payment_amount
        if sale.amount_paid < 0:
            sale.amount_paid = 0
        sale.calculate_totals()
        sale.save()

        credit_record = sale.credit_records.filter(status__in=['pending', 'partial']).first()
        if credit_record:
            credit_record.amount_paid = sale.amount_paid
            credit_record.remaining_balance = credit_record.credit_amount - credit_record.amount_paid
            if credit_record.remaining_balance <= 0:
                credit_record.status = 'paid'
            elif credit_record.amount_paid > 0:
                credit_record.status = 'partial'
            credit_record.save()

        ActivityLog.objects.create(
            user=request.user,
            action='delete',
            model_name='Payment',
            object_id=str(pk),
            object_repr=f"Payment {payment_number} of TSh {payment_amount}",
            ip_address=request.META.get('REMOTE_ADDR')
        )

        messages.success(request, f'Payment of TSh {payment_amount:,.2f} deleted successfully!')
        return redirect('sales:sale_payments', pk=sale.id)

    context = {
        'payment': payment,
        'sale': sale,
    }
    return render(request, 'sales/delete_payment_confirm.html', context)