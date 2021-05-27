from django.db import connection
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'List tables in db'

    # def add_arguments(self, parser):
    #     parser.add_argument('--poll_seconds', type=float, default=3)
    #     parser.add_argument('--max_retries', type=int, default=60)

    def handle(self, *args, **options):
        tables = connection.introspection.table_names()
        print(tables)

        # seen_models = connection.introspection.installed_models(tables)
        # print([f.name for f in list(seen_models)[4]._meta.get_fields()])
        