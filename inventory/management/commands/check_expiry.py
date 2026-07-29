from django.core.management.base import BaseCommand
from django.utils import timezone
from inventory.models import Batch, StockAlert
from core.models import Notification
from accounts.models import User

class Command(BaseCommand):
    help = 'Check for expired and expiring products'

    def handle(self, *args, **options):
        today = timezone.now().date()

        # Check for expiring soon (within 90 days)
        expiring_batches = Batch.objects.filter(
            expiry_date__lte=today + timezone.timedelta(days=90),
            expiry_date__gte=today,
            is_active=True,
            remaining_quantity__gt=0
        )

        for batch in expiring_batches:
            days_until = (batch.expiry_date - today).days
            alert, created = StockAlert.objects.get_or_create(
                product=batch.product,
                batch=batch,
                alert_type='expiring_soon',
                defaults={
                    'message': f'Batch {batch.batch_number} will expire in {days_until} days',
                    'current_value': days_until,
                    'threshold_value': 90,
                }
            )

            if created:
                self.stdout.write(self.style.WARNING(f'Created expiry alert for {batch.product.name}'))

        # Check for expired
        expired_batches = Batch.objects.filter(
            expiry_date__lt=today,
            is_active=True,
            remaining_quantity__gt=0
        )

        for batch in expired_batches:
            alert, created = StockAlert.objects.get_or_create(
                product=batch.product,
                batch=batch,
                alert_type='expired',
                defaults={
                    'message': f'Batch {batch.batch_number} has expired',
                    'current_value': (today - batch.expiry_date).days,
                    'threshold_value': 0,
                }
            )

            if created:
                self.stdout.write(self.style.ERROR(f'Created expired alert for {batch.product.name}'))

        self.stdout.write(self.style.SUCCESS('Expiry check completed'))