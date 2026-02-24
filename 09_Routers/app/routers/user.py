from fastapi import APIRouter, Depends
from app.core import dependecis


router = APIRouter(
    prefix="/users",
    tags=["USERS"],
    dependencies=[Depends(dependecis.log_request)]
)

users_list = [
    {"id": 1,"name": "Alice", "age": 30},
    {"id": 2,"name": "Bob", "age": 25},
    {"id": 3,"name": "Charlie", "age": 35},
]


@router.get("/users/")
async def get_user():
    return users_list

@router.get("/users/{user_id}")
async def get_user_by_id(user_id: int ):
    return next ((user for user in users_list if user["id"] == user_id), {"error": "User not found"})