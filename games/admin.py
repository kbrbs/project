from django.contrib import admin
from .models import Game, GameQuestion, GameOption, GameAttempt


class GameOptionInline(admin.TabularInline):
    model = GameOption
    extra = 1
    fields = ['option_text', 'option_image', 'is_correct', 'order']


class GameQuestionInline(admin.StackedInline):
    model = GameQuestion
    extra = 1
    fields = ['order', 'question_text', 'word', 'correct_sequence', 'correct_answer', 'memory_pairs', 'explanation']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['title', 'game_type', 'difficulty', 'is_active', 'created_at']
    list_filter = ['game_type', 'difficulty', 'is_active']
    search_fields = ['title', 'description']
    inlines = [GameQuestionInline]


@admin.register(GameQuestion)
class GameQuestionAdmin(admin.ModelAdmin):
    list_display = ['game', 'order', 'question_text']
    list_filter = ['game__game_type']
    inlines = [GameOptionInline]


@admin.register(GameAttempt)
class GameAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'game', 'score', 'max_score', 'get_percentage', 'completed', 'created_at']
    list_filter = ['completed', 'game__game_type', 'created_at']
    search_fields = ['user__username', 'game__title']
    readonly_fields = ['created_at']
