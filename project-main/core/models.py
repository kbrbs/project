from django.db import models
from django.conf import settings


class Article(models.Model):
    CATEGORY_CHOICES = [
        ('planting', 'Planting & Science'),
        ('culture', 'Culture & History'),
        ('economics', 'Economics & Sustainability'),
        ('creative', 'Creative Minasa'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    pdf = models.FileField(upload_to='pdfs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Progress(models.Model):
    STATUS_CHOICES = [
        ('incomplete', 'Incomplete'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    quiz_id = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='incomplete')
    score = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        label = self.article.title if self.article else f'Quiz {self.quiz_id}'
        return f"Progress: {self.user} - {label} ({self.status})"


class StudentProfile(models.Model):
    """Profile information for student users."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, blank=True)
    birthday = models.DateField(null=True, blank=True)
    grade = models.PositiveSmallIntegerField(null=True, blank=True)
    must_change_password = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def age(self):
        from datetime import date
        if not self.birthday:
            return None
        today = date.today()
        age = today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        return age

    def __str__(self):
        return f"Profile: {self.user.username}"
