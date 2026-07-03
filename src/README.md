# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Sign up for activities
- **Persistent data storage** using SQLite database

## Getting Started

1. Install the dependencies:

   ```bash
   pip install -r ../requirements.txt
   ```

2. Initialize the database (first time only):

   ```bash
   python init_db.py
   ```
   
   This will create the `activities.db` SQLite database and populate it with initial activity data.

3. Run the application:

   ```bash
   python app.py
   ```

4. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Unregister from an activity                                      |

## Data Model

The application uses SQLite for persistent storage with the following models:

1. **Activities** - Activity information:
   - Name (unique identifier)
   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of participants (many-to-many relationship)

2. **Users** - Student and teacher accounts:
   - Email (unique identifier)
   - Username (for teachers)
   - Password hash (for teacher authentication)
   - Is teacher flag
   - Associated activities (many-to-many relationship)

## Database Persistence

All data is now persisted in `activities.db` SQLite database, which means:
- ✅ Data survives server restarts
- ✅ Activities and enrollments are permanently stored
- ✅ Multiple API calls maintain consistent state

To reset the database, simply delete the `activities.db` file and run `init_db.py` again.

