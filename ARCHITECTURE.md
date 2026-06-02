# Project Architecture: Developer Portfolio
## Stack: Flask, Jinja2, Tailwind CSS, Docker

### 📂 Directory Tree
```text
portfolio/
├── app/                        # Main application package
│   ├── __init__.py             # Application Factory (Flask instance creation)
│   ├── models.py               # Data models (SQLAlchemy)
│   ├── routes/                 # Modular routing (Blueprints)
│   │   ├── __init__.py
│   │   ├── main.py             # General pages: Home, About, Contacts
│   │   └── portfolio.py         # Project and skill pages
│   ├── static/                 # Static resources
│   │   ├── css/                # Styles (Tailwind CSS)
│   │   │   └── style.css
│   │   ├── js/                 # Client-side JavaScript
│   │   │   └── main.js
│   │   └── img/                # Images, icons, project screenshots
│   └── templates/              # Jinja2 templates
│       ├── base.html            # Base layout (Navbar, Footer)
│       ├── index.html           # Home page
│       ├── project_detail.html   # Detailed project description
│       └── components/         # Reusable components (cards, buttons)
├── config.py                   # Application configuration (Dev, Prod, Test)
├── .env                        # Secrets and environment variables (not in Git)
├── .env.example                # Example of required .env variables
├── .gitignore                  # Git ignored files
├── docker-compose.yml          # Container orchestration (App + DB)
├── Dockerfile                  # Application image build instructions
└── requirements.txt            # List of Python dependencies
```

### 📝 File Descriptions and Purposes

#### 1. Core
- `app/__init__.py`: Implements the **Application Factory** pattern. Allows flexible application configuration for different environments and avoids circular imports.
- `config.py`: Configuration classes. Reads data from `.env` and provides it to the application (e.g., `SECRET_KEY`, `DATABASE_URL`).
- `models.py`: Describes the DB structure (e.g., `Project`, `Skill`, `Message` tables).

#### 2. Routing
- `routes/`: Using **Flask Blueprints** separates application logic into independent modules.
    - `main.py`: Handles static pages.
    - `portfolio.py`: Manages dynamic output of projects from the database.

#### 3. Frontend (Interface)
- `templates/`: Uses template inheritance. `base.html` contains the general structure, and other pages insert content into `{% block content %}` blocks.
- `components/`: Avoids HTML code duplication (e.g., a single macro for all project cards).
- `static/`: Tailwind CSS is connected for rapid styling. All JS scripts are moved to a separate file for optimization.

#### 4. DevOps & Deployment
- `.env`: Stores sensitive data.
- `Dockerfile`: Creates a lightweight image based on `python:3.11-slim` with dependency installation and launch via Gunicorn.
- `docker-compose.yml`: Allows launching the application and database (e.g., PostgreSQL) with a single `docker-compose up` command.
- `requirements.txt`: Fixes library versions (`Flask`, `Flask-SQLAlchemy`, `python-dotenv`, `gunicorn`).

### 🚀 Scalability
- **Horizontal Scaling**: Thanks to Docker and Gunicorn, the application can easily be deployed in multiple instances behind a load balancer (Nginx).
- **Modularity**: Adding new features (e.g., a blog or admin panel) is done by creating a new Blueprint in the `routes/` folder.
- **Separation**: The Backend provides data via routes, and the Frontend renders it via Jinja2, which allows for an easy replacement of Jinja2 with a full-fledged SPA (React/Vue) in the future, turning Flask into an API.
