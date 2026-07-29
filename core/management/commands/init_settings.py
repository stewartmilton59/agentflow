from django.core.management.base import BaseCommand
from core.models import Company, SystemSetting

class Command(BaseCommand):
    help = 'Initialize system settings'

    def handle(self, *args, **options):
        # Create company if not exists
        company, created = Company.objects.get_or_create(
            name='PharmaFlow Pharmacy',
            defaults={
                'email': 'info@pharmaflow.com',
                'phone': '+255123456789',
                'currency': 'TZS',
                'currency_symbol': 'TSh',
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Company created successfully'))

        # Create default system settings
        default_settings = [
            ('site_name', 'PharmaFlow', 'general', 'Site name'),
            ('items_per_page', '20', 'general', 'Items per page in lists'),
            ('low_stock_threshold', '10', 'inventory', 'Low stock alert threshold'),
            ('expiry_alert_days', '90', 'inventory', 'Days before expiry to alert'),
            ('auto_backup_enabled', 'true', 'backup', 'Enable automatic backups'),
            ('backup_frequency', 'daily', 'backup', 'Backup frequency'),
            ('backup_retention_days', '30', 'backup', 'Number of days to keep backups'),
        ]

        for key, value, setting_type, desc in default_settings:
            setting, created = SystemSetting.objects.get_or_create(
                setting_key=key,
                defaults={
                    'setting_value': value,
                    'setting_type': setting_type,
                    'description': desc,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Setting {key} created'))

        self.stdout.write(self.style.SUCCESS('System initialization completed'))