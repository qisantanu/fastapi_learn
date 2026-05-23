from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class ProcessedData(SQLModel, table=True):
    __tablename__ = "processed_data"
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.now)
    original_count: int
    mean: float
    std_dev: float
    min_val: float
    max_val: float
    raw_response: str # Store the full JSON string for reference
