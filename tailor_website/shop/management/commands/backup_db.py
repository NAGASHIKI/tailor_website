import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
import datetime

class Command(BaseCommand):
    help = 'Backup the database'

    def handle(self, *args, **kwargs):
        db_path = settings.DATABASES['default']['NAME']
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        backup_file = os.path.join(backup_dir, f'db_backup_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.sqlite3')

        shutil.copyfile(db_path, backup_file)
        self.stdout.write(self.style.SUCCESS(f'Database backup created at {backup_file}'))
