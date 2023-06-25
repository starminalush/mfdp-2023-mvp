from fastapi import APIRouter, Depends, Query

from crud.student import get_all_students
from api.deps import get_db, get_c3_client
from schemas.students import Student
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.get("/", response_model=list[Student | None])
async def get_students(
    db: AsyncSession = Depends(get_db)
):
    all_students = await get_all_students(db=db)
    return [Student(track_id = res['track_id']) for res in all_students]
