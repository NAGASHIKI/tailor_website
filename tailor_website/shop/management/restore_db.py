import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Restore the database from a backup file'

    def add_arguments(self, parser):
        parser.add_argument('backup_file', type=str, help='The backup file to restore')

    def handle(self, *args, **kwargs):
        db_path = settings.DATABASES['default']['NAME']
        backup_file = kwargs['backup_file']

        if not os.path.exists(backup_file):
            self.stdout.write(self.style.ERROR(f'Backup file {backup_file} does not exist'))
            return

        shutil.copyfile(backup_file, db_path)
        self.stdout.write(self.style.SUCCESS(f'Database restored from {backup_file}'))
