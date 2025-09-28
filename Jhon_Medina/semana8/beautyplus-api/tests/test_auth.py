import pytest
from fastapi import status
from fastapi.testclient import TestClient
from app.routers.auth_routers import get_password_hash

@pytest.mark.auth
@pytest.mark.integration
class TestAutenticacionGenerica:
    """Tests de autenticación genérica universal"""

    def test_registro_usuario_valido(self, client: TestClient, db_session, sample_user_generic):
        """Test para registrar un usuario con datos válidos"""
        response = client.post(
            "/api/v1/auth/register",
            json=sample_user_generic
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert "message" in response.json()
        assert response.json()["message"] == "Usuario creado exitosamente"

    def test_registro_usuario_existente(self, client: TestClient, db_session, sample_user_generic):
        """Test para registrar un usuario que ya existe"""
        # Se registra el usuario primero para que el segundo intento falle
        client.post("/api/v1/auth/register", json=sample_user_generic)
        response = client.post(
            "/api/v1/auth/register",
            json=sample_user_generic
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "Usuario ya existe"

    def test_login_credenciales_validas(self, client: TestClient, db_session, sample_user_generic):
        """Test para iniciar sesión con credenciales válidas"""
        client.post("/api/v1/auth/register", json=sample_user_generic)
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": sample_user_generic["username"],
                "password": sample_user_generic["password"]
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"

    def test_login_credenciales_invalidas(self, client: TestClient, db_session, sample_user_generic):
        """Test para iniciar sesión con credenciales inválidas"""
        client.post("/api/v1/auth/register", json=sample_user_generic)
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "usuario_incorrecto",
                "password": "contraseña_incorrecta"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Credenciales incorrectas"

    def test_acceso_con_token(self, client: TestClient, auth_headers):
        """Test para acceder a un _endpoint_ protegido con un token válido"""
        response = client.get("/api/v1/perfiles", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_acceso_sin_token(self, client: TestClient):
        """Test para acceder a un _endpoint_ protegido sin un token"""
        response = client.get("/api/v1/perfiles")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED