# Quick Start Guide

## 🚀 Getting Started

Follow these steps to run your Gym Tracker application:

### 1. Activate Virtual Environment

```powershell
.\venv\Scripts\activate
```

### 2. Install Dependencies (if not already installed)

```powershell
pip install -r requirements.txt
```

### 3. Run Migrations (already done, but if needed)

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Optional - for admin access)

```powershell
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 5. Run the Development Server

```powershell
python manage.py runserver
```

### 6. Access the Application

Open your browser to:
- **Main App**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 📱 Using the App

### First Time Setup

1. Go to http://127.0.0.1:8000/
2. Enter your name (e.g., "John")
3. Click "Start Training"

### Create Your First Workout

1. On the dashboard, click "New Workout"
2. Enter a workout name (e.g., "Push Day")
3. Add exercises (e.g., "Bench Press", "Shoulder Press", "Tricep Dips")
4. Use ↑ and ↓ buttons to reorder exercises

### Start a Training Session

1. From the dashboard, click "Start" on a workout
2. For each exercise:
   - Enter weight and reps for each set
   - Check the box when set is complete
   - Use the rest timer between sets
   - Add notes if needed
3. Swipe left/right or use Next/Back buttons to navigate
4. Click "Finish Session" when done

## 🔧 Troubleshooting

### Port Already in Use

If port 8000 is already in use:

```powershell
python manage.py runserver 8080
```

Then access at http://127.0.0.1:8080/

### Database Issues

To reset the database:

```powershell
# Delete the database file
Remove-Item db.sqlite3

# Run migrations again
python manage.py migrate
```

### Static Files Not Loading

```powershell
python manage.py collectstatic
```

## 📊 Admin Panel Features

Access at http://127.0.0.1:8000/admin/

- View all users, workouts, sessions
- Edit data directly
- View session history
- Export data

## 🎯 Tips for Best Experience

1. **Use on Mobile**: The app is optimized for phone use
2. **Landscape Mode**: Better for data entry
3. **Add Exercises Before Gym**: Set up workouts at home
4. **Check Previous Sets**: The app auto-loads your last performance
5. **Use Notes**: Track form, injuries, or adjustments

## 🔄 Progressive Overload

The app automatically:
- Loads your previous session's data
- Allows you to adjust weight/reps
- Saves new data for next time

## 💡 Keyboard Shortcuts (Desktop)

- `Space` - Start/Pause timer
- `R` - Reset timer
- `←` - Previous exercise
- `→` - Next exercise

## 📝 Sample Data

Want to test with sample workouts?

### Push Day
- Bench Press
- Incline Dumbbell Press
- Shoulder Press
- Lateral Raises
- Tricep Pushdowns

### Pull Day
- Pull-ups
- Barbell Rows
- Lat Pulldown
- Face Pulls
- Bicep Curls

### Leg Day
- Squats
- Romanian Deadlifts
- Leg Press
- Leg Curls
- Calf Raises

## 🌐 Accessing from Phone on Same Network

1. Find your computer's IP address:
   ```powershell
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)

2. Update settings.py:
   ```python
   ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.1.100']
   ```

3. Run server on all interfaces:
   ```powershell
   python manage.py runserver 0.0.0.0:8000
   ```

4. Access from phone:
   ```
   http://192.168.1.100:8000/
   ```

## ⚠️ Important Notes

- This is for development use only
- Data is stored locally in SQLite
- No data backup by default - back up `db.sqlite3` manually
- For production deployment, see README.md

## 🎉 Enjoy Your Workouts!

Track your progress and watch your gains! 💪
