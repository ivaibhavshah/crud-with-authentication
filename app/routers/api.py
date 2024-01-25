from typing import List, Optional
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def main():
    return {"Welcome": "To My Project"}