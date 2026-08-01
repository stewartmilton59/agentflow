"""Financial calculations for the pharmacy (profit & loss, estimates, charts)."""
from decimal import Decimal

from django.db.models import Sum, Count
from django.utils import timezone
from django.utils.timezone import timedelta

from sales.models import Sale, SaleItem, Payment, CreditRecord
from purchases.models import PurchaseOrder
from inventory.models import Product
from .models import Expense

ZERO = Decimal('0.00')


def _d(value):
    return Decimal(value) if value is not None else ZERO


def get_period_sales(start=None, end=None):
    """Completed sales in a date range."""
    qs = Sale.objects.filter(status='completed')
    if start:
        qs = qs.filter(sale_date__date__gte=start)
    if end:
        qs = qs.filter(sale_date__date__lte=end)
    return qs


def get_revenue(start=None, end=None):
    """Total revenue from completed sales (gross, including tax)."""
    return _d(get_period_sales(start, end).aggregate(t=Sum('total_amount'))['t'])


def get_cogs(start=None, end=None):
    """Cost of goods sold = quantity sold x product purchase price."""
    qs = SaleItem.objects.filter(sale__status='completed', product__isnull=False)
    if start:
        qs = qs.filter(sale__sale_date__date__gte=start)
    if end:
        qs = qs.filter(sale__sale_date__date__lte=end)

    cogs = ZERO
    for item in qs.select_related('product'):
        purchase_price = item.product.purchase_price if item.product.purchase_price else ZERO
        cogs += (item.quantity * purchase_price)
    return cogs


def get_gross_profit(start=None, end=None):
    return get_revenue(start, end) - get_cogs(start, end)


def get_purchases_total(start=None, end=None):
    """Total spent on completed purchase orders."""
    qs = PurchaseOrder.objects.filter(status='completed')
    if start:
        qs = qs.filter(order_date__date__gte=start)
    if end:
        qs = qs.filter(order_date__date__lte=end)
    return _d(qs.aggregate(t=Sum('total_amount'))['t'])


def get_expenses_total(start=None, end=None):
    """Total recorded expenses in a date range."""
    qs = Expense.objects.all()
    if start:
        qs = qs.filter(expense_date__gte=start)
    if end:
        qs = qs.filter(expense_date__lte=end)
    return _d(qs.aggregate(t=Sum('amount'))['t'])


def get_credit_outstanding():
    """Outstanding balance customers still owe."""
    return _d(CreditRecord.objects.filter(
        status__in=['pending', 'partial', 'overdue']
    ).aggregate(t=Sum('remaining_balance'))['t'])


def get_credit_collected(start=None, end=None):
    """Total credit repayments received in the period."""
    qs = Payment.objects.filter(notes__startswith='Credit repayment')
    if start:
        qs = qs.filter(created_at__date__gte=start)
    if end:
        qs = qs.filter(created_at__date__lte=end)
    return _d(qs.aggregate(t=Sum('amount'))['t'])


def get_total_credit_given(start=None, end=None):
    """Total credit issued on sales in the period."""
    qs = CreditRecord.objects.all()
    if start:
        qs = qs.filter(created_at__date__gte=start)
    if end:
        qs = qs.filter(created_at__date__lte=end)
    return _d(qs.aggregate(t=Sum('credit_amount'))['t'])


def get_stock_value():
    """Value of current stock at purchase price (cost)."""
    total = ZERO
    for product in Product.objects.filter(is_active=True):
        total += (product.current_stock or 0) * (product.purchase_price or ZERO)
    return total


def get_stock_sale_value():
    """Value of current stock at selling price (potential revenue)."""
    total = ZERO
    for product in Product.objects.filter(is_active=True):
        price = product.selling_price or product.purchase_price or ZERO
        total += (product.current_stock or 0) * price
    return total


def get_stock_estimated_profit():
    """Potential profit locked in remaining stock."""
    return get_stock_sale_value() - get_stock_value()


def get_net_profit(start=None, end=None):
    """Net profit = gross profit - expenses."""
    return get_gross_profit(start, end) - get_expenses_total(start, end)


def get_period_profit_report(start=None, end=None):
    """Realized profit breakdown for a date range (revenue/COGS/gross/expenses/net)."""
    revenue = get_revenue(start, end)
    cogs = get_cogs(start, end)
    gross = revenue - cogs
    expenses = get_expenses_total(start, end)
    net = gross - expenses
    return {
        'start': start,
        'end': end,
        'revenue': revenue,
        'cogs': cogs,
        'gross_profit': gross,
        'expenses': expenses,
        'net_profit': net,
        'sales_count': get_sales_count(start, end),
        'margin': (net / revenue * 100) if revenue else ZERO,
    }


def get_estimated_total_profit(start=None, end=None):
    """Realized gross profit + estimated profit on remaining stock - expenses."""
    return get_gross_profit(start, end) + get_stock_estimated_profit() - get_expenses_total(start, end)


def get_sales_count(start=None, end=None):
    return get_period_sales(start, end).count()


def get_expense_count(start=None, end=None):
    qs = Expense.objects.all()
    if start:
        qs = qs.filter(expense_date__gte=start)
    if end:
        qs = qs.filter(expense_date__lte=end)
    return qs.count()


def get_payment_methods_breakdown(start=None, end=None):
    """Payments received grouped by method."""
    qs = Payment.objects.all()
    if start:
        qs = qs.filter(created_at__date__gte=start)
    if end:
        qs = qs.filter(created_at__date__lte=end)
    data = qs.values('payment_method').annotate(total=Sum('amount'), count=Count('id')).order_by('-total')
    method_names = dict(Payment.PAYMENT_METHODS)
    result = []
    for row in data:
        result.append({
            'method': method_names.get(row['payment_method'], row['payment_method']),
            'method_key': row['payment_method'],
            'total': float(_d(row['total'])),
            'count': row['count'],
        })
    return result


def get_expenses_by_category(start=None, end=None):
    """Expenses grouped by category (for charts and frequent-expense grouping)."""
    qs = Expense.objects.all()
    if start:
        qs = qs.filter(expense_date__gte=start)
    if end:
        qs = qs.filter(expense_date__lte=end)
    data = qs.values('category__name', 'category__color', 'category__is_frequent').annotate(
        total=Sum('amount'), count=Count('id')
    ).order_by('-total')
    result = []
    for row in data:
        result.append({
            'name': row['category__name'] or 'Uncategorized',
            'color': row['category__color'] or '#6c757d',
            'is_frequent': row['category__is_frequent'],
            'total': float(_d(row['total'])),
            'count': row['count'],
        })
    return result


def get_monthly_series(months=6, end=None):
    """Revenue, expenses and net profit for the last N months (for charts)."""
    end_date = end or timezone.localdate()
    month = end_date.replace(day=1)
    months_list = []
    for i in range(months - 1, -1, -1):
        y = month.year
        m = month.month - i
        while m <= 0:
            m += 12
            y -= 1
        start = timezone.datetime(y, m, 1).date()
        if m == 12:
            next_month = timezone.datetime(y + 1, 1, 1).date()
        else:
            next_month = timezone.datetime(y, m + 1, 1).date()
        end = next_month - timedelta(days=1)
        months_list.append({
            'label': start.strftime('%b %Y'),
            'revenue': float(get_revenue(start, end)),
            'expenses': float(get_expenses_total(start, end)),
            'profit': float(get_net_profit(start, end)),
        })
    return months_list


def get_daily_sales_series(days=7, end=None):
    """Daily revenue for the last N days."""
    end_date = end or timezone.localdate()
    series = []
    for i in range(days - 1, -1, -1):
        day = end_date - timedelta(days=i)
        series.append({
            'label': day.strftime('%d/%m'),
            'revenue': float(get_revenue(day, day)),
        })
    return series


def get_top_selling_products(start=None, end=None):
    """Best-selling products by revenue in the period."""
    qs = SaleItem.objects.filter(sale__status='completed').values(
        'product__name',
        'product__generic_name',
        'product__purchase_price',
    ).annotate(
        qty=Sum('quantity'),
        revenue=Sum('subtotal'),
    ).order_by('-revenue')[:8]
    result = []
    for row in qs:
        cost = (row['qty'] or 0) * (row['product__purchase_price'] or ZERO)
        result.append({
            'name': row['product__name'],
            'generic_name': row['product__generic_name'] or '',
            'qty': row['qty'] or 0,
            'revenue': float(_d(row['revenue'])),
            'cost': float(cost),
            'profit': float(_d(row['revenue']) - cost),
        })
    return result


def get_recent_expenses(limit=10):
    return Expense.objects.select_related('category', 'created_by').order_by('-expense_date', '-created_at')[:limit]


def get_recent_purchases(limit=5):
    return PurchaseOrder.objects.filter(status='completed').order_by('-order_date')[:limit]


def get_recent_sales(limit=5):
    return Sale.objects.filter(status='completed').select_related('customer').order_by('-sale_date')[:limit]


def get_customer_credit_balances():
    return CreditRecord.objects.filter(status__in=['pending', 'partial', 'overdue']).select_related(
        'customer'
    ).order_by('-remaining_balance')[:8]
