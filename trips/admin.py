from django.contrib import admin
from .models import City, Activity, Trip, Stop, StopActivity, ChecklistItem, TripNote, UserProfile


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'region', 'cost_index', 'popularity']
    search_fields = ['name', 'country']
    list_filter = ['country', 'region']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'activity_type', 'cost', 'duration_hours']
    list_filter = ['activity_type', 'city']
    search_fields = ['name', 'city__name']


class StopInline(admin.TabularInline):
    model = Stop
    extra = 0


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'start_date', 'end_date', 'is_public']
    list_filter = ['is_public']
    search_fields = ['name', 'user__username']
    inlines = [StopInline]


@admin.register(Stop)
class StopAdmin(admin.ModelAdmin):
    list_display = ['trip', 'city', 'arrival_date', 'departure_date', 'order']


@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'trip', 'category', 'is_packed']
    list_filter = ['category', 'is_packed']


@admin.register(TripNote)
class TripNoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'trip', 'created_at']

admin.site.register(UserProfile)
admin.site.register(StopActivity)
