from django.core.management import call_command
from django.core.management.base import BaseCommand
from isapilib.connection import add_conn


class Command(BaseCommand):
    help = 'Migrate to external database'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username')
        parser.add_argument('organization_id', type=str, help='OrganizationID')

    def handle(self, *args, **options):
        conn_name = add_conn(options['username'], options['organization_id'])
        call_command('migrate', database=conn_name)
