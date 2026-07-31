from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib import messages
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from django.utils.timezone import now, timedelta
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from decimal import Decimal
import csv
import json
import os

from .models import Company, PaymentMethod, ActivityLog, Notification, Backup, SystemSetting
from .backup_utils import create_database_backup, create_media_backup, create_full_backup, restore_database_backup
from .forms import CompanyForm, SystemSettingForm, BackupForm
from accounts.models import UserActivityLog
from sales.models import Sale, Payment, SaleItem, Customer, CreditRecord
from inventory.models import Product, StockMovement
from core.decorators import administrator_required


@login_required
@administrator_required
def dashboard_view(request):
    """Main dashboard with comprehensive statistics"""
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    year_ago = today - timedelta(days=365)
    yesterday = today - timedelta(days=1)

    current_time = timezone.now()
    today_start = timezone.localtime(current_time).replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    yesterday_start = today_start - timedelta(days=1)
    yesterday_end = today_start

    # ========== SALES STATISTICS ==========

    # Today's sales should include completed sales created today and any credit repayments settled today.
    today_sales = Sale.objects.filter(
        sale_date__gte=today_start,
        sale_date__lt=today_end,
        status='completed'
    ).aggregate(
        total=Sum('total_amount'),
        count=Count('id')
    )
    today_sales['total'] = today_sales['total'] or Decimal('0')
    today_sales['count'] = today_sales['count'] or 0

    today_credit_payments = Payment.objects.filter(
        created_at__gte=today_start,
        created_at__lt=today_end,
        notes__startswith='Credit repayment'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    today_sales['total'] += today_credit_payments

    today_credit_count = Payment.objects.filter(
        created_at__gte=today_start,
        created_at__lt=today_end,
        notes__startswith='Credit repayment'
    ).count()
    today_sales['count'] += today_credit_count

    # Yesterday's sales for comparison, using the same logic as today.
    yesterday_sales = Sale.objects.filter(
        sale_date__gte=yesterday_start,
        sale_date__lt=yesterday_end,
        status='completed'
    ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0')

    yesterday_credit_payments = Payment.objects.filter(
        created_at__gte=yesterday_start,
        created_at__lt=yesterday_end,
        notes__startswith='Credit repayment'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    yesterday_sales += yesterday_credit_payments

    # Calculate percentage change
    if yesterday_sales > 0:
        vs_yesterday = ((today_sales['total'] - yesterday_sales) / yesterday_sales) * 100
        today_sales['vs_yesterday'] = round(float(vs_yesterday), 1)
    else:
        today_sales['vs_yesterday'] = 100 if today_sales['total'] > 0 else 0

    # Weekly sales
    weekly_sales = Sale.objects.filter(
        created_at__date__gte=week_ago,
        status='completed'
    ).aggregate(
        total=Sum('total_amount'),
        count=Count('id')
    )
    weekly_sales['total'] = weekly_sales['total'] or Decimal('0')
    weekly_sales['count'] = weekly_sales['count'] or 0

    # Monthly sales
    monthly_sales = Sale.objects.filter(
        created_at__date__gte=month_ago,
        status='completed'
    ).aggregate(
        total=Sum('total_amount'),
        count=Count('id')
    )
    monthly_sales['total'] = monthly_sales['total'] or Decimal('0')
    monthly_sales['count'] = monthly_sales['count'] or 0

    # Yearly sales
    yearly_sales = Sale.objects.filter(
        created_at__date__gte=year_ago,
        status='completed'
    ).aggregate(
        total=Sum('total_amount'),
        count=Count('id')
    )
    yearly_sales['total'] = yearly_sales['total'] or Decimal('0')
    yearly_sales['count'] = yearly_sales['count'] or 0

    # ========== INVENTORY STATISTICS ==========
    # Simplified - directly from Product model (no batches)
    total_stock_quantity = 0
    total_stock_value = Decimal('0')
    total_selling_value = Decimal('0')

    for product in Product.objects.filter(is_active=True):
        stock_qty = product.current_stock or 0
        if stock_qty > 0:
            total_stock_quantity += stock_qty
            total_stock_value += stock_qty * (product.purchase_price or Decimal('0'))
            total_selling_value += stock_qty * (product.selling_price or Decimal('0'))

    # Expected profit
    expected_profit = total_selling_value - total_stock_value
    profit_percentage = (expected_profit / total_stock_value * 100) if total_stock_value > 0 else Decimal('0')

    # ========== ALERTS ==========

    # Low stock count
    low_stock_count = Product.objects.filter(
        is_active=True,
        current_stock__lte=F('reorder_level'),
        current_stock__gt=0
    ).count()

    # Out of stock count
    out_of_stock_count = Product.objects.filter(
        is_active=True,
        current_stock=0
    ).count()

    # Low stock items list
    low_stock_items = Product.objects.filter(
        is_active=True,
        current_stock__lte=F('reorder_level')
    ).order_by('current_stock')[:1]

    # ========== CHARTS DATA ==========

    # Last 7 days sales data
    sales_data = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_sales = Sale.objects.filter(
            created_at__date=day,
            status='completed'
        ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0')
        sales_data.append({
            'date': day.strftime('%d/%m'),
            'amount': float(day_sales)
        })

    # Monthly sales chart (last 6 months)
    monthly_chart_data = []
    for i in range(5, -1, -1):
        month = today.replace(day=1) - timedelta(days=30*i)
        month_start = month.replace(day=1)
        if month.month == 12:
            month_end = month.replace(day=31)
        else:
            month_end = month.replace(month=month.month+1, day=1) - timedelta(days=1)

        month_sales_total = Sale.objects.filter(
            created_at__date__gte=month_start,
            created_at__date__lte=month_end,
            status='completed'
        ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0')

        monthly_chart_data.append({
            'month': month.strftime('%b %Y'),
            'total': float(month_sales_total)
        })

    # Payment methods chart
    payment_chart_data = list(Payment.objects.filter(
        sale__status='completed',
        created_at__date__gte=month_ago
    ).values('payment_method').annotate(
        total=Sum('amount')
    ).order_by('-total'))

    payment_method_names = dict(Payment.PAYMENT_METHODS)
    for item in payment_chart_data:
        item['method'] = payment_method_names.get(item['payment_method'], item['payment_method'])
        item['total'] = float(item['total']) if item['total'] else 0

    # ========== TOP PRODUCTS ==========

    top_products = SaleItem.objects.filter(
        sale__status='completed',
        sale__created_at__date__gte=month_ago
    ).values(
        'product__id',
        'product__name',
        'product__generic_name',
        'product__current_stock',
        'product__reorder_level'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum('subtotal')
    ).order_by('-total_quantity')[:10]

    top_products_list = []
    for product in top_products:
        top_products_list.append({
            'id': product['product__id'],
            'name': product['product__name'],
            'generic_name': product['product__generic_name'] or '',
            'current_stock': product['product__current_stock'] or 0,
            'reorder_level': product['product__reorder_level'] or 0,
            'total_quantity': float(product['total_quantity']) if product['total_quantity'] else 0,
            'total_revenue': float(product['total_revenue']) if product['total_revenue'] else 0,
        })

    # ========== RECENT SALES ==========

    recent_sales = Sale.objects.filter(
        status='completed'
    ).select_related('customer', 'created_by').order_by('-created_at')[:10]

    # Recent credit records (pending/partial) to show on dashboard
    recent_credits = CreditRecord.objects.select_related('sale', 'customer').filter(
        status__in=['pending', 'partial']
    ).order_by('-updated_at', '-created_at')[:10]

    total_credit_outstanding = CreditRecord.objects.filter(
        status__in=['pending', 'partial', 'overdue']
    ).aggregate(total=Sum('remaining_balance'))['total'] or Decimal('0')
    # ========== RECENT ACTIVITIES ==========

    recent_activities = UserActivityLog.objects.select_related('user').all().order_by('-created_at')[:15]

    context = {
        'current_time': current_time,
        'today_sales': {
            'total': float(today_sales['total']),
            'count': today_sales['count'],
            'vs_yesterday': today_sales['vs_yesterday']
        },
        'weekly_sales': {
            'total': float(weekly_sales['total']),
            'count': weekly_sales['count']
        },
        'monthly_sales': {
            'total': float(monthly_sales['total']),
            'count': monthly_sales['count']
        },
        'yearly_sales': {
            'total': float(yearly_sales['total']),
            'count': yearly_sales['count']
        },
        'total_stock_value': float(total_stock_value),
        'total_selling_value': float(total_selling_value),
        'total_stock_quantity': total_stock_quantity,
        'expected_profit': float(expected_profit),
        'profit_percentage': float(profit_percentage),
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'expiring_soon_count': 0,  # No batch tracking
        'low_stock_items': low_stock_items,
        'sales_data': sales_data,
        'monthly_chart_data': monthly_chart_data,
        'payment_chart_data': payment_chart_data,
        'top_products': top_products_list,
        'recent_sales': recent_sales,
        'recent_credits': recent_credits,
        'total_credit_outstanding': float(total_credit_outstanding),
        'recent_activities': recent_activities,
    }

    return render(request, 'core/dashboard.html', context)


@login_required
@user_passes_test(lambda u: u.is_administrator or u.is_superuser)
def company_settings_view(request):
    """Company information settings"""
    company = Company.objects.first()
    if not company:
        company = Company.objects.create(name='agentflow Pharmacy')

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()

            messages.success(request, 'Company information updated successfully!')
            return redirect('core:company_settings')
    else:
        form = CompanyForm(instance=company)

    payment_methods = company.payment_methods.all()

    context = {
        'form': form,
        'company': company,
        'payment_methods': payment_methods,
    }
    return render(request, 'core/company_settings.html', context)


@login_required
@user_passes_test(lambda u: u.is_administrator or u.is_superuser)
@require_http_methods(["POST"])
def payment_method_ajax_view(request):
    """AJAX endpoint to save/delete individual payment methods immediately."""
    company = Company.objects.first()
    if not company:
        return JsonResponse({'success': False, 'error': 'No company configured.'}, status=400)

    action = request.POST.get('action', 'save')

    if action == 'delete':
        pm_id = request.POST.get('pm_id', '').strip()
        if not pm_id or pm_id.startswith('new'):
            return JsonResponse({'success': True, 'deleted': True})
        try:
            pm = PaymentMethod.objects.get(id=pm_id, company=company)
            pm.delete()
        except PaymentMethod.DoesNotExist:
            pass
        return JsonResponse({'success': True, 'deleted': True})

    bank_name = request.POST.get('bank_name', '').strip()
    account_name = request.POST.get('account_name', '').strip()
    account_number = request.POST.get('account_number', '').strip()
    is_active = request.POST.get('is_active') == 'on'

    if not bank_name or not account_number:
        return JsonResponse({'success': False, 'error': 'Bank name and account number are required.'}, status=400)

    pm_id = request.POST.get('pm_id', '').strip()
    if pm_id and not pm_id.startswith('new'):
        try:
            pm = PaymentMethod.objects.get(id=pm_id, company=company)
            pm.bank_name = bank_name
            pm.account_name = account_name
            pm.account_number = account_number
            pm.is_active = is_active
            pm.save()
            return JsonResponse({
                'success': True,
                'pm_id': str(pm.id),
                'message': 'Payment method updated.',
            })
        except PaymentMethod.DoesNotExist:
            pass

    pm = PaymentMethod.objects.create(
        company=company,
        bank_name=bank_name,
        account_name=account_name,
        account_number=account_number,
        is_active=is_active,
    )
    return JsonResponse({
        'success': True,
        'pm_id': str(pm.id),
        'message': 'Payment method added.',
    })


@login_required
@user_passes_test(lambda u: u.is_administrator or u.is_superuser)
def system_settings_view(request):
    """System settings"""
    settings = SystemSetting.objects.all()

    if request.method == 'POST':
        for setting in settings:
            value = request.POST.get(setting.setting_key)
            if value is not None:
                setting.setting_value = value
                setting.save()

        messages.success(request, 'System settings updated successfully!')
        return redirect('core:system_settings')

    settings_by_type = {}
    for setting in settings:
        settings_by_type.setdefault(setting.setting_type, []).append(setting)

    context = {
        'settings_by_type': settings_by_type,
    }
    return render(request, 'core/system_settings.html', context)


@login_required
def notifications_view(request):
    """View all notifications"""
    notifications = Notification.objects.filter(user=request.user)

    if request.GET.get('mark_all_read'):
        notifications.update(is_read=True, read_at=timezone.now())
        messages.success(request, 'All notifications marked as read')
        return redirect('core:notifications')

    notification_id = request.GET.get('read')
    if notification_id:
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        notification.mark_as_read()
        return redirect('core:notifications')

    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'notifications': page_obj,
        'unread_count': Notification.objects.filter(user=request.user, is_read=False).count(),
    }
    return render(request, 'core/notifications.html', context)


@login_required
def mark_notification_read(request, notification_id):
    if request.method == 'POST':
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        notification.mark_as_read()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
@permission_required('core.view_activitylog', raise_exception=True)
def activity_logs_view(request):
    """View system activity logs"""
    from accounts.models import UserActivityLog

    logs = UserActivityLog.objects.select_related('user').all()

    # Filter by action
    action_filter = request.GET.get('action', '')
    if action_filter:
        logs = logs.filter(action=action_filter)

    # Date range filter
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    if from_date:
        logs = logs.filter(created_at__date__gte=from_date)
    if to_date:
        logs = logs.filter(created_at__date__lte=to_date)

    # Statistics
    total_logs = logs.count()
    login_count = logs.filter(action='login').count()
    create_count = logs.filter(action='create').count()
    delete_count = logs.filter(action='delete').count()

    # Pagination
    paginator = Paginator(logs, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'logs': page_obj,
        'action_filter': action_filter,
        'from_date': from_date,
        'to_date': to_date,
        'total_logs': total_logs,
        'login_count': login_count,
        'create_count': create_count,
        'delete_count': delete_count,
    }
    return render(request, 'core/activity_logs.html', context)


@login_required
@user_passes_test(lambda u: u.is_administrator or u.is_superuser)
@login_required
@administrator_required
def backup_view(request):
    backups = Backup.objects.all().order_by('-started_at')

    if request.method == 'POST':
        form = BackupForm(request.POST)
        if form.is_valid():
            backup = form.save(commit=False)
            backup.created_by = request.user
            backup.status = 'running'
            backup.save()
            
            # Create the actual backup based on type
            backup_name = backup.name
            backup_type = backup.backup_type
            file_path = None
            file_size = 0
            error_message = ''
            
            try:
                if backup_type == 'database':
                    file_path, file_size = create_database_backup(backup_name, backup_type)
                elif backup_type == 'media':
                    file_path, file_size = create_media_backup(backup_name)
                elif backup_type == 'full':
                    file_path, file_size = create_full_backup(backup_name)
                
                if file_path and file_size > 0:
                    # Update backup record
                    backup.file_path = file_path
                    backup.file_size = file_size
                    backup.status = 'completed'
                    backup.completed_at = timezone.now()
                    backup.save()
                    messages.success(request, f'Backup created successfully! File size: {file_size / (1024*1024):.2f} MB')
                else:
                    backup.status = 'failed'
                    backup.error_message = 'Failed to create backup file'
                    backup.save()
                    messages.error(request, 'Failed to create backup file.')
            except Exception as e:
                backup.status = 'failed'
                backup.error_message = str(e)
                backup.save()
                messages.error(request, f'Backup failed: {str(e)}')
            
            return redirect('core:backup')
    else:
        form = BackupForm()

    context = {
        'backups': backups,
        'form': form,
    }
    return render(request, 'core/backup.html', context)


@login_required
@require_http_methods(["POST"])
def delete_backup(request, backup_id):
    backup = get_object_or_404(Backup, id=backup_id)
    if backup.file_path and os.path.exists(backup.file_path):
        os.remove(backup.file_path)
    backup.delete()
    messages.success(request, 'Backup deleted successfully!')
    return redirect('core:backup')


@login_required
@user_passes_test(lambda u: u.is_administrator or u.is_superuser)
@require_http_methods(["POST"])
def restore_backup(request, backup_id):
    backup = get_object_or_404(Backup, id=backup_id)

    if not backup.file_path or not os.path.exists(backup.file_path):
        messages.error(request, 'Backup file not found. Cannot restore.')
        return redirect('core:backup')

    if not backup.file_path.endswith('.sql'):
        messages.error(request, 'Only database (.sql) backups can be restored through the interface. Media/full backups must be restored manually.')
        return redirect('core:backup')

    success, message = restore_database_backup(backup.file_path)

    if success:
        messages.success(request, f'Backup "{backup.name}" restored successfully.')
    else:
        messages.error(request, f'Restore failed: {message}')

    return redirect('core:backup')


@login_required
@permission_required('core.view_activitylog', raise_exception=True)
def export_activity_logs(request):
    """Export activity logs to CSV"""
    from accounts.models import UserActivityLog

    logs = UserActivityLog.objects.select_related('user').all()

    # Apply filters
    action_filter = request.GET.get('action', '')
    if action_filter:
        logs = logs.filter(action=action_filter)

    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    if from_date:
        logs = logs.filter(created_at__date__gte=from_date)
    if to_date:
        logs = logs.filter(created_at__date__lte=to_date)

    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="activity_logs.csv"'

    writer = csv.writer(response)
    writer.writerow(['Timestamp', 'User', 'Action', 'Model', 'Description', 'IP Address'])

    for log in logs:
        writer.writerow([
            log.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            log.user.get_full_name() if log.user else 'System/Deleted',
            log.action,
            log.model_name or '',
            log.description or '',
            log.ip_address or ''
        ])

    return response


@login_required
@permission_required('accounts.delete_useractivitylog', raise_exception=True)
def delete_all_activity_logs(request):
    """Delete all activity logs"""
    if request.method == 'POST':
        # Get count before deletion
        count = UserActivityLog.objects.count()

        # Delete all logs
        UserActivityLog.objects.all().delete()

        # Log this action
        UserActivityLog.objects.create(
            user=request.user,
            action='delete',
            model_name='UserActivityLog',
            description=f'Deleted all {count} activity logs',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

        messages.success(request, f'Successfully deleted {count} activity logs.')
        return redirect('core:activity_logs')

    return redirect('core:activity_logs')


@login_required
@permission_required('accounts.delete_useractivitylog', raise_exception=True)
def delete_old_activity_logs(request):
    """Delete activity logs older than specified days"""
    if request.method == 'POST':
        days = int(request.POST.get('days', 30))

        # Calculate cutoff date
        cutoff_date = timezone.now() - timedelta(days=days)

        # Get count before deletion
        count = UserActivityLog.objects.filter(created_at__lt=cutoff_date).count()

        # Delete old logs
        UserActivityLog.objects.filter(created_at__lt=cutoff_date).delete()

        # Log this action
        UserActivityLog.objects.create(
            user=request.user,
            action='delete',
            model_name='UserActivityLog',
            description=f'Deleted {count} activity logs older than {days} days',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

        messages.success(request, f'Successfully deleted {count} activity logs older than {days} days.')
        return redirect('core:activity_logs')

    return redirect('core:activity_logs')


# Error pages
def bad_request(request, exception=None):
    """400 Bad Request error handler"""
    return render(request, '400.html', status=400)


def permission_denied(request, exception=None):
    """403 Forbidden error handler"""
    return render(request, '403.html', status=403)


def page_not_found(request, exception=None):
    """404 Page Not Found error handler"""
    return render(request, '404.html', status=404)


def server_error(request):
    """500 Internal Server Error handler"""
    return render(request, '500.html', status=500)
