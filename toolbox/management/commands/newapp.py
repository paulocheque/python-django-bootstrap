# https://docs.djangoproject.com/en/dev/howto/custom-management-commands/
import os
import shutil

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'New app'

    def handle(self, *args, **options):
        project_dir = os.getcwd()
