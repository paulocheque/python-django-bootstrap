# https://docs.djangoproject.com/en/dev/howto/custom-management-commands/

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Count users'

    def add_arguments(self, parser):
        parser.add_argument('obj_name', nargs='+', type=int)

    def handle(self, *args, **options):
        try:
            print(User.objects.count())
        except User.DoesNotExist:
            raise CommandError('Ops')
            self.stdout.write('Success')
