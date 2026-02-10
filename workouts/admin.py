from django.contrib import admin
from .models import Workout, Exercise, Session, ExerciseSession, Set


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['name', 'user__username']


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'workout', 'order']
    list_filter = ['workout__user']
    search_fields = ['name', 'workout__name']
    ordering = ['workout', 'order']


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['workout', 'user', 'date', 'start_time', 'end_time', 'is_active']
    list_filter = ['user', 'date', 'workout']
    search_fields = ['workout__name', 'user__username']
    date_hierarchy = 'date'


@admin.register(ExerciseSession)
class ExerciseSessionAdmin(admin.ModelAdmin):
    list_display = ['exercise', 'session', 'rest_timer_seconds']
    list_filter = ['session__user', 'exercise__workout']
    search_fields = ['exercise__name', 'session__workout__name']


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ['exercise_session', 'set_number', 'weight', 'reps', 'completed']
    list_filter = ['completed', 'exercise_session__session__user']
    search_fields = ['exercise_session__exercise__name']
