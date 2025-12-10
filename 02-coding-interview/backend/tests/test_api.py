import pytest
from httpx import AsyncClient
from app.main import app
from app.database import db

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_signup():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/auth/signup",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["user"]["username"] == "testuser"
        assert data["access_token"]
        assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_signup_duplicate_email():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First signup
        await client.post(
            "/api/auth/signup",
            json={
                "username": "user1",
                "email": "duplicate@example.com",
                "password": "password123"
            }
        )
        # Try duplicate
        response = await client.post(
            "/api/auth/signup",
            json={
                "username": "user2",
                "email": "duplicate@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Signup first
        signup_response = await client.post(
            "/api/auth/signup",
            json={
                "username": "logintest",
                "email": "login@example.com",
                "password": "password123"
            }
        )
        
        # Login
        response = await client.post(
            "/api/auth/login",
            json={
                "email": "login@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["email"] == "login@example.com"
        assert data["access_token"]

@pytest.mark.asyncio
async def test_login_invalid_credentials():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "wrong"
            }
        )
        assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_current_user():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Signup and get token
        signup_response = await client.post(
            "/api/auth/signup",
            json={
                "username": "metest",
                "email": "me@example.com",
                "password": "password123"
            }
        )
        token = signup_response.json()["access_token"]
        
        # Get current user
        response = await client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json()["username"] == "metest"

@pytest.mark.asyncio
async def test_create_session():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Signup
        signup_response = await client.post(
            "/api/auth/signup",
            json={
                "username": "sessionuser",
                "email": "session@example.com",
                "password": "password123"
            }
        )
        token = signup_response.json()["access_token"]
        
        # Create session
        response = await client.post(
            "/api/sessions",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "title": "Python Interview",
                "language": "python",
                "description": "Interview session"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Python Interview"
        assert data["language"] == "python"
        assert data["participant_count"] == 1

@pytest.mark.asyncio
async def test_get_sessions():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Signup
        signup_response = await client.post(
            "/api/auth/signup",
            json={
                "username": "listuser",
                "email": "list@example.com",
                "password": "password123"
            }
        )
        token = signup_response.json()["access_token"]
        
        # Create sessions
        for i in range(3):
            await client.post(
                "/api/sessions",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "title": f"Session {i}",
                    "language": "python"
                }
            )
        
        # Get sessions
        response = await client.get(
            "/api/sessions",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 3

@pytest.mark.asyncio
async def test_get_session():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Signup and create session
        signup_response = await client.post(
            "/api/auth/signup",
            json={
                "username": "detailuser",
                "email": "detail@example.com",
                "password": "password123"
            }
        )
        token = signup_response.json()["access_token"]
        
        create_response = await client.post(
            "/api/sessions",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "title": "Detail Session",
                "language": "javascript"
            }
        )
        session_id = create_response.json()["id"]
        
        # Get session details
        response = await client.get(f"/api/sessions/{session_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == session_id
        assert data["title"] == "Detail Session"

@pytest.mark.asyncio
async def test_update_session():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Signup and create session
        signup_response = await client.post(
            "/api/auth/signup",
            json={
                "username": "updateuser",
                "email": "update@example.com",
                "password": "password123"
            }
        )
        token = signup_response.json()["access_token"]
        
        create_response = await client.post(
            "/api/sessions",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "title": "Original Title",
                "language": "python"
            }
        )
        session_id = create_response.json()["id"]
        
        # Update session
        response = await client.put(
            f"/api/sessions/{session_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={"title": "Updated Title", "code": "print('Hello')"}
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"

@pytest.mark.asyncio
async def test_delete_session():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Signup and create session
        signup_response = await client.post(
            "/api/auth/signup",
            json={
                "username": "deleteuser",
                "email": "delete@example.com",
                "password": "password123"
            }
        )
        token = signup_response.json()["access_token"]
        
        create_response = await client.post(
            "/api/sessions",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "title": "To Delete",
                "language": "python"
            }
        )
        session_id = create_response.json()["id"]
        
        # Delete session
        response = await client.delete(
            f"/api/sessions/{session_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 204
        
        # Verify deletion
        get_response = await client.get(f"/api/sessions/{session_id}")
        assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_execute_code():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Signup and create session
        signup_response = await client.post(
            "/api/auth/signup",
            json={
                "username": "codeuser",
                "email": "code@example.com",
                "password": "password123"
            }
        )
        token = signup_response.json()["access_token"]
        
        create_response = await client.post(
            "/api/sessions",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "title": "Code Session",
                "language": "python"
            }
        )
        session_id = create_response.json()["id"]
        
        # Execute code
        response = await client.post(
            f"/api/sessions/{session_id}/execute",
            json={
                "code": "print('Hello, World!')",
                "language": "python"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "Hello, World!" in data["output"]

@pytest.mark.asyncio
async def test_get_participants():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Signup and create session
        signup_response = await client.post(
            "/api/auth/signup",
            json={
                "username": "partuser",
                "email": "part@example.com",
                "password": "password123"
            }
        )
        token = signup_response.json()["access_token"]
        
        create_response = await client.post(
            "/api/sessions",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "title": "Participant Session",
                "language": "python"
            }
        )
        session_id = create_response.json()["id"]
        
        # Get participants
        response = await client.get(f"/api/sessions/{session_id}/participants")
        assert response.status_code == 200
        participants = response.json()
        assert len(participants) >= 1
        assert participants[0]["username"] == "partuser"
