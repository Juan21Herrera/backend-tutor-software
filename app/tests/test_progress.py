import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.db_users import User
from app.models.db_progress import StudentProgress
from app.routes.auth import get_current_user
from test_database import override_get_db, TestingSessionLocal
from app.db.database import get_db


client = TestClient(app)

# Mock: Authentication dependency function
def override_get_current_user_student():
    return User(id=1, role="student", group="A")

def override_get_current_user_admin():
    return User(id=2, role="admin", group="A")

@pytest.fixture(autouse=True)
def clear_overrides():
    yield
    app.dependency_overrides = {}

@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()



@pytest.fixture
def setup_data(db):
    student = User(id=1, role="student", group="A")
    admin = User(id=2, role="admin", group="A")
    progress = StudentProgress(user_id=1, progress=75.0)

    db.add_all([student, admin, progress])
    db.commit()
    yield
    db.query(StudentProgress).delete()
    db.query(User).delete()
    db.commit()

# Test: Get progress for student
def test_get_student_progress(setup_data):
    app.dependency_overrides[get_current_user] = override_get_current_user_student
    app.dependency_overrides[get_db] = override_get_db

    response = client.get("/progress/1")
    assert response.status_code == 200
    assert response.json() == {"progress": 75.0}

# Test: Get progress for admin with students in group
def test_get_admin_average_progress(setup_data):
    app.dependency_overrides[get_current_user] = override_get_current_user_admin
    app.dependency_overrides[get_db] = override_get_db

    response = client.get("/progress/2")
    assert response.status_code == 200
    assert response.json() == {"progress": 75.0}

# Test: User not found
def test_user_not_found():
    app.dependency_overrides[get_current_user] = override_get_current_user_admin
    app.dependency_overrides[get_db] = override_get_db

    response = client.get("/progress/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Usuario no encontrado"}

# Test: Unauthorized access for student trying to access another user's progress
def test_unauthorized_student_access(setup_data):
    app.dependency_overrides[get_current_user] = override_get_current_user_student
    app.dependency_overrides[get_db] = override_get_db

    response = client.get("/progress/2")
    assert response.status_code == 403
    assert response.json() == {"detail": "No tienes permiso para ver el progreso de otro usuario"}

# Test: Admin without group
def test_admin_without_group(setup_data, db):
    
    admin = User(id=3, role="admin", group=None)
    db.add(admin)
    db.commit()

    app.dependency_overrides[get_current_user] = lambda: admin
    app.dependency_overrides[get_db] = override_get_db

    response = client.get("/progress/3")
    assert response.status_code == 400
    assert response.json() == {"detail": "Administrador sin grupo asignado"}

    db.query(User).filter(User.id == 3).delete()
    db.commit()