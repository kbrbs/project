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
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
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


class EducationalSection(models.Model):
    """Sections like Planting, Cultural, Historical, Economic Value."""
    SLUG_MAX = 100
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=SLUG_MAX, unique=True)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


class MediaAsset(models.Model):
    TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('pdf', 'Document/PDF'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=200)
    asset_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='image')
    file = models.FileField(upload_to='media_assets/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ContentModeration(models.Model):
    STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    media = models.ForeignKey(MediaAsset, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    moderator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='moderations')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        target = self.article.title if self.article else (self.media.title if self.media else 'Unknown')
        return f'Moderation: {target} ({self.status})'


class Visit(models.Model):
    path = models.CharField(max_length=512)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.CharField(max_length=45, blank=True)
    user_agent = models.CharField(max_length=512, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Visit: {self.path} @ {self.created_at}'


class Download(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    media = models.ForeignKey(MediaAsset, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Download: {self.media} by {self.user} @ {self.created_at}'
