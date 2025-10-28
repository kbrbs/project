from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = 'Send a test email using the configured Django email backend.'

    def add_arguments(self, parser):
        parser.add_argument('--to', '-t', dest='to', help='Recipient email address', required=False)
        parser.add_argument('--subject', '-s', dest='subject', help='Email subject', default='Test email from Rooted in Knowledge')
        parser.add_argument('--body', '-b', dest='body', help='Email body', default='This is a test email sent from the Django project.')

    def handle(self, *args, **options):
        to = options.get('to')
        if not to:
            # Try to use DEFAULT_TEST_EMAIL_RECIPIENT from settings if present
            to = getattr(settings, 'DEFAULT_TEST_EMAIL_RECIPIENT', None)

        if not to:
            self.stderr.write(self.style.ERROR('No recipient provided. Use --to or set DEFAULT_TEST_EMAIL_RECIPIENT in settings.'))
            return

        subject = options.get('subject')
        body = options.get('body')
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)

        try:
            sent = send_mail(subject, body, from_email, [to])
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error while sending email: {e}'))
            return

        if sent:
            self.stdout.write(self.style.SUCCESS(f'Successfully sent test email to {to} (sent={sent}).'))
        else:
            self.stderr.write(self.style.ERROR('Email backend reported 0 emails sent.'))
