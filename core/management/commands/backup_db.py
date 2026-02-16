from django.core.management.base import BaseCommand
from django.conf import settings
import shutil
import os
import datetime

class Command(BaseCommand):
    help = 'Backs up the database'

    def handle(self, *args, **options):
        db_engine = settings.DATABASES['default']['ENGINE']
        
        if 'sqlite3' in db_engine:
            db_path = settings.DATABASES['default']['NAME']
            backup_dir = settings.BASE_DIR / 'backups'
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = backup_dir / f"db_backup_{timestamp}.sqlite3"
            
            shutil.copy2(db_path, backup_file)
            self.stdout.write(self.style.SUCCESS(f"Database backed up to: {backup_file}"))
        else:
            self.stdout.write(self.style.WARNING("PostgreSQL backup not implemented in this local version (requires pg_dump)."))
