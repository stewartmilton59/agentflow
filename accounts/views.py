from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, HttpResponseForbidden
from .models import User, UserProfile, UserActivityLog, LoginAttempt
from .forms import (LoginForm, UserRegistrationForm, ProfileUpdateForm,
                   UserProfileForm, CustomPasswordChangeForm, UserUpdateForm)
from .decorators import admin_required, manager_required, role_required
import json


def login_view(request):
    """Custom login view"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    login_attempts_count = 0
    ip_address = request.META.get('REMOTE_ADDR', '127.0.0.1')

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Check if account is locked
            attempt_record = LoginAttempt.objects.filter(username=email, ip_address=ip_address).first()
            if attempt_record and attempt_record.is_locked():
                messages.error(request, 'Account is temporarily locked due to too many failed attempts. Please try again later.')
                return render(request, 'accounts/login.html', {'form': form, 'login_attempts_count': attempt_record.attempt_count})

            user = authenticate(request, username=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    user.last_activity = timezone.now()
                    user.is_online = True
                    user.save()

                    # Clear login attempts on successful login
                    LoginAttempt.objects.filter(username=email, ip_address=ip_address).delete()

                    UserActivityLog.objects.create(
                        user=user,
                        action='login',
                        description=f'User logged in from IP {ip_address}',
                        ip_address=ip_address,
                        user_agent=request.META.get('HTTP_USER_AGENT', '')
                    )

                    messages.success(request, f'Welcome back, {user.get_full_name()}!')

                    next_url = request.GET.get('next', 'sales:pos_table')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Your account is disabled.')
            else:
                # Record failed login attempt
                attempt_record, created = LoginAttempt.objects.get_or_create(
                    username=email,
                    ip_address=ip_address,
                    defaults={'attempt_count': 1}
                )
                if not created:
                    attempt_record.attempt_count += 1
                    # Lock account after 5 failed attempts for 30 minutes
                    if attempt_record.attempt_count >= 5:
                        attempt_record.locked_until = timezone.now() + timezone.timedelta(minutes=30)
                    attempt_record.save()

                login_attempts_count = attempt_record.attempt_count
                remaining = max(0, 5 - login_attempts_count)
                if remaining > 0:
                    messages.error(request, f'Invalid email or password. {remaining} attempts remaining before lockout.')
                else:
                    messages.error(request, 'Account locked due to too many failed attempts. Try again in 30 minutes.')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form, 'login_attempts_count': login_attempts_count})


@login_required
def logout_view(request):
    """Custom logout view"""
    UserActivityLog.objects.create(
        user=request.user,
        action='logout',
        description='User logged out',
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )

    request.user.is_online = False
    request.user.save()
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('accounts:login')

@login_required
def profile_view(request):
    """User profile view - All authenticated users can access"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            UserActivityLog.objects.create(
                user=request.user,
                action='update',
                model_name='UserProfile',
                description='Updated profile information',
                ip_address=request.META.get('REMOTE_ADDR')
            )

            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
    else:
        user_form = ProfileUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def change_password_view(request):
    """Change password view - All authenticated users can access"""
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            UserActivityLog.objects.create(
                user=request.user,
                action='update',
                description='Changed password',
                ip_address=request.META.get('REMOTE_ADDR')
            )

            messages.success(request, 'Your password has been changed successfully!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})

# User Management - Only Managers and Admins
@login_required
@manager_required
def user_list_view(request):
    """List all users - Managers and Admins only"""
    users = User.objects.all()

    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    # Role filter
    role_filter = request.GET.get('role', '')
    if role_filter:
        users = users.filter(role=role_filter)

    # Pagination
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'users': page_obj,
        'search_query': search_query,
        'role_filter': role_filter,
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(is_active=True).count(),
        'role_counts': {
            'admin': User.objects.filter(role='admin').count(),
            'manager': User.objects.filter(role='manager').count(),
            'pharmacist': User.objects.filter(role='pharmacist').count(),
            'cashier': User.objects.filter(role='cashier').count(),
            'auditor': User.objects.filter(role='auditor').count(),
            'saler': User.objects.filter(role='saler').count(),
        },
    }
    return render(request, 'accounts/user_list.html', context)

@login_required
@manager_required
def user_detail_view(request, pk):
    """View user details - Managers and Admins only"""
    user = get_object_or_404(User, id=pk)

    # Get or create profile (to avoid DoesNotExist error)
    profile, created = UserProfile.objects.get_or_create(user=user)

    # If profile was just created, set a default role
    if created:
        profile.role = 'cashier'
        profile.save()

    activity_logs = UserActivityLog.objects.filter(user=user)[:20]

    context = {
        'user_detail': user,
        'profile': profile,
        'activity_logs': activity_logs,
    }
    return render(request, 'accounts/user_detail.html', context)

@login_required
@admin_required
def user_create_view(request):
    """Create new user - Admins only"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Use get_or_create instead of create to avoid IntegrityError
            UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': user.role}  # Set default role from user if available
            )

            UserActivityLog.objects.create(
                user=request.user,
                action='create',
                model_name='User',
                object_id=str(user.id),
                description=f'Created user: {user.email}',
                ip_address=request.META.get('REMOTE_ADDR')
            )

            messages.success(request, f'User {user.email} has been created successfully!')
            return redirect('accounts:user_list')
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Create User'})


@login_required
@admin_required
def user_edit_view(request, pk):
    """Edit user - Admins only"""
    user = get_object_or_404(User, id=pk)

    # Get or create profile
    profile, created = UserProfile.objects.get_or_create(user=user)
    if created:
        profile.role = 'cashier'
        profile.save()

    if request.method == 'POST':
        user_form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            UserActivityLog.objects.create(
                user=request.user,
                action='update',
                model_name='User',
                object_id=str(user.id),
                description=f'Edited user: {user.email}',
                ip_address=request.META.get('REMOTE_ADDR')
            )

            messages.success(request, f'User {user.email} has been updated successfully!')
            return redirect('accounts:user_list')
    else:
        user_form = ProfileUpdateForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_edit': user,
        'title': 'Edit User',
    }
    return render(request, 'accounts/user_form.html', context)

@login_required
@admin_required
def user_delete_view(request, pk):
    """Delete user - Admins only"""
    user = get_object_or_404(User, id=pk)

    if request.method == 'POST':
        if user == request.user:
            messages.error(request, 'You cannot delete your own account!')
            return redirect('accounts:user_list')

        email = user.email
        user.delete()

        UserActivityLog.objects.create(
            user=request.user,
            action='delete',
            model_name='User',
            object_id=str(pk),
            description=f'Deleted user: {email}',
            ip_address=request.META.get('REMOTE_ADDR')
        )

        messages.success(request, f'User {email} has been deleted successfully!')
        return redirect('accounts:user_list')

    return HttpResponseForbidden()

# Activity Logs - Only Admins and Auditors
@login_required
@role_required(['admin', 'auditor'])
def activity_log_view(request):
    """View user activity logs - Admins and Auditors only"""
    logs = UserActivityLog.objects.all()

    # Filter by user if not admin
    if request.user.role == 'auditor':
        logs = logs.filter(user=request.user)

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

    # Pagination
    paginator = Paginator(logs, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'logs': page_obj,
        'action_filter': action_filter,
        'from_date': from_date,
        'to_date': to_date,
        'user_role': request.user.role,
    }
    return render(request, 'accounts/activity_log.html', context)