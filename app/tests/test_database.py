from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base, get_db
import sys
import os

# Asegura el path correcto para imports de app.*
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# ✅ Usa una base SQLite temporal en disco
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Crea el engine y session de prueba
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Crea todas las tablas antes de usarlas
Base.metadata.create_all(bind=engine)

# Dependency override que usarás en tus tests
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
