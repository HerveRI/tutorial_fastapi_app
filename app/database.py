from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg.rows import dict_row
from .config import settings



SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# One way to connect to database using just the driver not the ORM
# while True:

#     try:
#         db_conn = psycopg.connect(host='localhost', dbname='social_app_db', user='social_app_admin', password='social_with_app')
#         cursor = db_conn.cursor(row_factory=dict_row)
#         print("Connection established")
#         break
#     except Exception as e:
#         print("Attempt to connect to database failed, Retrying in 5 seconds...")
#         db_conn = None
#         #print(f"Error: {e}")
#         time.sleep(5)