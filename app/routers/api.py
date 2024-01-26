from fastapi import APIRouter

from app.routers.crud.users.routes import router as users

router = APIRouter()


@router.get("/")
def main():
    return {"Welcome": "To My Project"}


router.include_router(users)
