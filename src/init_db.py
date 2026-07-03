"""
Database initialization script - populates initial activities and test data
Run this script once to set up the database:
    python init_db.py
"""

from database import init_db, SessionLocal, engine, Base
from models import Activity, User
import sys


def initialize_database():
    """Create tables and populate with initial data"""
    
    # Create tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created successfully")

    # Get a session
    db = SessionLocal()

    try:
        # Check if data already exists
        existing_count = db.query(Activity).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} activities. Skipping data population.")
            return

        print("Populating initial activities...")
        
        # Initial activities data (from the original in-memory database)
        activities_data = [
            {
                "name": "Chess Club",
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
            },
            {
                "name": "Programming Class",
                "description": "Learn programming fundamentals and build software projects",
                "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                "max_participants": 20,
                "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
            },
            {
                "name": "Gym Class",
                "description": "Physical education and sports activities",
                "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
                "max_participants": 30,
                "participants": ["john@mergington.edu", "olivia@mergington.edu"]
            },
            {
                "name": "Soccer Team",
                "description": "Join the school soccer team and compete in matches",
                "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
                "max_participants": 22,
                "participants": ["liam@mergington.edu", "noah@mergington.edu"]
            },
            {
                "name": "Basketball Team",
                "description": "Practice and play basketball with the school team",
                "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 15,
                "participants": ["ava@mergington.edu", "mia@mergington.edu"]
            },
            {
                "name": "Art Club",
                "description": "Explore your creativity through painting and drawing",
                "schedule": "Thursdays, 3:30 PM - 5:00 PM",
                "max_participants": 15,
                "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
            },
            {
                "name": "Drama Club",
                "description": "Act, direct, and produce plays and performances",
                "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
                "max_participants": 20,
                "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
            },
            {
                "name": "Math Club",
                "description": "Solve challenging problems and participate in math competitions",
                "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
                "max_participants": 10,
                "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
            },
            {
                "name": "Debate Team",
                "description": "Develop public speaking and argumentation skills",
                "schedule": "Fridays, 4:00 PM - 5:30 PM",
                "max_participants": 12,
                "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
            },
        ]

        # Create users and activities
        all_users = {}
        
        for activity_data in activities_data:
            # Create or get users for this activity
            participant_emails = activity_data.pop("participants", [])
            
            # Create activity
            activity = Activity(**activity_data)
            db.add(activity)
            db.flush()  # Flush to get the ID
            
            # Create/get users and add to activity
            for email in participant_emails:
                if email not in all_users:
                    user = User(email=email, is_teacher=0)
                    db.add(user)
                    db.flush()
                    all_users[email] = user
                
                activity.participants.append(all_users[email])

        # Commit all changes
        db.commit()
        print(f"✓ Successfully created {len(activities_data)} activities")
        print(f"✓ Successfully created {len(all_users)} student users")

    except Exception as e:
        db.rollback()
        print(f"✗ Error initializing database: {e}", file=sys.stderr)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 50)
    print("Mergington High School - Database Initialization")
    print("=" * 50)
    initialize_database()
    print("\n✅ Database initialization complete!")
    print("You can now run the application with: python app.py")
