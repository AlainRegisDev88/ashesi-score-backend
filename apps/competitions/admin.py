from django.contrib import admin
from .models import Competition, CompetitionTeam, RankingRule


class CompetitionTeamInline(admin.TabularInline):
    model = CompetitionTeam
    extra = 1
    autocomplete_fields = ["team"]


class RankingRuleInline(admin.TabularInline):
    model = RankingRule
    extra = 1


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ("name", "sport", "competition_type", "status", "start_date", "end_date")
    search_fields = ("name",)
    list_filter = ("sport", "competition_type", "status")
    inlines = [CompetitionTeamInline, RankingRuleInline]


@admin.register(RankingRule)
class RankingRuleAdmin(admin.ModelAdmin):
    list_display = ("criterion", "priority", "sport", "competition")
    list_filter = ("criterion", "sport", "competition")