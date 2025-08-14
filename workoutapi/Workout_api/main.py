from fastapi import FastAPI
from Workout_api.routers import api_router


app = FastAPI(tittle="Workout API", description="API for managing workout routines", version="1.0.0")
app.include_router(api_router)
