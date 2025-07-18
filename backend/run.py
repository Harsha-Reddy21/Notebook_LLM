import uvicorn
from app.db.init_db import init_db
from app.db.session import SessionLocal

if __name__ == "__main__":
    # Initialize the database
    db = SessionLocal()
    init_db(db)
    db.close()
    
    # Run the server
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 