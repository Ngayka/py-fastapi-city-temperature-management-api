from typing import List, Optional

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from cities.crud import create_city, get_all_cities_or_city_by_id, delete_city, update_city
from cities.schemas import CityListSchema, CityCreateSchema, CityUpdateSchema
from database import get_db

router = APIRouter()


@router.post("/",
             response_model=CityListSchema,
             summary="Create city",
             status_code=status.HTTP_201_CREATED)
async def add_city(city: CityCreateSchema, db: AsyncSession = Depends(get_db)):
    return await create_city(city, db)


@router.get("/{city_id}/",
            response_model=List[CityListSchema],
            summary="Get one city by id, or all cities",
            status_code=status.HTTP_200_OK)
async def get_cities(city_id: Optional[int] = None,
                     db: AsyncSession = Depends(get_db),
                     skip: int = 0,
                     limit: int = 10,
                     ):
    return await get_all_cities_or_city_by_id(
        city_id=city_id,
        db=db,
        skip=skip,
        limit=limit
    )


@router.patch("/{city_id}/", response_model=CityListSchema,
              summary="Patch city by id",
              status_code=status.HTTP_200_OK)
async def upgrade_city(
        city_id: int,
        city_data: CityUpdateSchema,
        db: AsyncSession = Depends(get_db)):
    return await update_city(
        city_id=city_id,
        city_data=city_data,
        db=db)


@router.delete("/{city_id}/",
               summary="Delete city by id",
               status_code=status.HTTP_404_NOT_FOUND)
async def delete_city_by_id(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> dict:
    return await delete_city(city_id=city_id, db=db)
