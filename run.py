import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from APIs.home.view import home_router
from APIs.project.view import project_router
from APIs.db_preprocessing import db_preparation




app = FastAPI(title="Portfolio Backend")



origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    # Add any other allowed origins here
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows these origins to make requests
    allow_credentials=True,  # Allow sending credentials (e.g., cookies)
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)



app.include_router(home_router)
app.include_router(project_router)



if __name__ == "__main__":
    asyncio.run(db_preparation())
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)
