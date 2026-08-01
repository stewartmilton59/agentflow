from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from core.models import ActivityLog

from . import services
from .forms import ExpenseCategoryForm, ExpenseForm
from .models import Expense, ExpenseCategory


def _finance_allowed(user):
    return user.is_administrator or user.is_superuser or user.role in ('manager', 'auditor')


def _finance_required(view_func):
    from functools import wraps

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login to continue.')
            return redirect('accounts:login')
        if not _finance_allowed(request.user):
            messages.error(request, 'Access Denied. You do not have permission to view financial data.')
            return redirect('core:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def _get_date_range(request):
    """Parse from/to date filters from request."""
    from_date = request.GET.get('from_date') or request.GET.get('from')
    to_date = request.GET.get('to_date') or request.GET.get('to')

    try:
        start = date.fromisoformat(from_date) if from_date else None
    except ValueError:
        start = None
    try:
        end = date.fromisoformat(to_date) if to_date else None
    except ValueError:
        end = None

    if not start:
        start = date.today().replace(day=1)
    if not end:
        end = date.today()

    if start > end:
        start, end = end, start

    return start, end


def _log(user, action, model_name, obj=None, extra=''):
    try:
        ActivityLog.objects.create(
            user=user,
            action=action,
            model_name=model_name,
            object_id=str(obj.pk) if obj else '',
            object_repr=str(obj) if obj else '',
            changes={},
            ip_address=None,
        )
    except Exception:
        pass


@login_required
@_finance_required
def finance_dashboard_view(request):
    """Main financial dashboard with P&L, estimates, charts and tables."""
    start, end = _get_date_range(request)
    period_label = f"{start.strftime('%d %b %Y')} - {end.strftime('%d %b %Y')}"

    revenue = services.get_revenue(start, end)
    cogs = services.get_cogs(start, end)
    gross_profit = services.get_gross_profit(start, end)
    expenses = services.get_expenses_total(start, end)
    purchases = services.get_purchases_total(start, end)
    net_profit = services.get_net_profit(start, end)

    stock_value = services.get_stock_value()
    stock_sale_value = services.get_stock_sale_value()
    stock_est_profit = services.get_stock_estimated_profit()
    estimated_total_profit = services.get_estimated_total_profit(start, end)

    # Realized profit breakdown for today / this week / this month / this year
    from datetime import date as _date, timedelta as _timedelta
    _today = _date.today()
    profit_today = services.get_period_profit_report(_today, _today)
    profit_week = services.get_period_profit_report(_today - _timedelta(days=6), _today)
    profit_month = services.get_period_profit_report(_today.replace(day=1), _today)
    profit_year = services.get_period_profit_report(_today.replace(month=1, day=1), _today)
    profit_periods = [
        {'key': 'today', 'label': 'Today', 'sub': 'vs yesterday', 'report': profit_today},
        {'key': 'week', 'label': 'This Week', 'sub': 'Last 7 days', 'report': profit_week},
        {'key': 'month', 'label': 'This Month', 'sub': 'Last 30 days', 'report': profit_month},
        {'key': 'year', 'label': 'This Year', 'sub': 'Year to date', 'report': profit_year},
    ]
    for period in profit_periods:
        for k in ('revenue', 'cogs', 'gross_profit', 'expenses', 'net_profit'):
            period['report'][k] = float(period['report'][k])
        period['report']['margin'] = float(period['report']['margin'])

    credit_given = services.get_total_credit_given(start, end)
    credit_collected = services.get_credit_collected(start, end)
    credit_outstanding = services.get_credit_outstanding()

    context = {
        'start': start,
        'end': end,
        'period_label': period_label,

        'revenue': float(revenue),
        'cogs': float(cogs),
        'gross_profit': float(gross_profit),
        'gross_margin': float((gross_profit / revenue * 100)) if revenue else 0.0,
        'expenses': float(expenses),
        'purchases': float(purchases),
        'net_profit': float(net_profit),
        'net_margin': float((net_profit / revenue * 100)) if revenue else 0.0,
        'sales_count': services.get_sales_count(start, end),
        'expense_count': services.get_expense_count(start, end),

        'stock_value': float(stock_value),
        'stock_sale_value': float(stock_sale_value),
        'stock_est_profit': float(stock_est_profit),
        'estimated_total_profit': float(estimated_total_profit),
        'stock_profit_margin': float((stock_est_profit / stock_value * 100)) if stock_value else 0.0,

        'profit_periods': profit_periods,

        'credit_given': float(credit_given),
        'credit_collected': float(credit_collected),
        'credit_outstanding': float(credit_outstanding),

        'payment_methods': services.get_payment_methods_breakdown(start, end),
        'expenses_by_category': services.get_expenses_by_category(start, end),
        'monthly_series': services.get_monthly_series(6, end),
        'daily_sales': services.get_daily_sales_series(7, end),
        'top_products': services.get_top_selling_products(start, end),

        'recent_expenses': services.get_recent_expenses(),
        'recent_purchases': services.get_recent_purchases(),
        'recent_sales': services.get_recent_sales(),
        'customer_credits': services.get_customer_credit_balances(),

        'frequent_categories': ExpenseCategory.objects.filter(is_frequent=True, is_active=True).order_by('name'),
        'categories': ExpenseCategory.objects.filter(is_active=True).order_by('-is_frequent', 'name'),
    }
    return render(request, 'finance/dashboard.html', context)


@login_required
@_finance_required
def expense_list_view(request):
    """List expenses with filters and quick add."""
    expenses_qs = Expense.objects.select_related('category', 'created_by').all()

    start, end = _get_date_range(request)
    expenses_qs = expenses_qs.filter(expense_date__gte=start, expense_date__lte=end)

    category_filter = request.GET.get('category', '')
    if category_filter:
        expenses_qs = expenses_qs.filter(category_id=category_filter)

    payment_filter = request.GET.get('payment_method', '')
    if payment_filter:
        expenses_qs = expenses_qs.filter(payment_method=payment_filter)

    search = request.GET.get('q', '')
    if search:
        expenses_qs = expenses_qs.filter(description__icontains=search)

    total = expenses_qs.aggregate(total=Sum('amount'))['total'] or 0

    paginator = Paginator(expenses_qs.order_by('-expense_date', '-created_at'), 25)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'expenses': page_obj,
        'start': start,
        'end': end,
        'total': float(total),
        'categories': ExpenseCategory.objects.filter(is_active=True).order_by('name'),
        'frequent_categories': ExpenseCategory.objects.filter(is_frequent=True, is_active=True),
        'category_filter': category_filter,
        'payment_filter': payment_filter,
        'search': search,
        'form': ExpenseForm(),
    }
    return render(request, 'finance/expense_list.html', context)


@login_required
@_finance_required
@require_http_methods(["POST"])
def expense_create_view(request):
    """Create a new expense."""
    form = ExpenseForm(request.POST)
    if form.is_valid():
        expense = form.save(commit=False)
        expense.created_by = request.user
        expense.save()
        _log(request.user, 'create', 'Expense', expense, f'Added expense TSh {expense.amount}')
        messages.success(request, f'Expense of TSh {expense.amount} recorded successfully.')
    else:
        errors = '; '.join(f"{field}: {', '.join(errs)}" for field, errs in form.errors.items())
        messages.error(request, f'Could not save expense: {errors or "Invalid data"}')

    next_url = request.POST.get('next', '')
    if next_url:
        return redirect(next_url)
    return redirect('finance:expense_list')


@login_required
@_finance_required
@require_http_methods(["POST"])
def expense_delete_view(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    _log(request.user, 'delete', 'Expense', expense, f'Deleted expense TSh {expense.amount}')
    expense.delete()
    messages.success(request, 'Expense deleted successfully.')
    return redirect('finance:expense_list')


@login_required
@_finance_required
def expense_category_list_view(request):
    """Expense categories list + create."""
    categories = ExpenseCategory.objects.annotate(
        expense_total=Sum('expenses__amount'),
        expense_count=Count('expenses'),
    ).order_by('-is_frequent', 'name')

    form = ExpenseCategoryForm()
    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST)
        if form.is_valid():
            cat = form.save()
            _log(request.user, 'create', 'ExpenseCategory', cat, f'Created category {cat.name}')
            messages.success(request, f'Category "{cat.name}" created successfully.')
            return redirect('finance:expense_category_list')

    context = {
        'categories': categories,
        'form': form,
        'total_spend': float(Expense.objects.aggregate(t=Sum('amount'))['t'] or 0),
        'total_count': Expense.objects.count(),
        'frequent_count': ExpenseCategory.objects.filter(is_frequent=True).count(),
    }
    return render(request, 'finance/expense_category_list.html', context)


@login_required
@_finance_required
def expense_category_edit_view(request, category_id):
    category = get_object_or_404(ExpenseCategory, id=category_id)
    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            _log(request.user, 'update', 'ExpenseCategory', category, f'Updated category {category.name}')
            messages.success(request, f'Category "{category.name}" updated successfully.')
            return redirect('finance:expense_category_list')
    else:
        form = ExpenseCategoryForm(instance=category)

    context = {'form': form, 'category': category}
    return render(request, 'finance/expense_category_form.html', context)


@login_required
@_finance_required
@require_http_methods(["POST"])
def expense_category_delete_view(request, category_id):
    category = get_object_or_404(ExpenseCategory, id=category_id)
    name = category.name
    category.delete()
    _log(request.user, 'delete', 'ExpenseCategory', None, f'Deleted category {name}')
    messages.success(request, f'Category "{name}" deleted successfully.')
    return redirect('finance:expense_category_list')


@login_required
@_finance_required
def expense_category_expenses_view(request, category_id):
    """Expenses within a single (frequent) category - grouped by category."""
    category = get_object_or_404(ExpenseCategory, id=category_id)
    start, end = _get_date_range(request)
    expenses = Expense.objects.filter(
        category=category,
        expense_date__gte=start,
        expense_date__lte=end,
    ).select_related('created_by').order_by('-expense_date')

    total = expenses.aggregate(t=Sum('amount'))['t'] or 0

    context = {
        'category': category,
        'expenses': expenses,
        'start': start,
        'end': end,
        'total': float(total),
    }
    return render(request, 'finance/expense_category_detail.html', context)


@login_required
@_finance_required
@require_http_methods(["POST"])
def expense_quick_add_ajax_view(request):
    """AJAX quick-add for expenses (used from the dashboard)."""
    form = ExpenseForm(request.POST)
    if form.is_valid():
        expense = form.save(commit=False)
        expense.created_by = request.user
        expense.save()
        _log(request.user, 'create', 'Expense', expense, f'Added expense TSh {expense.amount}')
        return JsonResponse({'success': True, 'message': 'Expense recorded.'})
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)
