from django.db import models
from core.models import Article


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    choices = models.JSONField(default=list)  # [{'id':1,'text':'...','correct':False}, ...]

    def __str__(self):
        return f"Q: {self.text[:40]}"
