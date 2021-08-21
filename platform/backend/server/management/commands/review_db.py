from django.db import connection
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '''Shorcuts for review database'''

    def add_arguments(self, parser):
        parser.add_argument('--table', type=str, default='')
        parser.add_argument('--columns', default=False, action='store_true')
        parser.add_argument('--join', type=str, default='')
        parser.add_argument('--select', type=str, default='*')
        parser.add_argument('--where', type=str, default='')

    def handle(self, *args, **options):
        table = options.get('table')
        columns = options.get('columns')
        
        if table == '':
            tables = connection.introspection.table_names()
            print(tables)
        elif columns:
            cursor = connection.cursor()
            cursor.execute(
                f'''
                    SELECT *
                    FROM information_schema.columns
                    WHERE table_name = '{table}'
                '''
            )
            print('\n'.join([str(line) for line in cursor.fetchall()]))
        else:
            join = options.get('join').split('.')
            select = options.get('select')
            where = options.get('where')
 
            join_raw = ''
            if len(join) == 2:
                join_raw = f'LEFT JOIN {join[0]} ON {table}.{join[1]} = {join[0]}.id'

            where_raw = where if where == '' else f'WHERE {where}'

            cursor = connection.cursor()
            cursor.execute(
                f'''
                    SELECT {select}
                    FROM {table}
                    {join_raw}
                    {where_raw}
                '''
            )
            print('\n'.join([str(line) for line in cursor.fetchall()]))

        