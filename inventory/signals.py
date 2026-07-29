from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Product, StockAlert
from core.models import Notification


@receiver(post_save, sender=Product)
def check_product_alerts(sender, instance, created, **kwargs):
    """Check for stock and expiry alerts when a product is saved"""
    if instance.current_stock <= instance.reorder_level and instance.current_stock > 0:
        alert, alert_created = StockAlert.objects.get_or_create(
            product=instance,
            alert_type='low_stock',
            defaults={
                'message': f'Product {instance.name} is low on stock. Current: {instance.current_stock}, Threshold: {instance.reorder_level}',
                'current_value': instance.current_stock,
                'threshold_value': instance.reorder_level,
            }
        )
        if alert_created:
            from accounts.models import User
            admins = User.objects.filter(role='admin', is_active=True)
            for admin in admins:
                Notification.objects.create(
                    user=admin,
                    title='Low Stock Alert',
                    message=f'Product {instance.name} is low on stock. Please reorder.',
                    notification_type='warning',
                    link='/inventory/stock/alerts/'
                )
    else:
        StockAlert.objects.filter(
            product=instance,
            alert_type='low_stock',
            status='active'
        ).update(status='resolved', resolved_at=timezone.now())

    if instance.expiry_date:
        days_until = (instance.expiry_date - timezone.now().date()).days
        if 0 < days_until <= 90:
            alert, alert_created = StockAlert.objects.get_or_create(
                product=instance,
                alert_type='expiring_soon',
                defaults={
                    'message': f'Product {instance.name} batch {instance.batch_number or "N/A"} will expire in {days_until} days',
                    'current_value': days_until,
                    'threshold_value': 90,
                }
            )
            if alert_created:
                from accounts.models import User
                admins = User.objects.filter(role='admin', is_active=True)
                for admin in admins:
                    Notification.objects.create(
                        user=admin,
                        title='Expiry Alert',
                        message=f'Product {instance.name} batch {instance.batch_number or "N/A"} will expire in {days_until} days',
                        notification_type='warning',
                        link='/inventory/reports/expiry/'
                    )
            else:
                alert.message = f'Product {instance.name} batch {instance.batch_number or "N/A"} will expire in {days_until} days'
                alert.current_value = days_until
                alert.save(update_fields=['message', 'current_value'])
        elif days_until < 0:
            alert, alert_created = StockAlert.objects.get_or_create(
                product=instance,
                alert_type='expired',
                defaults={
                    'message': f'Product {instance.name} batch {instance.batch_number or "N/A"} has expired',
                    'current_value': abs(days_until),
                    'threshold_value': 0,
                }
            )
            if not alert_created:
                alert.message = f'Product {instance.name} batch {instance.batch_number or "N/A"} has expired'
                alert.current_value = abs(days_until)
                alert.save(update_fields=['message', 'current_value'])
        else:
            StockAlert.objects.filter(
                product=instance,
                alert_type__in=['expiring_soon', 'expired'],
                status='active'
            ).update(status='resolved', resolved_at=timezone.now())
