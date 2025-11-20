from django.db import models
from django.contrib.auth.models import User
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


class QuizAttempt(models.Model):
    """Store quiz attempt results for authenticated users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.IntegerField(help_text="Number of correct answers")
    total_questions = models.IntegerField(help_text="Total number of questions")
    time_taken = models.IntegerField(help_text="Time taken in seconds", null=True, blank=True)
    answers = models.JSONField(default=dict, help_text="User's answers as JSON")
    completed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.get_percentage()}%"
    
    def get_percentage(self):
        """Return score as percentage"""
        if self.total_questions > 0:
            return round((self.score / self.total_questions) * 100)
        return 0

