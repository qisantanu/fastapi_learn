from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Annotated
import logging
from sqlmodel import SQLModel
from database.database import engine
from controllers.items import router as items_router
from controllers.users import router as users_router
from controllers.weathers import router as weathers_router
from controllers.data_processing import router as data_processing_router
from models.processed_data_model import ProcessedData

# Create FastAPI instance
app = FastAPI()
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(items_router)
app.include_router(users_router)
app.include_router(weathers_router)
app.include_router(data_processing_router)

# # Root endpoint
@app.get("/products/{product_id}")
async def read_product(
    product_id: Annotated[int, Path(title="The ID of the product to get")],
    q: Annotated[Optional[str], Query(title="Query string for the product to search in the database")],
):
    results = {"product_id": product_id}

    if q:
        results.update({"q": q})

    return results

#     return {"item_id": item_id, "q": q}

# to run the FastAPI app, use the command:
# uvicorn main:app --reload --log-config=log_conf.yml
# alembic revision --autogenerate -m "Add user-item relationship"
# alembic upgrade head  
# rails' pry like lib is : breakpoint()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
