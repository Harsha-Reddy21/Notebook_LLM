import os
import subprocess
import sys
import venv
from pathlib import Path


def create_venv():
    """Create a virtual environment if it doesn't exist."""
    venv_dir = Path("venv")
    if not venv_dir.exists():
        print("Creating virtual environment...")
        venv.create(venv_dir, with_pip=True)
        return True
    return False


def install_requirements():
    """Install requirements from requirements.txt."""
    print("Installing requirements...")
    if sys.platform == 'win32':
        pip_path = "venv\\Scripts\\pip"
    else:
        pip_path = "venv/bin/pip"
    
    subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])


def create_directories():
    """Create necessary directories if they don't exist."""
    directories = ["vector_db", "document_storage"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")


def setup_env_file():
    """Check if .env file exists, create it if it doesn't."""
    env_file = Path(".env")
    if not env_file.exists():
        print("Creating .env file...")
        with open(env_file, "w") as f:
            f.write("""# API Configuration
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
# Replace with your actual API keys
OPENAI_API_KEY=your_openai_api_key_here
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
""")
        print("Created .env file. Please edit it to add your API keys.")
    else:
        print(".env file already exists.")


def main():
    """Main setup function."""
    print("Setting up Notebook LLM backend...")
    
    # Create virtual environment if it doesn't exist
    created_venv = create_venv()
    
    # Install requirements
    install_requirements()
    
    # Create necessary directories
    create_directories()
    
    # Setup .env file
    setup_env_file()
    
    print("\nSetup complete!")
    print("\nTo run the application:")
    if sys.platform == 'win32':
        print("1. Activate the virtual environment: .\\venv\\Scripts\\activate")
    else:
        print("1. Activate the virtual environment: source venv/bin/activate")
    print("2. Edit the .env file to add your API keys")
    print("3. Run the application: python run.py")


if __name__ == "__main__":
    main() 