from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Max
from django.db import models
import json

from .models import Workout, Exercise, Session, ExerciseSession, Set


def login_view(request):
    """Simple name-based login - no password required"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        if username:
            # Get or create user
            user, created = User.objects.get_or_create(username=username)
            # Log them in
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('dashboard')
    
    return render(request, 'workouts/login.html')


@login_required
def dashboard(request):
    """Main dashboard showing user's workouts"""
    workouts = Workout.objects.filter(user=request.user)
    active_session = Session.objects.filter(user=request.user, end_time__isnull=True).first()
    
    context = {
        'workouts': workouts,
        'active_session': active_session,
    }
    return render(request, 'workouts/dashboard.html', context)


@login_required
def workout_list(request):
    """List all workouts for the user"""
    workouts = Workout.objects.filter(user=request.user)
    return render(request, 'workouts/workout_list.html', {'workouts': workouts})


@login_required
def workout_create(request):
    """Create a new workout"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            workout = Workout.objects.create(name=name, user=request.user)
            return redirect('workout_edit', workout_id=workout.id)
    
    return render(request, 'workouts/workout_create.html')


@login_required
def workout_edit(request, workout_id):
    """Edit workout and manage exercises"""
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_exercise':
            name = request.POST.get('exercise_name', '').strip()
            if name:
                max_order = workout.exercises.aggregate(Max('order'))['order__max'] or 0
                new_exercise = Exercise.objects.create(
                    name=name,
                    workout=workout,
                    order=max_order + 1
                )
                
                # If there's an active session for this workout, add the exercise to it
                active_session = Session.objects.filter(
                    user=request.user,
                    workout=workout,
                    end_time__isnull=True
                ).first()
                
                if active_session:
                    ExerciseSession.objects.create(
                        exercise=new_exercise,
                        session=active_session
                    )
        
        elif action == 'delete_exercise':
            exercise_id = request.POST.get('exercise_id')
            Exercise.objects.filter(id=exercise_id, workout=workout).delete()
        
        elif action == 'reorder':
            exercise_id = request.POST.get('exercise_id')
            direction = request.POST.get('direction')
            exercise = get_object_or_404(Exercise, id=exercise_id, workout=workout)
            
            if direction == 'up' and exercise.order > 0:
                # Swap with previous
                prev_exercise = workout.exercises.filter(order__lt=exercise.order).order_by('-order').first()
                if prev_exercise:
                    exercise.order, prev_exercise.order = prev_exercise.order, exercise.order
                    exercise.save()
                    prev_exercise.save()
            
            elif direction == 'down':
                # Swap with next
                next_exercise = workout.exercises.filter(order__gt=exercise.order).order_by('order').first()
                if next_exercise:
                    exercise.order, next_exercise.order = next_exercise.order, exercise.order
                    exercise.save()
                    next_exercise.save()
        
        return redirect('workout_edit', workout_id=workout.id)
    
    exercises = workout.exercises.all()
    return render(request, 'workouts/workout_edit.html', {
        'workout': workout,
        'exercises': exercises,
    })


@login_required
def session_start(request, workout_id):
    """Start a new workout session"""
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    
    # Check if there's already an active session
    active_session = Session.objects.filter(user=request.user, end_time__isnull=True).first()
    if active_session:
        return redirect('exercise_session', session_id=active_session.id, order=1)
    
    # Create new session
    session = Session.objects.create(
        workout=workout,
        user=request.user
    )
    
    # Create ExerciseSession for each exercise in the workout
    for exercise in workout.exercises.all():
        ExerciseSession.objects.create(
            exercise=exercise,
            session=session
        )
    
    # Redirect to first exercise
    return redirect('exercise_session', session_id=session.id, order=1)


@login_required
def exercise_session(request, session_id, order):
    """Main exercise logging screen"""
    session = get_object_or_404(Session, id=session_id, user=request.user)
    
    # Get all exercise sessions for this workout session
    exercise_sessions = list(session.exercise_sessions.all())
    
    if not exercise_sessions:
        return redirect('session_finish', session_id=session.id)
    
    # Get the exercise at the specified order (1-indexed)
    if order < 1 or order > len(exercise_sessions):
        order = 1
    
    current_exercise_session = exercise_sessions[order - 1]
    
    # Get or create sets for this exercise session
    existing_sets = current_exercise_session.sets.all()
    
    # If no sets exist, create 4 empty sets with data from previous session
    if not existing_sets:
        previous_sets = current_exercise_session.get_previous_sets()
        if previous_sets:
            for i, prev_set in enumerate(previous_sets[:4], 1):
                Set.objects.create(
                    exercise_session=current_exercise_session,
                    set_number=i,
                    weight=prev_set.weight,
                    reps=prev_set.reps,
                    completed=False
                )
        else:
            for i in range(1, 5):
                Set.objects.create(
                    exercise_session=current_exercise_session,
                    set_number=i,
                    weight=0,
                    reps=0,
                    completed=False
                )
        existing_sets = current_exercise_session.sets.all()
    
    context = {
        'session': session,
        'current_exercise_session': current_exercise_session,
        'sets': existing_sets,
        'current_order': order,
        'total_exercises': len(exercise_sessions),
        'has_previous': order > 1,
        'has_next': order < len(exercise_sessions),
    }
    
    return render(request, 'workouts/exercise_session.html', context)


@login_required
@require_http_methods(["POST"])
def update_set(request):
    """AJAX endpoint to update a set"""
    try:
        data = json.loads(request.body)
        set_id = data.get('set_id')
        weight = float(data.get('weight', 0))
        reps = int(data.get('reps', 0))
        completed = data.get('completed', False)
        
        set_obj = get_object_or_404(Set, id=set_id, exercise_session__session__user=request.user)
        set_obj.weight = weight
        set_obj.reps = reps
        set_obj.completed = completed
        set_obj.save()
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
@require_http_methods(["POST"])
def update_notes(request):
    """AJAX endpoint to update exercise notes"""
    try:
        data = json.loads(request.body)
        exercise_session_id = data.get('exercise_session_id')
        notes = data.get('notes', '')
        
        exercise_session = get_object_or_404(
            ExerciseSession,
            id=exercise_session_id,
            session__user=request.user
        )
        exercise_session.notes = notes
        exercise_session.save()
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
@require_http_methods(["POST"])
def add_set(request):
    """AJAX endpoint to add a new set"""
    try:
        data = json.loads(request.body)
        exercise_session_id = data.get('exercise_session_id')
        
        exercise_session = get_object_or_404(
            ExerciseSession,
            id=exercise_session_id,
            session__user=request.user
        )
        
        # Get the next set number
        max_set = exercise_session.sets.aggregate(Max('set_number'))['set_number__max'] or 0
        new_set = Set.objects.create(
            exercise_session=exercise_session,
            set_number=max_set + 1,
            weight=0,
            reps=0,
            completed=False
        )
        
        return JsonResponse({
            'status': 'success',
            'set_id': new_set.id,
            'set_number': new_set.set_number
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
def session_finish(request, session_id):
    """Finish the workout session"""
    session = get_object_or_404(Session, id=session_id, user=request.user)
    
    if request.method == 'POST':
        session.end_time = timezone.now()
        session.save()
        return redirect('dashboard')
    
    return render(request, 'workouts/session_finish.html', {'session': session})


@login_required
def session_cancel(request, session_id):
    """Cancel an active workout session"""
    session = get_object_or_404(Session, id=session_id, user=request.user, end_time__isnull=True)
    
    if request.method == 'POST':
        # Delete the session and all related data
        session.delete()
        return redirect('dashboard')
    
    return render(request, 'workouts/session_cancel.html', {'session': session})


@login_required
def history(request):
    """Show workout history with calendar view"""
    from datetime import date, timedelta
    from calendar import monthrange
    
    # Get current month or requested month
    year = int(request.GET.get('year', date.today().year))
    month = int(request.GET.get('month', date.today().month))
    
    # Get all sessions for this month
    sessions = Session.objects.filter(
        user=request.user,
        date__year=year,
        date__month=month,
        end_time__isnull=False
    ).order_by('-date')
    
    # Create calendar data
    first_day = date(year, month, 1)
    last_day = date(year, month, monthrange(year, month)[1])
    
    # Get dates with sessions
    session_dates = set(sessions.values_list('date', flat=True))
    
    # Calculate calendar grid
    start_weekday = first_day.weekday()
    days_in_month = monthrange(year, month)[1]
    
    # Previous month days
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year
    prev_month_days = monthrange(prev_year, prev_month)[1]
    
    calendar_days = []
    
    # Add previous month days
    for i in range(start_weekday):
        day_num = prev_month_days - start_weekday + i + 1
        calendar_days.append({
            'day': day_num,
            'date': date(prev_year, prev_month, day_num),
            'other_month': True,
            'has_session': False
        })
    
    # Add current month days
    for day in range(1, days_in_month + 1):
        day_date = date(year, month, day)
        calendar_days.append({
            'day': day,
            'date': day_date,
            'other_month': False,
            'has_session': day_date in session_dates,
            'is_today': day_date == date.today()
        })
    
    # Add next month days to complete the grid
    remaining_days = 42 - len(calendar_days)  # 6 weeks * 7 days
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    
    for day in range(1, remaining_days + 1):
        calendar_days.append({
            'day': day,
            'date': date(next_year, next_month, day),
            'other_month': True,
            'has_session': False
        })
    
    # Navigation dates
    prev_month_date = first_day - timedelta(days=1)
    next_month_date = last_day + timedelta(days=1)
    
    context = {
        'year': year,
        'month': month,
        'month_name': first_day.strftime('%B %Y'),
        'calendar_days': calendar_days,
        'prev_month': prev_month_date.month,
        'prev_year': prev_month_date.year,
        'next_month': next_month_date.month,
        'next_year': next_month_date.year,
        'sessions_this_month': sessions.count(),
    }
    
    return render(request, 'workouts/history.html', context)


@login_required
def history_day(request, year, month, day):
    """Show workout details for a specific day"""
    from datetime import date
    
    target_date = date(year, month, day)
    sessions = Session.objects.filter(
        user=request.user,
        date=target_date,
        end_time__isnull=False
    ).prefetch_related('exercise_sessions__exercise', 'exercise_sessions__sets')
    
    context = {
        'date': target_date,
        'sessions': sessions,
    }
    
    return render(request, 'workouts/history_day.html', context)


@login_required
def charts(request):
    """Show exercise progress charts"""
    # Get all exercises the user has done
    exercises = Exercise.objects.filter(
        workout__user=request.user,
        exercise_sessions__session__end_time__isnull=False
    ).distinct().order_by('name')
    
    selected_exercise_id = request.GET.get('exercise')
    chart_data = None
    
    if selected_exercise_id:
        exercise = get_object_or_404(Exercise, id=selected_exercise_id, workout__user=request.user)
        
        # Get all completed sessions for this exercise
        exercise_sessions = ExerciseSession.objects.filter(
            exercise=exercise,
            session__end_time__isnull=False,
            session__user=request.user
        ).order_by('session__date').prefetch_related('sets')
        
        # Prepare chart data
        chart_data = {
            'labels': [],
            'max_weight': [],
            'avg_weight': [],
            'total_reps': [],
            'total_volume': [],
        }
        
        for ex_session in exercise_sessions:
            sets = ex_session.sets.filter(completed=True)
            if sets.exists():
                chart_data['labels'].append(ex_session.session.date.strftime('%Y-%m-%d'))
                chart_data['max_weight'].append(float(sets.order_by('-weight').first().weight))
                chart_data['avg_weight'].append(float(sets.aggregate(avg=models.Avg('weight'))['avg'] or 0))
                chart_data['total_reps'].append(sets.aggregate(total=models.Sum('reps'))['total'] or 0)
                
                # Volume = sum of (weight * reps) for all sets
                volume = sum(s.weight * s.reps for s in sets)
                chart_data['total_volume'].append(float(volume))
    
    context = {
        'exercises': exercises,
        'selected_exercise_id': selected_exercise_id,
        'chart_data': chart_data,
    }
    
    return render(request, 'workouts/charts.html', context)
