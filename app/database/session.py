from db.engine import engine
from sqlalchemy.orm import sessionmaker

SessionLocalCRM = sessionmaker(autocommit=False, autoflush=False, bind=engine)
