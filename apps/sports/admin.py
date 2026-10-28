from django.contrib import admin
from .models import Sport, Position, EventType


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "clock_direction", "starters_count", "is_active")
    search_fields = ("name", "slug")
    list_filter = ("clock_direction", "is_active", "coverage_tier")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "sport")
    search_fields = ("name", "code")
    list_filter = ("sport",)


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "sport", "points", "credits_opponent", "is_shootout", "is_active")
    search_fields = ("name", "code")
    list_filter = ("sport", "credits_opponent", "is_shootout", "is_active")