from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np

router = APIRouter(prefix="/data", tags=["data-processing"])

class DataPayload(BaseModel):
    readings: List[float]
    multiplier: float = 1.0

@router.post("/process")
async def process_data(payload: DataPayload):
    if not payload.readings:
        raise HTTPException(status_code=400, detail="Readings list cannot be empty")
    
    # 1. Convert the standard Python list to a NumPy array
    arr = np.array(payload.readings)

    # 2. Perform vectorized operations (scaling the data)
    scaled_arr = arr * payload.multiplier

    # 3. Calculate metrics using NumPy aggregations
    response_data = {
        "original_count": len(arr),
        "scaled_readings": scaled_arr.tolist(), # .tolist() converts it back to a standard Python list
        "metrics": {
            "mean": float(np.mean(scaled_arr)),
            "standard_deviation": float(np.std(scaled_arr)),
            "min": float(np.min(scaled_arr)),
            "max": float(np.max(scaled_arr))
        }
    }
    return response_data
