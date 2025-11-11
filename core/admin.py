from django.contrib import admin
from .models import Article, Progress, ActivityLog
from .models import StudentProfile, EducationalSection, MediaAsset, ContentModeration, Visit, Download, SectionImage


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'quiz_id', 'status', 'score', 'updated_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'article__title')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'grade', 'must_change_password', 'created_at')
    readonly_fields = ('profile_picture_preview',)

    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return f"<img src='{obj.profile_picture.url}' style='max-height:60px;'/>'"
        return '(no image)'
    profile_picture_preview.allow_tags = True
    profile_picture_preview.short_description = 'Profile picture'
    search_fields = ('user__username', 'full_name')


class SectionImageInline(admin.TabularInline):
    model = SectionImage
    extra = 1
    fields = ('image', 'caption', 'order')
    ordering = ('order', 'created_at')


@admin.register(EducationalSection)
class EducationalSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'order', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
    inlines = [SectionImageInline]


@admin.register(SectionImage)
class SectionImageAdmin(admin.ModelAdmin):
    list_display = ('section', 'order', 'caption', 'created_at')
    list_filter = ('section',)
    search_fields = ('section__title', 'caption')
    ordering = ('section', 'order', 'created_at')


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ('title', 'asset_type', 'article', 'uploaded_by', 'created_at')
    list_filter = ('asset_type',)
    search_fields = ('title', 'article__title')


@admin.register(ContentModeration)
class ContentModerationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status', 'moderator', 'created_at')
    list_filter = ('status',)
    search_fields = ('article__title', 'media__title')


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('path', 'user', 'ip_address', 'created_at')
    search_fields = ('path', 'user__username')
    list_filter = ('created_at',)


@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    list_display = ('media', 'user', 'created_at')
    search_fields = ('media__title', 'user__username')


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'action', 'created_at', 'ip_address')
    list_filter = ('category', 'action', 'created_at')
    search_fields = ('user__username', 'description', 'ip_address')
    readonly_fields = ('user', 'category', 'action', 'description', 'article', 'quiz_id', 
                      'game_id', 'media', 'ip_address', 'user_agent', 'metadata', 'created_at')
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        # Prevent manual creation of activity logs
        return False
    
    def has_change_permission(self, request, obj=None):
        # Make logs read-only
        return False

