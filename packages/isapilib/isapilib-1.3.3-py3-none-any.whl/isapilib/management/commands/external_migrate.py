from django.core.management.commands.migrate import Command as MigrateCommand

from isapilib.connection import add_conn


class ExternalMigrate(MigrateCommand):
    def handle(self, *args, **options):
        options["database"] = add_conn(options['username'], options['organization_id'])
        super().handle(*args, **options)
