from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create or update an admin user. Defaults provided for convenience.'

    def add_arguments(self, parser):
        parser.add_argument('--email', dest='email', help='Email for admin user', default='katrinamicaellabarbosa@gmail.com')
        parser.add_argument('--username', dest='username', help='Username for admin user', default='admin kat')
        parser.add_argument('--password', dest='password', help='Password for admin user', default='Administrator')

    def handle(self, *args, **options):
        User = get_user_model()
        email = options.get('email')
        username = options.get('username')
        password = options.get('password')

        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        if not created:
            # update email if changed
            if user.email != email:
                user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Admin user created: {username} ({email})'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Admin user updated: {username} ({email})'))
