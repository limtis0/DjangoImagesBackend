from django.core.management.base import BaseCommand
from users.permissions import Permissions


class Command(BaseCommand):
    help = 'Manage a permission with arbitrary height: thumbnail_permission [--delete] [height in pixels]'
    missing_args_message = 'Arguments missing: thumbnail_permission [--delete] [height in pixels]'

    def add_arguments(self, parser):
        parser.add_argument('height', type=int, help='Height of a thumbnail (in pixels)')

        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete a permission instead of creating'
        )

    def handle(self, *args, **kwargs):
        height = kwargs['height']

        codename = Permissions.get_thumbnail_size_permission_codename(height)
        name = Permissions.get_thumbnail_size_permission_name(height)

        if kwargs['delete']:
            if Permissions.delete_permission(codename):
                return self.stdout.write(f'Successfully removed permission with codename {codename}')
            return self.stdout.write(f'Permission with codename {codename} could not be found')

        if Permissions.create_permission(codename, name):
            return self.stdout.write(f'Created permission with codename "{codename}"')
        return self.stdout.write(f'Permission with codename {codename} already exists')
