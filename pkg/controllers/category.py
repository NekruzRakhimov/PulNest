from typing import List
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pkg.services import category as category_service
from schemas.category import Category as CategorySchema

router = APIRouter()


@router.get("/", response_model=List[CategorySchema], tags=["category"])
def get_all_cards():
    categories = category_service.get_categories()
    return categories  # FastAPI сам конвертирует в JSON


@router.get("/{category_id}", response_model=CategorySchema, tags=["category"])
def get_category_by_id(category_id: int):
    category = category_service.get_category_by_id(category_id)
    if category is None:
        return JSONResponse(
            content={"error": "Category not found"},
            status_code=status.HTTP_404_NOT_FOUND
        )
    return category  # FastAPI сам конвертирует в JSON


@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED, tags=["category"])
def create_category(category: CategorySchema):
    category_new = category_service.create_new_category(category.category_name)
    return category_new


@router.delete("/{category_id}", status_code=status.HTTP_200_OK, tags=["category"])
def delete_category(category_id: int):
    category_service.delete_category_by_id(category_id)
    return {"message": "Category deleted successfully"}


@router.put("/{category_id}", status_code=status.HTTP_200_OK, tags=["category"])
def update_category(category_id: int, category: CategorySchema):
    category_service.update_category_by_id(category_id, category.category_name)
    return {"message": "Category updated successfully"}
