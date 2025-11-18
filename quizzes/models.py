from django.db import models
from core.models import Article


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True, help_text="Optional description of the quiz")

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    choices = models.TextField(blank=True, default='', help_text="Enter choices separated by commas (e.g., Choice A, Choice B, Choice C)")
    correct_answer = models.CharField(max_length=200, blank=True, default='', help_text="Enter the exact correct answer as it appears in choices")

    def __str__(self):
        return f"Q: {self.text[:40]}"
    
    def get_choices_list(self):
        """Return choices as a list of strings"""
        if not self.choices:
            return []
        return [choice.strip() for choice in self.choices.split(',') if choice.strip()]
    
    def get_choices_json(self):
        """Return choices in the format expected by the frontend"""
        choices_list = self.get_choices_list()
        return [
            {
                'id': idx + 1,
                'text': choice,
                'correct': choice == self.correct_answer.strip()
            }
            for idx, choice in enumerate(choices_list)
        ]

