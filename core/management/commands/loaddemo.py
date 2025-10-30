from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Article, Progress
from quizzes.models import Quiz, Question


class Command(BaseCommand):
    help = 'Load demo content: articles, a quiz, a demo user and some progress.'

    def handle(self, *args, **options):
        User = get_user_model()
        # create demo users
        teacher, _ = User.objects.get_or_create(username='teacher', defaults={'is_staff': True, 'is_superuser': True})
        student, _ = User.objects.get_or_create(username='student', defaults={'is_staff': False})

        # create sample articles
        a1, _ = Article.objects.get_or_create(slug='from-root-to-cookie', defaults={
            'title': 'From Root to Cookie: The Arrowroot Journey',
            'category': 'planting',
            'excerpt': 'A short guide about how arrowroot grows and its uses.',
            'content': 'This is a demo article about arrowroot life cycle and how it becomes Minasa cookies.'
        })

        a2, _ = Article.objects.get_or_create(slug='why-bustos-celebrates-minasa', defaults={
            'title': 'Why Bustos Celebrates Minasa',
            'category': 'culture',
            'excerpt': 'The story behind the Minasa Festival.',
            'content': 'An illustrated article about the festival origins.'
        })

        # create a demo quiz
        quiz, _ = Quiz.objects.get_or_create(title='Minasa Basics Quiz', article=a1)
        # add questions if none exist
        if quiz.questions.count() == 0:
            Question.objects.create(quiz=quiz, text='What is arrowroot commonly used for?', choices=[
                {'id': 1, 'text': 'Thickening agent', 'correct': True},
                {'id': 2, 'text': 'Fuel', 'correct': False},
            ])
            Question.objects.create(quiz=quiz, text='Which town is associated with Minasa?', choices=[
                {'id': 1, 'text': 'Bustos', 'correct': True},
                {'id': 2, 'text': 'Quezon', 'correct': False},
            ])

        # add some progress entries
        Progress.objects.get_or_create(user=student, article=a1, defaults={'status': 'completed', 'score': 95.0})
        Progress.objects.get_or_create(user=student, article=a2, defaults={'status': 'incomplete'})
        Progress.objects.get_or_create(user=teacher, article=a1, defaults={'status': 'completed', 'score': 100.0})

        self.stdout.write(self.style.SUCCESS('Demo content loaded: users, articles, quiz, progress.'))
