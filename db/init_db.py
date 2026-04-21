# db/init_db.py

from .config import engine, Base
from .models import User, Email, Response, BankingContext

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database setup complete.")

if __name__ == "__main__":
    init_db()
