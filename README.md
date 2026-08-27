# Task App Backend

A FastAPI backend for the Task App.

## Getting Started

### 1. Clone the Repository

Clone the repository from GitHub:

```bash
git clone https://github.com/N1sh97/task-app-backend.git
```

Navigate into the project:

```bash
cd task-app-backend
```

### 2. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

The project uses:

* FastAPI
* Uvicorn
* SQLAlchemy
* Pydantic

### 3. Run Locally

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

**http://localhost:8000**

FastAPI's interactive API documentation is available at:

**http://localhost:8000/docs**

---

# Deploying to Render

The backend can be deployed to Render as a Web Service.

### 1. Connect GitHub

1. Sign in to Render.
2. Select **New → Web Service**.
3. Connect your GitHub account.
4. Select the `task-app-backend` repository.

### 2. Configure the Web Service

Use the following settings:

| Setting        | Value                                              |
| -------------- | -------------------------------------------------- |
| Runtime        | Python                                             |
| Root Directory | Leave blank                                        |
| Build Command  | `pip install -r requirements.txt`                  |
| Start Command  | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

### 3. Deploy

Select the **Free** plan if available and click **Create Web Service**.

Render will:

1. Clone the GitHub repository.
2. Install the dependencies from `requirements.txt`.
3. Start the FastAPI application.
4. Provide a public URL for the API.

Your deployed API will have a URL similar to:

```text
https://your-app-name.onrender.com
```

### 4. Verify the Deployment

Once deployment is complete, open:

```text
https://your-app-name.onrender.com/docs
```

This should display the FastAPI Swagger documentation and your available API endpoints.

## Project Structure

```text
task-app-backend/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── .gitignore
└── requirements.txt
```

## Technologies

* Python
* FastAPI
* Uvicorn
* SQLAlchemy
* Pydantic
* Render
* GitHub
