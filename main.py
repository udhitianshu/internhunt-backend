from fastapi import FastAPI
from app.routes.api_routes import router as api_router
from app.routes.resume_routes import router as resume_router
from app.routes.policy_routes import router as policy_router
from fastapi.responses import FileResponse
from app.routes.resume_generate_routes import router as resume_generate_router
from app.routes.resume_review_routes import router as resume_review_router
from app.routes.internship_routes import router as internship_router
from app.routes.payment_routes import router as payment_router
from app.routes.resume_generate_routes import router as resume_generate_router
from app.routes.file_routes import router as file_router




app = FastAPI(
    title="InternHunt.AI",
    description="AI-powered Internship & Skill Matcher Backend",
    version="1.0.0"
)

# Include main routes
app.include_router(api_router)
app.include_router(resume_router)
app.include_router(policy_router)
app.include_router(resume_generate_router)
app.include_router(resume_review_router)
app.include_router(internship_router)
app.include_router(payment_router)
app.include_router(resume_generate_router)
app.include_router(file_router)



@app.get("/")
def root():
    return {"message": "InternHunt.AI is running 🚀"}

@app.get("/health")
def health_check():
    return {"status": "healthy ✅"}

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("favicon.ico")