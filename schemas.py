from pydantic import BaseModel
from typing import Optional


class BuildUpdate(BaseModel):
    name_build: Optional[str] = None
    cpu_id: Optional[int] = None
    motherboard_id: Optional[int] = None
    gpu_id: Optional[int] = None
    psu_id: Optional[int] = None
    cooler_id: Optional[int] = None
    case_chassis_id: Optional[int] = None

class RAMAdd(BaseModel):
    ram_id: int
    quantity: int = 1

class StorageAdd(BaseModel):
    storage_id: int