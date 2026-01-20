import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_cors_allows_origin():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Preflight request
        response = await client.options(
            "/api/health",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "GET",
            },
        )

        assert response.status_code in (200, 204)
        # CORS middleware may echo the requesting origin or return '*'
        allow_origin = response.headers.get("access-control-allow-origin")
        assert allow_origin is not None
        assert allow_origin in ("*", "http://localhost:5173")


@pytest.mark.asyncio
async def test_execute_with_stdin():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Signup user
        signup = await client.post(
            "/api/auth/signup",
            json={
                "username": "stdinuser",
                "email": "stdin@example.com",
                "password": "password123",
            },
        )
        assert signup.status_code == 201

        token = signup.json()["access_token"]

        # Create session
        create_resp = await client.post(
            "/api/sessions",
            headers={"Authorization": f"Bearer {token}"},
            json={"title": "Stdin Session", "language": "python"},
        )
        assert create_resp.status_code == 201
        session_id = create_resp.json()["id"]

        # Execute a Python snippet that reads from stdin
        exec_resp = await client.post(
            f"/api/sessions/{session_id}/execute",
            json={
                "code": "print(input())",
                "language": "python",
                "stdin": "Hello-stdin",
            },
        )

        assert exec_resp.status_code == 200
        data = exec_resp.json()
        assert data["success"] is True
        assert "Hello-stdin" in data["output"]
