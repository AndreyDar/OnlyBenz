# Example dependency for getting a database session
def get_db():
    db = "FakeDatabaseConnection"
    try:
        yield db
    finally:
        db.close()