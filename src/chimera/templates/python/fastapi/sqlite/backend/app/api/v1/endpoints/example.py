from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.example import Example

router = APIRouter()

@router.get("/", response_model=List[dict])
async def read_examples(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Example))
    return result.scalars().all()

@router.post("/", response_model=dict)
async def create_example(title: str, description: str, db: AsyncSession = Depends(get_db)):
    example = Example(title=title, description=description)
    db.add(example)
    await db.commit()
    await db.refresh(example)
    return example