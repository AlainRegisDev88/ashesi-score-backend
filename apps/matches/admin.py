from django.contrib import admin
from .models import Venue, Match, MatchClock, MatchReporter, LineupEntry, MatchEvent


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "capacity", "is_active")
    search_fields = ("name", "slug")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}


class MatchReporterInline(admin.TabularInline):
    model = MatchReporter
    extra = 1
    autocomplete_fields = ["user", "assigned_by"]


class MatchClockInline(admin.StackedInline):
    model = MatchClock
    can_delete = False


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("home_team", "away_team", "sport", "competition", "scheduled_at", "status", "home_score", "away_score")
    search_fields = ("home_team__name", "away_team__name", "venue__name")
    list_filter = ("status", "sport", "competition")
    inlines = [MatchClockInline, MatchReporterInline]


@admin.register(LineupEntry)
class LineupEntryAdmin(admin.ModelAdmin):
    list_display = ("match", "team", "player", "position", "is_starter")
    search_fields = ("player__first_name", "player__last_name", "team__name")
    list_filter = ("is_starter", "team")


@admin.register(MatchEvent)
class MatchEventAdmin(admin.ModelAdmin):
    list_display = ("match", "event_type", "team", "player", "period", "clock_seconds", "is_voided")
    search_fields = ("match__home_team__name", "match__away_team__name", "player__first_name", "player__last_name")
    list_filter = ("is_voided", "event_type", "team")