from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL credentials
USERNAME = "root"
PASSWORD = "-------"
HOST = "localhost"
PORT = "3306"
DATABASE = "secureapp"

# Properly URL-encoded password for SQLAlchemy (handles special characters like @)
from urllib.parse import quote_plus
encoded_password = quote_plus(PASSWORD)

DATABASE_URL = f"mysql+pymysql://{USERNAME}:{encoded_password}@{HOST}:{PORT}/{DATABASE}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
