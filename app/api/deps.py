from db.session import SessionLocalCRM


def get_db():
    try:
        db = SessionLocalCRM()
        yield db
    finally:
        db.close()


