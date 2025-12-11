from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import health, auth, sessions

# Create FastAPI app
app = FastAPI(
    title="Coding Interview Platform",
    description="API for online coding interviews",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    health.router,
    prefix="/api",
    tags=["health"]
)
app.include_router(
    auth.router,
    prefix="/api/auth",
    tags=["auth"]
)
app.include_router(
    sessions.router,
    prefix="/api/sessions",
    tags=["sessions"]
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Coding Interview Platform API"}
