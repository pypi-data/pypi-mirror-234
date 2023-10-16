from django.core.management.base import no_translations, CommandError
from django.core.management.commands.migrate import Command as MigrateCommand
from django.db import connections

from isapilib.connection import add_conn


class Command(MigrateCommand):
    help = 'Migrate from external database'
    exclude_apps = ['admin', 'auth', 'contenttypes', 'oauth2_provider', 'sessions']

    def add_arguments(self, parser):
        parser.add_argument(
            "username",
            nargs="?",
            help="username",
        )
        parser.add_argument(
            "organization_id",
            nargs="?",
            help="organization_id",
        )
        super().add_arguments(parser)

    @no_translations
    def handle(self, *args, **options):
        options['database'] = add_conn(options['username'], options['organization_id'])
        if not options['app_label']:
            raise CommandError('you must specified app_name')
        elif options['app_label'] in self.exclude_apps:
            raise CommandError(f'You can´t migrate {options["app_label"]} app')

        db_host = connections[options['database']].settings_dict['HOST']
        db_name = connections[options['database']].settings_dict['NAME']
        self.stdout.write(self.style.SUCCESS(f'Running migrations on {db_host} {db_name}:'))
        super().handle(*args, **options)
