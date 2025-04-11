from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Teacher

async def orm_add_teacher(session: AsyncSession, data: dict):
    obj = Teacher(
        name=data["full_name"],
        description=data["description"],
        image=data["image"]

    )
    session.add(obj)

    await session.commit()

async def orm_get_teachers(session: AsyncSession):
     query = select(Teacher)
     result = await session.execute(query)
     return result.scalars().all()


async def orm_get_teacher(session: AsyncSession, product_id: int):
    query = select(Teacher).where(Teacher.id == product_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_teacher(session: AsyncSession, product_id: int, data):
    query = update(Teacher).where(Teacher.id == product_id).values(
        name=data["full_name"],
        description=data["description"],
        image=data["image"],)
    await session.execute(query)
    await session.commit()


async def orm_delete_teacher(session: AsyncSession, product_id: int):
    query = delete(Teacher).where(Teacher.id == product_id)
    await session.execute(query)
    await session.commit()
