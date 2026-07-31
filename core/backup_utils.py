"""Backup utilities for database and file backups"""
import os
import subprocess
from datetime import datetime
from django.conf import settings
from pathlib import Path
from django.utils import timezone


def ensure_backup_directory():
    """Ensure the Backup directory exists"""
    backup_dir = os.path.join(settings.BASE_DIR, 'Backup')
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir, exist_ok=True)
    return backup_dir


def create_database_backup(backup_name, backup_type):
    """
    Create a database backup (SQL dump)
    
    Args:
        backup_name: Name of the backup
        backup_type: Type of backup (database, media, full)
    
    Returns:
        Tuple of (file_path, file_size) or (None, 0) if failed
    """
    try:
        backup_dir = ensure_backup_directory()
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{backup_name}_{timestamp}.sql"
        file_path = os.path.join(backup_dir, filename)
        
        # Get database configuration
        db_config = settings.DATABASES['default']
        
        if db_config['ENGINE'] == 'django.db.backends.sqlite3':
            # SQLite backup - use sqlite3 command line tool or Python's built-in
            db_path = db_config['NAME']
            
            # Option 1: Use .dump command via sqlite3
            try:
                result = subprocess.run(
                    ['sqlite3', db_path, '.dump'],
                    capture_output=True,
                    text=True,
                    check=True
                )
                sql_content = result.stdout
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Fallback: Use Python's sqlite3 module
                import sqlite3
                conn = sqlite3.connect(db_path)
                with open(file_path, 'w') as f:
                    for line in conn.iterdump():
                        f.write(f'{line}\n')
                conn.close()
                file_size = os.path.getsize(file_path)
                return file_path, file_size
            
            # Write SQL content to file
            with open(file_path, 'w') as f:
                f.write(sql_content)
        
        elif db_config['ENGINE'] == 'django.db.backends.mysql':
            # MySQL backup
            cmd = [
                'mysqldump',
                f"--user={db_config.get('USER', 'root')}",
                f"--password={db_config.get('PASSWORD', '')}",
                f"--host={db_config.get('HOST', 'localhost')}",
                f"--port={db_config.get('PORT', 3306)}",
                db_config['NAME']
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            with open(file_path, 'w') as f:
                f.write(result.stdout)
        
        elif db_config['ENGINE'] == 'django.db.backends.postgresql':
            # PostgreSQL backup
            cmd = [
                'pg_dump',
                f"--username={db_config.get('USER', 'postgres')}",
                f"--host={db_config.get('HOST', 'localhost')}",
                f"--port={db_config.get('PORT', 5432)}",
                db_config['NAME']
            ]
            # Add password via environment variable if provided
            env = os.environ.copy()
            if db_config.get('PASSWORD'):
                env['PGPASSWORD'] = db_config['PASSWORD']
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, env=env)
            with open(file_path, 'w') as f:
                f.write(result.stdout)
        
        else:
            raise ValueError(f"Unsupported database backend: {db_config['ENGINE']}")
        
        # Get file size
        file_size = os.path.getsize(file_path)
        return file_path, file_size
    
    except Exception as e:
        print(f"Error creating database backup: {str(e)}")
        return None, 0


def restore_database_backup(file_path):
    """
    Restore a database from a backup SQL dump.

    Args:
        file_path: Path to the backup .sql file

    Returns:
        (success, message) tuple
    """
    try:
        if not os.path.exists(file_path):
            return False, f"Backup file not found: {file_path}"

        db_config = settings.DATABASES['default']

        if db_config['ENGINE'] == 'django.db.backends.sqlite3':
            db_path = db_config['NAME']
            import sqlite3
            with open(file_path, 'r') as f:
                sql_content = f.read()
            conn = sqlite3.connect(db_path)
            conn.executescript(sql_content)
            conn.close()

        elif db_config['ENGINE'] == 'django.db.backends.mysql':
            cmd = [
                'mysql',
                f"--user={db_config.get('USER', 'root')}",
                f"--password={db_config.get('PASSWORD', '')}",
                f"--host={db_config.get('HOST', 'localhost')}",
                f"--port={db_config.get('PORT', 3306)}",
                db_config['NAME']
            ]
            with open(file_path, 'r') as f:
                result = subprocess.run(cmd, stdin=f, capture_output=True, text=True)
            if result.returncode != 0:
                return False, f"MySQL restore failed: {result.stderr}"

        elif db_config['ENGINE'] == 'django.db.backends.postgresql':
            env = os.environ.copy()
            if db_config.get('PASSWORD'):
                env['PGPASSWORD'] = db_config['PASSWORD']
            cmd = [
                'psql',
                f"--username={db_config.get('USER', 'postgres')}",
                f"--host={db_config.get('HOST', 'localhost')}",
                f"--port={db_config.get('PORT', 5432)}",
                f"--dbname={db_config['NAME']}"
            ]
            with open(file_path, 'r') as f:
                result = subprocess.run(cmd, stdin=f, capture_output=True, text=True, env=env)
            if result.returncode != 0:
                return False, f"PostgreSQL restore failed: {result.stderr}"

        else:
            return False, f"Unsupported database backend: {db_config['ENGINE']}"

        return True, "Database restored successfully."
    except Exception as e:
        return False, f"Error restoring database: {str(e)}"


def create_media_backup(backup_name):
    """
    Create a media files backup (tar.gz)
    
    Args:
        backup_name: Name of the backup
    
    Returns:
        Tuple of (file_path, file_size) or (None, 0) if failed
    """
    try:
        backup_dir = ensure_backup_directory()
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{backup_name}_{timestamp}.tar.gz"
        file_path = os.path.join(backup_dir, filename)
        
        media_path = os.path.join(settings.BASE_DIR, 'media')
        
        if not os.path.exists(media_path):
            return None, 0
        
        # Create tar.gz archive
        import tarfile
        with tarfile.open(file_path, 'w:gz') as tar:
            tar.add(media_path, arcname='media')
        
        # Get file size
        file_size = os.path.getsize(file_path)
        return file_path, file_size
    
    except Exception as e:
        print(f"Error creating media backup: {str(e)}")
        return None, 0


def create_full_backup(backup_name):
    """
    Create a full system backup (database + media + static)
    
    Args:
        backup_name: Name of the backup
    
    Returns:
        Tuple of (file_path, file_size) or (None, 0) if failed
    """
    try:
        backup_dir = ensure_backup_directory()
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{backup_name}_{timestamp}.tar.gz"
        file_path = os.path.join(backup_dir, filename)
        
        import tarfile
        with tarfile.open(file_path, 'w:gz') as tar:
            # Add database
            db_config = settings.DATABASES['default']
            if db_config['ENGINE'] == 'django.db.backends.sqlite3':
                db_path = db_config['NAME']
                if os.path.exists(db_path):
                    tar.add(db_path, arcname='db.sqlite3')
            
            # Add media
            media_path = os.path.join(settings.BASE_DIR, 'media')
            if os.path.exists(media_path):
                tar.add(media_path, arcname='media')
            
            # Add static
            static_path = os.path.join(settings.BASE_DIR, 'static')
            if os.path.exists(static_path):
                tar.add(static_path, arcname='static')
        
        # Get file size
        file_size = os.path.getsize(file_path)
        return file_path, file_size
    
    except Exception as e:
        print(f"Error creating full backup: {str(e)}")
        return None, 0
