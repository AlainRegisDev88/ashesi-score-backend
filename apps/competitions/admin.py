from django.contrib import admin
from .models import (
    Competition,
    CompetitionTeam,
    RankingRule,
    CompetitionStage,
    StageGroup,
    StageGroupTeam,
    KnockoutTie,
)

class CompetitionTeamInline(admin.TabularInline):
    model = CompetitionTeam
    extra = 1

class RankingRuleInline(admin.TabularInline):
    model = RankingRule
    extra = 1

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ("name", "sport", "competition_type", "status", "start_date", "end_date")
    list_filter = ("sport", "competition_type", "status")
    search_fields = ("name",)
    inlines = [CompetitionTeamInline, RankingRuleInline]

@admin.register(CompetitionStage)
class CompetitionStageAdmin(admin.ModelAdmin):
    list_display = ("name", "competition", "stage_type", "sequence", "two_legged")
    list_filter = ("stage_type", "competition")
    search_fields = ("name",)

@admin.register(StageGroup)
class StageGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "stage")
    list_filter = ("stage__competition",)
    search_fields = ("name",)

@admin.register(StageGroupTeam)
class StageGroupTeamAdmin(admin.ModelAdmin):
    list_display = ("group", "team")
    list_filter = ("group__stage__competition",)

@admin.register(KnockoutTie)
class KnockoutTieAdmin(admin.ModelAdmin):
    list_display = ("stage", "slot", "home_team", "away_team", "winner_team")
    list_filter = ("stage__competition",)