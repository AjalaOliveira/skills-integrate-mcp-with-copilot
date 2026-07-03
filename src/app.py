"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.

Database: Uses SQLite for persistent data storage.
Initialize the database by running: python init_db.py
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
from sqlalchemy.orm import Session

from database import init_db, get_db, engine, Base
from models import Activity, User

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# Initialize database on startup
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities(db: Session = Depends(get_db)):
    """Get all activities with their details and current participant count"""
    activities = db.query(Activity).all()
    
    # Convert to dictionary format compatible with frontend
    result = {}
    for activity in activities:
        result[activity.name] = activity.to_dict()
    
    return result


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    """Sign up a student for an activity"""
    # Validate activity exists
    activity = db.query(Activity).filter(Activity.name == activity_name).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Check if student is already signed up
    user = db.query(User).filter(User.email == email).first()
    if user and user in activity.participants:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Create user if doesn't exist
    if not user:
        user = User(email=email, is_teacher=0)
        db.add(user)
        db.flush()

    # Add student to activity
    activity.participants.append(user)
    db.commit()
    
    return {"message": f"Signed up {email} for {activity_name}"}



@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    """Unregister a student from an activity"""
    # Validate activity exists
    activity = db.query(Activity).filter(Activity.name == activity_name).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the user
    user = db.query(User).filter(User.email == email).first()
    if not user or user not in activity.participants:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student from activity
    activity.participants.remove(user)
    db.commit()
    
    return {"message": f"Unregistered {email} from {activity_name}"}

