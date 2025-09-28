import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app

# Configuración de base de datos de prueba
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    db = TestingSessionLocal(bind=connection)
    yield db
    db.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def sample_user_generic():
    """Fixture para usuario genérico de prueba"""
    return {
        "username": "usuario_generico_test",
        "email": "test@ejemplo.com",
        "password": "password123"
    }

@pytest.fixture
def sample_perfil_usuario_tipo_c():
    """Fixture para datos de perfil de usuario"""
    return {
        "nombre_completo": "Juan Perez",
        "telefono": "3001234567",
        "direccion": "Calle Falsa 123"
    }

@pytest.fixture
def sample_asignacion_tipo_c():
    """Fixture para datos de asignación de servicio"""
    return {
        "service_id": 1,
        "user_id": 1
    }

@pytest.fixture
def auth_headers(client, sample_user_generic):
    """Fixture para headers de autenticación genérica"""
    # Se registra el usuario directamente en la base de datos de prueba
    client.post("/api/v1/auth/register", json=sample_user_generic)
    
    login_data = {
        "username": sample_user_generic["username"],
        "password": sample_user_generic["password"]
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}