from django.contrib import admin
from .models import NewsArticle, Award


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "sport", "status", "published_at")
    search_fields = ("title", "slug")
    list_filter = ("status", "sport")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ("title", "award_type", "awarded_by", "created_at")
    search_fields = ("title",)
    list_filter = ("award_type",)