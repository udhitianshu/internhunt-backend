from fastapi import FastAPI
from app.routes.api_routes import router as api_router
from app.routes.resume_routes import router as resume_router
from app.routes.policy_routes import router as policy_router
from fastapi.responses import FileResponse

app = FastAPI(
    title="InternHunt.AI",
    description="AI-powered Internship & Skill Matcher Backend",
    version="1.0.0"
)

# Include main routes
app.include_router(api_router)
app.include_router(resume_router)
app.include_router(policy_router)


@app.get("/")
def root():
    return {"message": "InternHunt.AI is running 🚀"}

@app.get("/health")
def health_check():
    return {"status": "healthy ✅"}

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("favicon.ico")