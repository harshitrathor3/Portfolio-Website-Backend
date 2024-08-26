import asyncio
import uvicorn
from fastapi import FastAPI

from APIs.home.view import home_router
from APIs.project.view import project_router
from APIs.db_preprocessing import db_preparation




app = FastAPI(title="Portfolio Backend")


app.include_router(home_router)
app.include_router(project_router)



if __name__ == "__main__":
    import platform
    print(platform.python_version())
    asyncio.run(db_preparation())
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)
