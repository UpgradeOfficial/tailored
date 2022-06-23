from account.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Delete users'

    def add_arguments(self, parser):
        parser.add_argument('-user_id', nargs='+', type=int, help='User ID')
        
    # Optional argument
        parser.add_argument('-p', '--prefix', type=str, help='Define a username prefix', )
        

    def handle(self, *args, **kwargs):
        users_ids = kwargs['user_id']
        prefix = kwargs['prefix']
        
        if prefix == 'all':
            User.objects.filter(is_superuser=False).delete()
        else:

            for user_id in users_ids:
                try:
                    user = User.objects.get(pk=user_id)
                    user.delete()
                    self.stdout.write(self.style.SUCCESS('User "%s (%s)" deleted with success!' % (user.username, user_id)))
                except User.DoesNotExist:
                    self.stdout.write(self.style.WARNING('User with id "%s" does not exist.' % user_id))
