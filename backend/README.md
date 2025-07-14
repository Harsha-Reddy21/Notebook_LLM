# Notebook LLM Backend

This is the backend for the Notebook LLM multimodal research assistant, built with FastAPI and LangChain.

## Quick Setup

Run the setup script to create a virtual environment, install dependencies, and set up the necessary files:

```bash
python setup.py
```

## Manual Setup

1. Create a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Unix/MacOS
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with the following content:
```
# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=Notebook LLM
SECRET_KEY=your_secret_key_here_change_this_in_production
ACCESS_TOKEN_EXPIRE_MINUTES=11520

# CORS Configuration
BACKEND_CORS_ORIGINS=["http://localhost:3000"]

# Database Configuration
DATABASE_URL=sqlite:///./notebook_llm.db

# Vector Database Configuration
VECTOR_DB_PATH=./vector_db

# Document Storage
DOCUMENT_STORAGE_PATH=./document_storage

# LLM Configuration
OPENAI_API_KEY=your_openai_api_key_here
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

4. Create necessary directories:
```bash
mkdir -p vector_db document_storage
```

## Running the Application

```bash
python run.py
```

The API will be available at http://localhost:8000

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Default Admin User

The system creates a default admin user on startup:

- Email: admin@example.com
- Password: admin

**Important:** Change this password in production!

## Project Structure

```
backend/
├── app/
│   ├── api/              # API endpoints
│   ├── core/             # Core functionality
│   ├── db/               # Database models and session
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   └── utils/            # Utility functions
├── document_storage/     # Uploaded documents storage
├── vector_db/            # Vector database storage
├── requirements.txt      # Python dependencies
├── setup.py             # Setup script
└── run.py               # Application entry point
``` 