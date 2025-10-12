from fastapi import FastAPI
from app.routes.api_routes import router as api_router
from app.routes.resume_routes import router as resume_router



app = FastAPI(
    title="InternHunt.AI",
    description="AI-powered Internship & Skill Matcher Backend",
    version="1.0.0"
)

# Include main routes
app.include_router(api_router)
app.include_router(resume_router)

@app.get("/")
def root():
    return {"message": "InternHunt.AI is running 🚀"}

@app.get("/health")
def health_check():
    return {"status": "healthy ✅"}
