from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from config.settings import env


class Command(BaseCommand):
    def handle(self, *args, **options):
        username = env.str('SUPERUSER_USERNAME')
        email = env.str('SUPERUSER_EMAIL')
        password = env.str('SUPERUSER_PASSWORD')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                email=email, username=username, password=password
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created superuser {username} with password - {password}'
                )
            )
        else:
            self.stdout.write(
                f'The user with username {username} already exists'
            )
