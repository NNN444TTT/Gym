from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Workout(models.Model):
    """Represents a workout split (e.g., Push, Pull, Legs)"""
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"


class Exercise(models.Model):
    """An exercise within a workout"""
    name = models.CharField(max_length=200)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.name} ({self.workout.name})"
    
    def get_last_session_for_user(self, user):
        """Get the most recent ExerciseSession for this exercise and user"""
        return ExerciseSession.objects.filter(
            exercise=self,
            session__user=user,
            session__end_time__isnull=False
        ).order_by('-session__date').first()


class Session(models.Model):
    """A workout session occurrence"""
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='sessions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    date = models.DateField(default=timezone.now)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-date', '-start_time']
    
    def __str__(self):
        return f"{self.workout.name} - {self.user.username} - {self.date}"
    
    @property
    def is_active(self):
        return self.end_time is None


class ExerciseSession(models.Model):
    """An exercise within a session"""
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='exercise_sessions')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='exercise_sessions')
    notes = models.TextField(blank=True, default='')
    rest_timer_seconds = models.IntegerField(default=120)
    
    class Meta:
        ordering = ['exercise__order', 'id']
    
    def __str__(self):
        return f"{self.exercise.name} in {self.session}"
    
    def get_previous_sets(self):
        """Get sets from the last completed session for this exercise"""
        previous_session = self.exercise.get_last_session_for_user(self.session.user)
        if previous_session:
            return previous_session.sets.all()
        return []


class Set(models.Model):
    """A single set within an exercise session"""
    exercise_session = models.ForeignKey(ExerciseSession, on_delete=models.CASCADE, related_name='sets')
    set_number = models.IntegerField()
    weight = models.FloatField(default=0)
    reps = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['set_number']
    
    def __str__(self):
        return f"Set {self.set_number}: {self.weight}kg x {self.reps} reps"
