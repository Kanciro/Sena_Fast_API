# tests/test_tipo_c/test_basic_tipo_c.py

import pytest
from fastapi import status

@pytest.mark.tipo_c
@pytest.mark.integration
class TestServiciosUsuario:
    """Tests básicos para servicios de usuario genéricos tipo C"""

    def test_crear_perfil_usuario_valido(self, client, sample_perfil_usuario_tipo_c, auth_headers):
        """Test crear perfil de usuario con datos válidos"""
        response = client.post(
            "/api/v1/perfiles",
            json=sample_perfil_usuario_tipo_c,
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["nombre_completo"] == sample_perfil_usuario_tipo_c["nombre_completo"]
        assert "id" in data

    def test_crear_asignacion_valida(self, client, sample_asignacion_tipo_c, auth_headers):
        """Test crear una asignación de servicio válida para un usuario"""
        response = client.post(
            "/api/v1/asignaciones",
            json=sample_asignacion_tipo_c,
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["service_id"] == sample_asignacion_tipo_c["service_id"]
        assert "id" in data
    
    def test_obtener_asignacion_existente(self, client, sample_asignacion_tipo_c, auth_headers):
        """Test obtener una asignación por ID existente"""
        create_response = client.post(
            "/api/v1/asignaciones",
            json=sample_asignacion_tipo_c,
            headers=auth_headers
        )
        assignment_id = create_response.json()["id"]

        response = client.get(
            f"/api/v1/asignaciones/{assignment_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == assignment_id

    def test_obtener_asignacion_inexistente(self, client, auth_headers):
        """Test obtener una asignación con ID inexistente"""
        response = client.get(
            "/api/v1/asignaciones/99999",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "no encontrada" in response.json()["detail"].lower()

    def test_actualizar_perfil_usuario_invalido(self, client, auth_headers):
        """Test actualizar perfil de usuario con datos inválidos"""
        invalid_data = {
            "nombre_completo": "",
            "telefono": "123"
        }
        # First, create a profile to update
        profile_response = client.post(
            "/api/v1/perfiles",
            json={"nombre_completo": "Test", "telefono": "1234567890", "direccion": "Calle Falsa"},
            headers=auth_headers
        )
        profile_id = profile_response.json()["id"]

        # Try to update with invalid data
        response = client.put(
            f"/api/v1/perfiles/{profile_id}",
            json=invalid_data,
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        errors = response.json()["detail"]
        assert any("nombre_completo" in str(error) for error in errors)