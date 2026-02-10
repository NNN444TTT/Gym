from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('workouts/', views.workout_list, name='workout_list'),
    path('workouts/create/', views.workout_create, name='workout_create'),
    path('workouts/edit/<int:workout_id>/', views.workout_edit, name='workout_edit'),
    path('session/start/<int:workout_id>/', views.session_start, name='session_start'),
    path('session/<int:session_id>/exercise/<int:order>/', views.exercise_session, name='exercise_session'),
    path('session/<int:session_id>/finish/', views.session_finish, name='session_finish'),
    path('session/<int:session_id>/cancel/', views.session_cancel, name='session_cancel'),
    
    # History and Charts
    path('history/', views.history, name='history'),
    path('history/<int:year>/<int:month>/<int:day>/', views.history_day, name='history_day'),
    path('charts/', views.charts, name='charts'),
    
    # AJAX endpoints
    path('api/set/update/', views.update_set, name='update_set'),
    path('api/notes/update/', views.update_notes, name='update_notes'),
    path('api/set/add/', views.add_set, name='add_set'),
]
