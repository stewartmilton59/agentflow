from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from django.core.paginator import Paginator
from django.core.files.storage import default_storage
from django.template.loader import get_template
from django.forms import inlineformset_factory
from django.utils import timezone
from decimal import Decimal
from xhtml2pdf import pisa
from .models import PurchaseOrder, PurchaseOrderItem
from .forms import PurchaseOrderForm, PurchaseOrderItemForm
from inventory.models import Product, StockMovement, StockAlert
from core.models import ActivityLog, Company

# Formset for purchase order items
PurchaseOrderItemFormSet = inlineformset_factory(
    PurchaseOrder,
    PurchaseOrderItem,
    form=PurchaseOrderItemForm,
    fields=['product', 'quantity', 'unit_price', 'markup_percent', 'selling_price', 'batch_number', 'expiry_date'],
    extra=1,
    can_delete=True
)


@login_required
def purchase_order_list_view(request):
    """List all purchase orders"""
    orders = PurchaseOrder.objects.all().order_by('-created_at')

    draft_count = PurchaseOrder.objects.filter(status='draft').count()
    completed_count = PurchaseOrder.objects.filter(status='completed').count()
    total_spent = PurchaseOrder.objects.filter(status='completed').aggregate(total=Sum('total_amount'))['total'] or Decimal('0')

    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)

    search = request.GET.get('search')
    if search:
        orders = orders.filter(
            Q(po_number__icontains=search) |
            Q(items__product__name__icontains=search)
        ).distinct()

    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'purchases/purchase_order_list.html', {
        'orders': page_obj,
        'status_choices': PurchaseOrder.STATUS_CHOICES,
        'draft_count': draft_count,
        'completed_count': completed_count,
        'total_spent': total_spent,
    })


@login_required
def purchase_order_create_view(request):
    """Create a purchase order and add stock to inventory"""
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        formset = PurchaseOrderItemFormSet(request.POST, prefix='items')

        if form.is_valid() and formset.is_valid():
            purchase_order = form.save(commit=False)
            purchase_order.created_by = request.user
            purchase_order.status = 'completed'
            purchase_order.save()

            # Save items
            items_saved = False
            for item_form in formset:
                if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE', False):
                    item = item_form.save(commit=False)
                    item.purchase_order = purchase_order

                    if not item.unit_price:
                        item.unit_price = item.product.purchase_price

                    item.save()
                    items_saved = True

            if not items_saved:
                purchase_order.delete()
                messages.error(request, 'Please add at least one product to the purchase order.')
                return redirect('purchases:purchase_order_create')

            purchase_order.calculate_totals()

            # Update inventory stock
            for item in purchase_order.items.select_related('product').all():
                product = item.product
                previous_stock = product.current_stock

                product.purchase_price = item.unit_price
                product.selling_price = item.selling_price or product.selling_price
                product.batch_number = item.batch_number or product.batch_number
                product.expiry_date = item.expiry_date or product.expiry_date
                product.current_stock += item.quantity
                product.save(update_fields=['purchase_price', 'selling_price', 'batch_number', 'expiry_date', 'current_stock'])

                StockMovement.objects.create(
                    product=product,
                    movement_type='purchase',
                    quantity=item.quantity,
                    previous_quantity=previous_stock,
                    new_quantity=product.current_stock,
                    unit_price=item.unit_price,
                    total_amount=item.quantity * item.unit_price,
                    reference_type='PurchaseOrder',
                    reference_id=str(purchase_order.id),
                    created_by=request.user,
                    notes=f'PO {purchase_order.po_number} | Invoice {purchase_order.invoice_number or "N/A"} | Batch {item.batch_number or "N/A"} | Expiry {item.expiry_date or "N/A"}'
                )

                if product.current_stock > product.reorder_level:
                    StockAlert.objects.filter(
                        product=product,
                        alert_type='low_stock',
                        status='active'
                    ).update(status='resolved', resolved_at=timezone.now(), resolved_by=request.user)

            ActivityLog.objects.create(
                user=request.user,
                action='create',
                model_name='PurchaseOrder',
                object_id=str(purchase_order.id),
                object_repr=purchase_order.po_number,
                ip_address=request.META.get('REMOTE_ADDR')
            )

            messages.success(request, f'Purchase order {purchase_order.po_number} completed! Stock has been updated.')
            return redirect('purchases:purchase_order_detail', pk=purchase_order.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PurchaseOrderForm()
        formset = PurchaseOrderItemFormSet(prefix='items')

    return render(request, 'purchases/purchase_order_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Create Purchase Order',
    })


@login_required
def purchase_order_detail_view(request, pk):
    """View purchase order details"""
    purchase_order = get_object_or_404(PurchaseOrder, id=pk)
    items = purchase_order.items.select_related('product').all()

    return render(request, 'purchases/purchase_order_detail.html', {
        'order': purchase_order,
        'items': items,
    })


@login_required
def purchase_order_cancel_view(request, pk):
    """Cancel a purchase order"""
    purchase_order = get_object_or_404(PurchaseOrder, id=pk)

    if purchase_order.status == 'completed':
        messages.error(request, 'Cannot cancel a completed purchase order.')
        return redirect('purchases:purchase_order_detail', pk=purchase_order.id)

    if request.method == 'POST':
        purchase_order.status = 'cancelled'
        purchase_order.save()

        messages.success(request, f'Purchase order {purchase_order.po_number} cancelled.')
        return redirect('purchases:purchase_order_list')

    return render(request, 'purchases/purchase_order_confirm_cancel.html', {'order': purchase_order})


@login_required
def purchase_order_pdf_view(request, pk):
    """Export purchase order as PDF"""
    purchase_order = get_object_or_404(PurchaseOrder, id=pk)
    items = purchase_order.items.select_related('product').all()
    company = Company.objects.first()

    context = {
        'order': purchase_order,
        'items': items,
        'company': company,
    }

    template = get_template('purchases/purchase_order_pdf.html')
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    filename = f"{purchase_order.po_number}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)

    return response