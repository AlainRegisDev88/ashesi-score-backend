from django.contrib import admin
from .models import Team, Manager, Player, SquadMembership


class SquadMembershipInline(admin.TabularInline):
    model = SquadMembership
    extra = 1
    autocomplete_fields = ["team", "sport", "position", "created_by"]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "sport", "slug", "is_active")
    search_fields = ("name", "short_name", "slug")
    list_filter = ("sport", "is_active")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "team", "is_active")
    search_fields = ("first_name", "last_name")
    list_filter = ("is_active",)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "slug", "is_active")
    search_fields = ("first_name", "last_name", "slug")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("first_name", "last_name")}
    inlines = [SquadMembershipInline]


@admin.register(SquadMembership)
class SquadMembershipAdmin(admin.ModelAdmin):
    list_display = ("player", "team", "sport", "start_date", "end_date")
    search_fields = ("player__first_name", "player__last_name", "team__name")
    list_filter = ("sport", "team")