// ===== UTILITY FUNCTIONS =====

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showSaveIndicator() {
    const indicator = document.getElementById('save-indicator');
    if (indicator) {
        indicator.classList.add('show');
        setTimeout(() => {
            indicator.classList.remove('show');
        }, 1000);
    }
}

// ===== EXERCISE SESSION =====

let timerInterval = null;
let timeRemaining = 120; // Default 2 minutes
let timerRunning = false;

function initExerciseSession() {
    const exerciseSession = document.querySelector('.exercise-session');
    if (!exerciseSession) return;
    
    // Initialize timer
    initTimer();
    
    // Initialize set inputs
    initSetInputs();
    
    // Initialize notes
    initNotes();
    
    // Initialize add set button
    initAddSet();
    
    // Initialize swipe gestures
    initSwipeGestures();
}

// ===== TIMER =====

function initTimer() {
    const timerDisplay = document.getElementById('timer-display');
    const startBtn = document.getElementById('timer-start');
    const pauseBtn = document.getElementById('timer-pause');
    const resetBtn = document.getElementById('timer-reset');
    
    if (!timerDisplay || !startBtn || !pauseBtn || !resetBtn) return;
    
    updateTimerDisplay();
    
    startBtn.addEventListener('click', () => {
        startTimer();
        startBtn.style.display = 'none';
        pauseBtn.style.display = 'inline-block';
    });
    
    pauseBtn.addEventListener('click', () => {
        pauseTimer();
        pauseBtn.style.display = 'none';
        startBtn.style.display = 'inline-block';
    });
    
    resetBtn.addEventListener('click', () => {
        resetTimer();
        pauseBtn.style.display = 'none';
        startBtn.style.display = 'inline-block';
    });
}

function startTimer() {
    if (timerRunning) return;
    
    timerRunning = true;
    timerInterval = setInterval(() => {
        timeRemaining--;
        
        if (timeRemaining <= 0) {
            pauseTimer();
            playNotificationSound();
            timeRemaining = 0;
        }
        
        updateTimerDisplay();
    }, 1000);
}

function pauseTimer() {
    timerRunning = false;
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
}

function resetTimer() {
    pauseTimer();
    timeRemaining = 120;
    updateTimerDisplay();
}

function updateTimerDisplay() {
    const timerDisplay = document.getElementById('timer-display');
    if (!timerDisplay) return;
    
    const minutes = Math.floor(timeRemaining / 60);
    const seconds = timeRemaining % 60;
    
    timerDisplay.textContent = 
        `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    
    // Change color when time is running out
    if (timeRemaining <= 10 && timeRemaining > 0) {
        timerDisplay.style.color = '#ff9800'; // Warning color
    } else if (timeRemaining === 0) {
        timerDisplay.style.color = '#f44336'; // Danger color
    } else {
        timerDisplay.style.color = '#4CAF50'; // Primary color
    }
}

function playNotificationSound() {
    // Try to play a beep sound (browser-dependent)
    // For MVP, we'll use vibration if available
    if ('vibrate' in navigator) {
        navigator.vibrate([200, 100, 200]);
    }
}

// ===== SET INPUTS =====

function initSetInputs() {
    const setRows = document.querySelectorAll('.set-row');
    
    setRows.forEach(row => {
        const setId = row.dataset.setId;
        const weightInput = row.querySelector('.weight-input');
        const repsInput = row.querySelector('.reps-input');
        const checkbox = row.querySelector('.set-checkbox');
        
        // Debounce timer for autosave
        let saveTimeout = null;
        
        const saveSet = () => {
            if (saveTimeout) clearTimeout(saveTimeout);
            
            saveTimeout = setTimeout(() => {
                updateSet(setId, {
                    weight: parseFloat(weightInput.value) || 0,
                    reps: parseInt(repsInput.value) || 0,
                    completed: checkbox.checked
                });
            }, 500);
        };
        
        weightInput.addEventListener('input', saveSet);
        repsInput.addEventListener('input', saveSet);
        checkbox.addEventListener('change', () => {
            // Immediate save for checkbox
            updateSet(setId, {
                weight: parseFloat(weightInput.value) || 0,
                reps: parseInt(repsInput.value) || 0,
                completed: checkbox.checked
            });
            
            // Auto-start timer when set is completed
            if (checkbox.checked && !timerRunning) {
                resetTimer();
                startTimer();
                document.getElementById('timer-start').style.display = 'none';
                document.getElementById('timer-pause').style.display = 'inline-block';
            }
        });
    });
}

function updateSet(setId, data) {
    fetch('/api/set/update/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            set_id: setId,
            weight: data.weight,
            reps: data.reps,
            completed: data.completed
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            showSaveIndicator();
        }
    })
    .catch(error => {
        console.error('Error updating set:', error);
    });
}

// ===== NOTES =====

function initNotes() {
    const notesInput = document.getElementById('notes-input');
    if (!notesInput) return;
    
    const exerciseSession = document.querySelector('.exercise-session');
    const exerciseSessionId = exerciseSession.dataset.exerciseSessionId;
    
    let saveTimeout = null;
    
    notesInput.addEventListener('input', () => {
        if (saveTimeout) clearTimeout(saveTimeout);
        
        saveTimeout = setTimeout(() => {
            updateNotes(exerciseSessionId, notesInput.value);
        }, 1000);
    });
}

function updateNotes(exerciseSessionId, notes) {
    fetch('/api/notes/update/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            exercise_session_id: exerciseSessionId,
            notes: notes
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            showSaveIndicator();
        }
    })
    .catch(error => {
        console.error('Error updating notes:', error);
    });
}

// ===== ADD SET =====

function initAddSet() {
    const addSetBtn = document.getElementById('add-set-btn');
    if (!addSetBtn) return;
    
    const exerciseSession = document.querySelector('.exercise-session');
    const exerciseSessionId = exerciseSession.dataset.exerciseSessionId;
    
    addSetBtn.addEventListener('click', () => {
        fetch('/api/set/add/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                exercise_session_id: exerciseSessionId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Reload the page to show the new set
                location.reload();
            }
        })
        .catch(error => {
            console.error('Error adding set:', error);
        });
    });
}

// ===== SWIPE GESTURES =====

function initSwipeGestures() {
    const exerciseSession = document.querySelector('.exercise-session');
    if (!exerciseSession) return;
    
    const hasPrevious = exerciseSession.dataset.hasPrevious === 'true';
    const hasNext = exerciseSession.dataset.hasNext === 'true';
    const sessionId = exerciseSession.dataset.sessionId;
    const currentOrder = parseInt(exerciseSession.dataset.currentOrder);
    
    let touchStartX = 0;
    let touchEndX = 0;
    const minSwipeDistance = 50;
    
    exerciseSession.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });
    
    exerciseSession.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, { passive: true });
    
    function handleSwipe() {
        const swipeDistance = touchEndX - touchStartX;
        
        // Swipe right (previous exercise)
        if (swipeDistance > minSwipeDistance && hasPrevious) {
            window.location.href = `/session/${sessionId}/exercise/${currentOrder - 1}/`;
        }
        
        // Swipe left (next exercise)
        if (swipeDistance < -minSwipeDistance && hasNext) {
            window.location.href = `/session/${sessionId}/exercise/${currentOrder + 1}/`;
        }
    }
}

// ===== KEYBOARD SHORTCUTS =====

document.addEventListener('keydown', (e) => {
    const exerciseSession = document.querySelector('.exercise-session');
    if (!exerciseSession) return;
    
    // Don't trigger shortcuts if user is typing in an input
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
        return;
    }
    
    // Space bar - start/pause timer
    if (e.code === 'Space') {
        e.preventDefault();
        const startBtn = document.getElementById('timer-start');
        const pauseBtn = document.getElementById('timer-pause');
        
        if (startBtn && startBtn.style.display !== 'none') {
            startBtn.click();
        } else if (pauseBtn && pauseBtn.style.display !== 'none') {
            pauseBtn.click();
        }
    }
    
    // R key - reset timer
    if (e.code === 'KeyR') {
        e.preventDefault();
        const resetBtn = document.getElementById('timer-reset');
        if (resetBtn) resetBtn.click();
    }
    
    // Arrow keys for navigation
    if (e.code === 'ArrowLeft') {
        e.preventDefault();
        const prevBtn = document.getElementById('prev-btn');
        if (prevBtn) prevBtn.click();
    }
    
    if (e.code === 'ArrowRight') {
        e.preventDefault();
        const nextBtn = document.getElementById('next-btn');
        if (nextBtn) nextBtn.click();
    }
});

// ===== PREVENT ACCIDENTAL NAVIGATION =====

window.addEventListener('beforeunload', (e) => {
    const exerciseSession = document.querySelector('.exercise-session');
    if (exerciseSession) {
        // Warn user before leaving if in active session
        e.preventDefault();
        e.returnValue = '';
    }
});

// ===== INITIALIZATION =====

document.addEventListener('DOMContentLoaded', () => {
    initExerciseSession();
});
