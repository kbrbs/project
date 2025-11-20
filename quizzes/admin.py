from django.contrib import admin
from .models import Quiz, Question, QuizAttempt


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'article')
    inlines = [QuestionInline]


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'total_questions', 'get_percentage', 'created_at')
    list_filter = ('quiz', 'created_at', 'completed')
    search_fields = ('user__username', 'quiz__title')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    def get_percentage(self, obj):
        return f"{obj.get_percentage()}%"
    get_percentage.short_description = 'Score %'
