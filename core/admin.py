from django.contrib import admin
from .models import Article, Progress


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'quiz_id', 'status', 'score', 'updated_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'article__title')
