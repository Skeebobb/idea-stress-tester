from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import CategoryItem, IdeaRequest, IdeaResponse, ModelInfoResponse
from app.services.idea_service import IdeaAnalysisService


app = FastAPI(title="Idea Stress Tester API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

idea_service: IdeaAnalysisService | None = None


@app.on_event("startup")
def startup_event() -> None:
    global idea_service
    idea_service = IdeaAnalysisService()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze", response_model=IdeaResponse)
def analyze_idea(payload: IdeaRequest) -> dict:
    if idea_service is None:
        raise HTTPException(status_code=500, detail="Service is not initialized")

    return idea_service.analyze_idea(payload.idea)


@app.get("/model-info", response_model=ModelInfoResponse)
def get_model_info() -> dict:
    if idea_service is None:
        raise HTTPException(status_code=500, detail="Service is not initialized")

    try:
        return idea_service.get_model_info()
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/categories", response_model=list[CategoryItem])
def get_categories() -> list[dict]:
    if idea_service is None:
        raise HTTPException(status_code=500, detail="Service is not initialized")

    try:
        return idea_service.get_categories()
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))