from celery import shared_task
from django.core.management import call_command
from django.utils import timezone
from django.conf import settings
import os
import shutil
import zipfile
from .models import Backup, Notification

@shared_task
def create_backup(backup_id):
    """Create system backup"""
    backup = Backup.objects.get(id=backup_id)

    try:
        backup.status = 'running'
        backup.save()

        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)

        if backup.backup_type == 'database':
            # Create database backup
            backup_file = os.path.join(backup_dir, f"{backup.name}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.sql")
            with open(backup_file, 'w') as f:
                call_command('dumpdata', stdout=f)

            # Compress
            zip_path = backup_file + '.zip'
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(backup_file, os.path.basename(backup_file))

            backup.file_path = zip_path
            backup.file_size = os.path.getsize(zip_path)
            os.remove(backup_file)

        elif backup.backup_type == 'media':
            # Create media files backup
            media_dir = settings.MEDIA_ROOT
            backup_file = os.path.join(backup_dir, f"{backup.name}_{timezone.now().strftime('%Y%m%d_%H%M%S')}_media.zip")

            with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(media_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, media_dir)
                        zipf.write(file_path, arcname)

            backup.file_path = backup_file
            backup.file_size = os.path.getsize(backup_file)

        backup.status = 'completed'
        backup.completed_at = timezone.now()
        backup.save()

        # Create notification for user
        Notification.objects.create(
            user=backup.created_by,
            title='Backup Completed',
            message=f'Backup "{backup.name}" has been completed successfully.',
            notification_type='success',
            link='/core/backup/'
        )

    except Exception as e:
        backup.status = 'failed'
        backup.error_message = str(e)
        backup.save()

        Notification.objects.create(
            user=backup.created_by,
            title='Backup Failed',
            message=f'Backup "{backup.name}" failed: {str(e)}',
            notification_type='error',
            link='/core/backup/'
        )