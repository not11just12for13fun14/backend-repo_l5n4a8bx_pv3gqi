import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson.objectid import ObjectId
from datetime import datetime

from database import db, create_document, get_documents
from schemas import Exercise, Workout, WorkoutExercise, WorkoutSet

app = FastAPI(title="Workout Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helpers
class IdResponse(BaseModel):
    id: str


def to_str_id(doc):
    if not doc:
        return doc
    doc["id"] = str(doc.pop("_id")) if doc.get("_id") else None
    # Convert nested ObjectIds if any
    return doc


@app.get("/")
def read_root():
    return {"message": "Workout Tracker Backend Running"}


# Exercises catalog endpoints
@app.post("/api/exercises", response_model=IdResponse)
async def create_exercise(item: Exercise):
    try:
        new_id = create_document("exercise", item)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/exercises")
async def list_exercises():
    try:
        docs = get_documents("exercise")
        return [to_str_id(doc) for doc in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Workouts endpoints
@app.post("/api/workouts", response_model=IdResponse)
async def create_workout(item: Workout):
    try:
        new_id = create_document("workout", item)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class WorkoutQuery(BaseModel):
    limit: Optional[int] = 50


@app.get("/api/workouts")
async def list_workouts(limit: int = 50):
    try:
        docs = get_documents("workout", limit=limit)
        # Sort by performed_at desc if exists
        docs.sort(key=lambda x: x.get("performed_at", datetime.min), reverse=True)
        return [to_str_id(doc) for doc in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
