from django.contrib import admin
from .models import (
    Venue,
    Match,
    MatchClock,
    MatchReporter,
    LineupEntry,
    MatchEvent,
)

class MatchReporterInline(admin.TabularInline):
    model = MatchReporter
    extra = 1

class MatchClockInline(admin.StackedInline):
    model = MatchClock
    can_delete = False

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("name", "capacity")
    search_fields = ("name",)

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "home_team",
        "away_team",
        "sport",
        "competition",
        "stage",
        "status",
        "scheduled_at",
        "home_score",
        "away_score",
    )
    list_filter = ("status", "sport", "competition", "stage__stage_type")
    search_fields = ("home_team__name", "away_team__name", "venue__name")
    inlines = [MatchClockInline, MatchReporterInline]

@admin.register(LineupEntry)
class LineupEntryAdmin(admin.ModelAdmin):
    list_display = ("match", "team", "player", "position", "jersey_number", "is_starter")
    list_filter = ("is_starter", "team")
    search_fields = ("player__first_name", "player__last_name", "team__name")

@admin.register(MatchEvent)
class MatchEventAdmin(admin.ModelAdmin):
    list_display = ("match", "event_type", "team", "player", "clock_seconds", "is_voided")
    list_filter = ("is_voided", "event_type", "team")
    search_fields = ("player__first_name", "player__last_name", "match__home_team__name")