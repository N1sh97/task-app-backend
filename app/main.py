from app import schemas
from fastapi import FastAPI,  Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from . import models

from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)
# creates the tables from models.py and call the database engine from database.py

# Creating a database session function


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a task


@app.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=schemas.TaskResponse)
# Registers a POST endpoint with FastAPI.
#
# POST endpoints are typically used to create new data.
#
# Example request:
#
# POST /tasks
#
# Request Body:
#
# {
#   "title": "Learn FastAPI"
#
# }
#
# status_code=status.HTTP_201_CREATED
# tells FastAPI to return a 201 status code when
# the task is successfully created.
#
# 201 = Resource Created
def create_task(task: schemas.CreateTask, db: Session = Depends(get_db)):
    # task:
    # - Contains the JSON data sent by the frontend.
    # - FastAPI automatically validates the request body
    #   using the CreateTask schema.
    #
    # Example:
    #
    # {
    #   "title": "Learn FastAPI"
    # }
    #
    # FastAPI converts that JSON into:
    #
    # task.title
    #
    # db:
    # - Database session provided by FastAPI.
    # - Used to interact with the database.

    new_task = models.Task(
        title=task.title,
        task_status=task.task_status,
    )

    # Create a new Task object in Python.
    #
    # models.Task represents a row in the tasks table.
    #
    # At this point:
    # - Nothing has been saved to the database yet.
    # - We have only created a Python object.
    #
    # Example:
    #
    # new_task = {
    #     title: "Learn FastAPI",
    #     completed: False
    # }

    db.add(new_task)
# Add the new task to SQLAlchemy's session.
#
# Think of this as:
# "I want to save this object to the database."
#
# The task is staged and waiting to be committed.
#
# Nothing has been written to the database yet.

    db.commit()
# Permanently save the changes to the database.
#
# This is the step that actually executes the SQL.
#
# SQL equivalent:
#
# INSERT INTO tasks (
#     title,
#     completed
# )
# VALUES (
#     'Learn FastAPI',
#     'Study POST endpoints',
#     false
# );

    db.refresh(new_task)
# Reload the object from the database.
#
# Why?
#
# The database may have generated values
# that didn't exist before.
#
# Example:
#
# id = 1
# created_at = current timestamp
#
# refresh() updates the Python object with
# the latest values from the database.

    return new_task
# Return the newly created task.
#
# FastAPI automatically converts it into JSON.
#
# Example response:
#
# {
#   "id": 1,
#   "title": "Learn FastAPI",
#   "completed": false
# }

# Get all tasks


@app.get("/tasks")
# Creates a GET endpoint at /tasks
#
# We need a database session ('db') so this endpoint can communicate
# with the database and retrieve data.
#
# FastAPI uses Depends(get_db) to:
# 1. Create a database session before the request starts
# 2. Pass that session into this function as 'db'
# 3. Automatically close the session when the request finishes
#
# Without 'db', we would not be able to query the Task table.
def get_tasks(db: Session = Depends(get_db)):

    # Query the Task table and retrieve all records
    # SQL equivalent: SELECT * FROM tasks;
    tasks = db.query(models.Task).all()

    # Return the results as a JSON response
    return tasks


# Get a single tasks

@app.get("/tasks/{task_id}")
# Registers a GET endpoint with FastAPI.
# When a request is made to /tasks/{task_id}, FastAPI will execute
# the get_single_task() function below.
#
# Example:
# GET /tasks/1
# GET /tasks/25
#
# {task_id} is a path parameter whose value is extracted from the URL.
def get_single_task(task_id: int, db: Session = Depends(get_db)):
    # task_id:
    # - Automatically extracted from the URL.
    # - FastAPI validates it as an integer because of ': int'.
    #
    # Example:
    # GET /tasks/5
    # task_id = 5
    #
    # db:
    # - A SQLAlchemy database session.
    # - FastAPI creates it by calling get_db().
    # - Used to communicate with the database.
    #
    # Think of db as your active connection to the database.

    task = db.query(models.Task).filter(models.Task.id == task_id). first()
 # db.query(models.Task)
    # - Query the Task table.
    # - Equivalent to:
    #   SELECT * FROM tasks
    #
    # .filter(models.Task.id == task_id)
    # - Add a WHERE condition.
    # - Equivalent to:
    #   WHERE id = task_id
    #
    # .first()
    # - Return the first matching row.
    # - Equivalent to:
    #   LIMIT 1
    #

    if task is None:
        # Check whether the database found a matching task.
        #
        # Example:
        # GET /tasks/999
        #
        # If task 999 doesn't exist:
        # task = None
        #
        # In this case we return a 404 error to the frontend.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
        # HTTPException immediately stops the function.
        #
        # status_code=404
        # Means "Resource Not Found".
        #
        # Frontend receives:
        #
        # {
        #   "detail": "Task not found"
        # }

    return task

  # Return the Task object.
    #
    # FastAPI automatically converts the SQLAlchemy object
    # into JSON before sending it back to the client.
    #
    # Example response:
    #
    # {
    #   "id": 1,
    #   "title": "Learn FastAPI"
    # }
    #
    # The frontend can then display this data in the UI.


@app.put("/tasks/{task_id}")
# Registers a PUT endpoint with FastAPI.
# PUT is typically used when we want to update an existing resource.
#
# Example requests:
# PUT /tasks/1
# PUT /tasks/25
#
# {task_id} is a path parameter and FastAPI automatically
# extracts its value from the URL.
def update_task(
    task_id: int,
    updated_task: schemas.UpdateTask,
    db: Session = Depends(get_db)
    # task_id:
    # Value taken from the URL path.
    # FastAPI validates that it is an integer.
    #
    # updated_task:
    # Request body containing the new task data.
    # This must match the UpdateTask Pydantic schema.
    #
    # db:
    # Database session injected by FastAPI using Depends(get_db).
    # Allows us to query and update data in the database.
):
    task = db.query(models.Task).filter(models.Task.id == task_id). first()

    # db.query(models.Task)
    # Tells SQLAlchemy to query the Task table.
    #
    # .filter(models.Task.id == task_id)
    # Adds a WHERE clause so we only look for the task
    # whose id matches the value passed in the URL.
    #
    # .first()
    # Returns the first matching row or None if no task exists.
    #
    # SQL equivalent:
    # SELECT * FROM tasks WHERE id = task_id LIMIT 1;

    if task is None:
        # If no task was found with the provided ID,
        # return a 404 Not Found response.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update the existing task object with the new values
    # provided in the request body.

    for field, value in updated_task.dict(exclude_unset=True).items():
        setattr(task, field, value)

    # Commit saves the changes permanently to the database.
    db.commit()

    # Refresh reloads the task from the database so we have
    # the latest version of the record.
    db.refresh(task)

    # Return the updated task as the response.
    return task


@app.delete("/tasks/{task_id}")
# Registers a DELETE endpoint with FastAPI.
# DELETE is typically used when we want to remove an existing resource.
#
# Example requests:
# DELETE /tasks/1
# DELETE /tasks/25
#
# {task_id} is a path parameter and FastAPI automatically
# extracts its value from the URL.
def delete_task(
        task_id: int, db: Session = Depends(get_db)):

    # task_id:
    # Value taken from the URL path.
    # FastAPI validates that it is an integer.
    #
    # db:
    # Database session injected by FastAPI using Depends(get_db).
    # Allows us to query and modify data in the database.

    task = db.query(models.Task).filter(models.Task.id == task_id). first()

    # db.query(models.Task)
    # Tells SQLAlchemy to query the Task table.
    #
    # .filter(models.Task.id == task_id)
    # Adds a WHERE clause so we only look for the task
    # whose id matches the value passed in the URL.
    #
    # .first()
    # Returns the first matching row or None if no task exists.
    #
    # SQL equivalent:
    # SELECT * FROM tasks WHERE id = task_id LIMIT 1;

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(task)
    # Mark the task object for deletion.
    # At this point the record is not yet removed
    # from the database.

    db.commit()

    # Return a confirmation message along with
    # the details of the task that was deleted.
    # This can be useful for debugging or confirming
    # which record was removed.

    return task
