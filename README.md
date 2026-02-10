# 💪 Gym Tracker - Mobile-First Workout Tracking App

A Django web application for tracking gym workouts, exercises, sets, reps, and progressive overload. Optimized for mobile use during workouts.

## Features

- **Simple Login**: No passwords - just enter your name
- **Workout Management**: Create custom workout splits (Push, Pull, Legs, etc.)
- **Exercise Builder**: Add, reorder, and manage exercises in each workout
- **Session Tracking**: Track sets, reps, and weight for each exercise
- **Progressive Overload**: Automatically loads data from your last session
- **Rest Timer**: Built-in countdown timer with audio/vibration notifications
- **Mobile-First Design**: Large buttons, touch-friendly inputs, swipe gestures
- **Autosave**: Automatic saving of all changes via AJAX
- **Dark Mode**: Eye-friendly dark theme

## Tech Stack

- Django 5.2+
- SQLite (default, PostgreSQL-ready)
- Vanilla JavaScript (no frameworks)
- CSS (mobile-first, no Bootstrap)
- AJAX for real-time updates

## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup Instructions

1. **Clone or navigate to the project directory**

```bash
cd C:\Users\Natal\OneDrive\Projects\Gym
```

2. **Activate virtual environment**

```bash
.\venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create a superuser (optional, for admin access)**

```bash
python manage.py createsuperuser
```

6. **Run the development server**

```bash
python manage.py runserver
```

7. **Access the application**

Open your browser to: `http://127.0.0.1:8000/`

## Project Structure

```
Gym/
├── config/                 # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── workouts/              # Main app
│   ├── migrations/
│   ├── templates/
│   │   └── workouts/
│   │       ├── base.html
│   │       ├── login.html
│   │       ├── dashboard.html
│   │       ├── workout_create.html
│   │       ├── workout_edit.html
│   │       ├── exercise_session.html
│   │       └── session_finish.html
│   ├── admin.py
│   ├── models.py          # Data models
│   ├── views.py           # View logic
│   └── urls.py            # URL routing
├── static/
│   ├── css/
│   │   └── styles.css     # Mobile-first styles
│   └── js/
│       └── app.js         # Interactive features
├── manage.py
└── requirements.txt
```

## Data Models

### Workout
- Represents a workout split (e.g., Push, Pull, Legs)
- Belongs to a User

### Exercise
- Individual exercise within a workout
- Has an order for sequencing

### Session
- A workout occurrence
- Tracks start/end times

### ExerciseSession
- An exercise within a session
- Stores notes and rest timer settings

### Set
- Individual set data (weight, reps, completion status)

## User Flow

1. **Login** → Enter your name (auto-creates user if new)
2. **Dashboard** → View your workouts
3. **Create Workout** → Add a workout split
4. **Edit Workout** → Add/remove/reorder exercises
5. **Start Session** → Begin tracking
6. **Log Sets** → Enter weight/reps, check off completed sets
7. **Navigate** → Swipe or use buttons to move between exercises
8. **Finish** → Complete session and return to dashboard

## Key Features

### Exercise Logging Screen

The most important page, optimized for gym use:

- **Large Exercise Name Header**
- **Rest Timer**: 2-minute countdown with start/pause/reset
- **Sets Table**: Pre-populated with last session's data
- **Touch-Friendly Inputs**: Large, easy-to-tap controls
- **Checkboxes**: Tap to mark sets complete
- **Autosave**: Changes save automatically
- **Notes**: Add exercise-specific notes
- **Progress Bar**: Shows current exercise position
- **Swipe Gestures**: Swipe left/right to navigate

### Keyboard Shortcuts (Desktop)

- `Space` - Start/Pause timer
- `R` - Reset timer
- `←` - Previous exercise
- `→` - Next exercise

## API Endpoints

### AJAX Endpoints (JSON)

- `POST /api/set/update/` - Update a set
- `POST /api/notes/update/` - Update exercise notes
- `POST /api/set/add/` - Add a new set

## Deployment Considerations

The project is structured for easy deployment:

### For Production

1. **Update settings.py**:
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Add a secure `SECRET_KEY`

2. **Use PostgreSQL** (recommended):
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'gymtracker',
           'USER': 'your_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```

4. **Install whitenoise** (for static files):
   ```bash
   pip install whitenoise
   ```
   
   Add to `MIDDLEWARE` in settings.py:
   ```python
   'whitenoise.middleware.WhiteNoiseMiddleware',
   ```

5. **Use gunicorn** (production server):
   ```bash
   pip install gunicorn
   gunicorn config.wsgi:application
   ```

## Future Enhancements

Potential features for future versions:

- [ ] Exercise library with images/videos
- [ ] Workout history and statistics
- [ ] Progressive overload suggestions
- [ ] Exercise templates
- [ ] Export data to CSV
- [ ] Workout calendar view
- [ ] Personal records tracking
- [ ] Rest day reminders
- [ ] Exercise substitution suggestions
- [ ] Workout duration tracking
- [ ] Body weight tracking

## License

This is a personal/family use project. Modify as needed for your own use.

## Support

For issues or questions, refer to the Django documentation:
- https://docs.djangoproject.com/

## Contributing

This is a personal project, but feel free to fork and customize for your own needs!

---

**Built with ❤️ for gains** 💪
