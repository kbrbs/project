from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import EducationalSection, Article, MediaAsset, ContentModeration, StudentProfile
from quizzes.models import Quiz, Question
from django.contrib.auth import get_user_model
import random


class Command(BaseCommand):
    help = 'Load sample content (sections, articles, media, quizzes) for demo and testing.'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample sections...')
        sections = [
            ('Planting & Science', 'planting'),
            ('Culture & History', 'culture'),
            ('Economics & Sustainability', 'economics'),
            ('Creative Minasa', 'creative'),
        ]
        sec_objs = []
        for i, (title, slug) in enumerate(sections, start=1):
            obj, _ = EducationalSection.objects.get_or_create(slug=slug, defaults={'title': title, 'description': f'Sample content for {title}', 'content': f'Full content for {title}', 'order': i})
            sec_objs.append(obj)

        self.stdout.write('Creating sample articles...')
        for i, s in enumerate(sec_objs, start=1):
            a_title = f'Sample Lesson {i}: {s.title}'
            a_slug = slugify(a_title)
            Article.objects.get_or_create(slug=a_slug, defaults={'title': a_title, 'category': s.slug if s.slug in dict(Article.CATEGORY_CHOICES) else 'creative', 'excerpt': 'An example excerpt', 'content': f'Long form content for {a_title}'})

        self.stdout.write('Creating media assets...')
        for i in range(1,5):
            MediaAsset.objects.get_or_create(title=f'Sample Image {i}', defaults={'asset_type': 'image', 'url': f'https://placehold.co/600x400?text=Image+{i}'})

        self.stdout.write('Creating quizzes...')
        for a in Article.objects.all()[:4]:
            q, _ = Quiz.objects.get_or_create(title=f'Quiz for {a.title}', article=a)
            # create one sample question if none
            if not q.questions.exists():
                Question.objects.create(quiz=q, text='What is this sample question?', choices=[{'id':1,'text':'Option A','correct':False},{'id':2,'text':'Option B','correct':True}])

        self.stdout.write(self.style.SUCCESS('Sample content created.'))