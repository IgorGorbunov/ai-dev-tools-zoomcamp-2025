import asyncio
import httpx
from typing import Optional

BASE_URL = "http://localhost:8000"

class APIVerifier:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.user_id: Optional[str] = None
        self.session_id: Optional[str] = None
        self.results = []

    async def verify_all(self):
        """Run all verification tests"""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=10) as client:
            self.client = client
            
            await self.test_health()
            await self.test_auth_flow()
            await self.test_session_flow()
            await self.test_code_execution()
            await self.test_participants()
            
        self.print_results()

    async def test_health(self):
        """Test health check endpoint"""
        try:
            response = await self.client.get("/api/health")
            if response.status_code == 200:
                self.results.append(("✓ Health Check", "PASS"))
            else:
                self.results.append(("✗ Health Check", f"FAIL: {response.status_code}"))
        except Exception as e:
            self.results.append(("✗ Health Check", f"ERROR: {str(e)}"))

    async def test_auth_flow(self):
        """Test authentication endpoints"""
        try:
            # Signup
            signup_data = {
                "username": "verifyuser",
                "email": "verify@example.com",
                "password": "password123"
            }
            response = await self.client.post("/api/auth/signup", json=signup_data)
            if response.status_code == 201:
                data = response.json()
                self.token = data["access_token"]
                self.user_id = data["user"]["id"]
                self.results.append(("✓ Signup", "PASS"))
            else:
                self.results.append(("✗ Signup", f"FAIL: {response.status_code}"))
                return

            # Login
            login_data = {
                "email": "verify@example.com",
                "password": "password123"
            }
            response = await self.client.post("/api/auth/login", json=login_data)
            if response.status_code == 200:
                self.results.append(("✓ Login", "PASS"))
            else:
                self.results.append(("✗ Login", f"FAIL: {response.status_code}"))

            # Get current user
            headers = {"Authorization": f"Bearer {self.token}"}
            response = await self.client.get("/api/auth/me", headers=headers)
            if response.status_code == 200:
                self.results.append(("✓ Get Current User", "PASS"))
            else:
                self.results.append(("✗ Get Current User", f"FAIL: {response.status_code}"))
        except Exception as e:
            self.results.append(("✗ Auth Flow", f"ERROR: {str(e)}"))

    async def test_session_flow(self):
        """Test session endpoints"""
        if not self.token:
            self.results.append(("✗ Session Flow", "SKIP: Not authenticated"))
            return

        try:
            headers = {"Authorization": f"Bearer {self.token}"}

            # Create session
            create_data = {
                "title": "Verification Session",
                "language": "python",
                "description": "Test session"
            }
            response = await self.client.post("/api/sessions", json=create_data, headers=headers)
            if response.status_code == 201:
                data = response.json()
                self.session_id = data["id"]
                self.results.append(("✓ Create Session", "PASS"))
            else:
                self.results.append(("✗ Create Session", f"FAIL: {response.status_code}"))
                return

            # Get sessions
            response = await self.client.get("/api/sessions", headers=headers)
            if response.status_code == 200:
                self.results.append(("✓ Get Sessions", "PASS"))
            else:
                self.results.append(("✗ Get Sessions", f"FAIL: {response.status_code}"))

            # Get session details
            response = await self.client.get(f"/api/sessions/{self.session_id}")
            if response.status_code == 200:
                self.results.append(("✓ Get Session Details", "PASS"))
            else:
                self.results.append(("✗ Get Session Details", f"FAIL: {response.status_code}"))

            # Update session
            update_data = {
                "title": "Updated Session",
                "code": "print('test')"
            }
            response = await self.client.put(f"/api/sessions/{self.session_id}", json=update_data, headers=headers)
            if response.status_code == 200:
                self.results.append(("✓ Update Session", "PASS"))
            else:
                self.results.append(("✗ Update Session", f"FAIL: {response.status_code}"))
        except Exception as e:
            self.results.append(("✗ Session Flow", f"ERROR: {str(e)}"))

    async def test_code_execution(self):
        """Test code execution endpoint"""
        if not self.session_id:
            self.results.append(("✗ Code Execution", "SKIP: No session"))
            return

        try:
            execution_data = {
                "code": "print('Hello, Verification!')",
                "language": "python"
            }
            response = await self.client.post(
                f"/api/sessions/{self.session_id}/execute",
                json=execution_data
            )
            if response.status_code == 200:
                data = response.json()
                if data["success"]:
                    self.results.append(("✓ Code Execution", "PASS"))
                else:
                    self.results.append(("✗ Code Execution", f"FAIL: {data['error']}"))
            else:
                self.results.append(("✗ Code Execution", f"FAIL: {response.status_code}"))
        except Exception as e:
            self.results.append(("✗ Code Execution", f"ERROR: {str(e)}"))

    async def test_participants(self):
        """Test participants endpoint"""
        if not self.session_id:
            self.results.append(("✗ Get Participants", "SKIP: No session"))
            return

        try:
            response = await self.client.get(f"/api/sessions/{self.session_id}/participants")
            if response.status_code == 200:
                self.results.append(("✓ Get Participants", "PASS"))
            else:
                self.results.append(("✗ Get Participants", f"FAIL: {response.status_code}"))
        except Exception as e:
            self.results.append(("✗ Get Participants", f"ERROR: {str(e)}"))

    def print_results(self):
        """Print verification results"""
        print("\n" + "=" * 60)
        print("API VERIFICATION RESULTS")
        print("=" * 60)
        for test_name, result in self.results:
            print(f"{test_name:<30} {result}")
        print("=" * 60)
        
        passed = sum(1 for _, r in self.results if "PASS" in r)
        total = len(self.results)
        print(f"\nTotal: {passed}/{total} tests passed")
        print("=" * 60 + "\n")

async def main():
    verifier = APIVerifier()
    await verifier.verify_all()

if __name__ == "__main__":
    asyncio.run(main())
