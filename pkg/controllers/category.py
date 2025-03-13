import json
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from starlette.responses import Response

from logger.logger import logger
from pkg.services import category as category_service
from schemas.category import CategoryResponse, CategorySchema
from pkg.controllers.middlewares import get_current_user
from utils.auth import TokenPayload

router = APIRouter()


# Create Category
@router.post("/categories", summary="Create new category",  tags=["categories"])
def create_category(category_data: CategorySchema, payload: TokenPayload = Depends(get_current_user)):
    
    if payload.role != "admin":
        return Response(json.dumps({"error": "only admin can create categories"}),
                        status_code=status.HTTP_403_FORBIDDEN)
    
    try:
        category = category_service.create_category(category_data)
        return Response(json.dumps({'message': 'Category created successfully'}), status.HTTP_201_CREATED)
    
    except Exception as e:
        logger.error(f"Error creating category: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the category"
        )


# Get Category by ID
@router.get("/categories/{category_id}", summary="Get category by ID",  tags=["categories"])
def get_category_by_id(category_id):
    try:
        category = category_service.get_category_by_id(category_id)
        if category is not None:
            category_response = CategoryResponse(
                id=category.id,
                name=category.name,
                created_at=category.created_at,
                deleted_at=category.deleted_at
            )
            return JSONResponse(
                content={"Category": category_response.dict()},
                status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={"error": "Category not found"},
                status_code=status.HTTP_404_NOT_FOUND
            )
    except Exception as e:
        logger.error(f"Error retrieving category {category_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the category"
        )


# Get All Categories
@router.get("/categories", summary="Get all categories",  tags=["categories"])
def get_all_categories():
    try:
        categories = category_service.get_all_categories()
        if categories is not None:
            categories_list = []
            for category in categories:
                category_response = CategoryResponse(
                    id=category.id,
                    name=category.name,
                    created_at=category.created_at,
                    deleted_at=category.deleted_at
                )
                categories_list.append(category_response.dict())

            return JSONResponse(
                content={"Categories": categories_list},
                status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={"error": "No categories found"},
                status_code=status.HTTP_404_NOT_FOUND
            )
    except Exception as e:
        logger.error(f"Error retrieving all categories: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving categories"
        )


# Update Category
@router.put("/categories/{category_id}", summary="Update category name",  tags=["categories"])
def update_category(category_id, category_data: CategorySchema, payload: TokenPayload = Depends(get_current_user)):
    
    if payload.role != "admin":
        return Response(json.dumps({"error": "only admin can create categories"}),
                        status_code=status.HTTP_403_FORBIDDEN)
    
    try:
        category = category_service.update_category(category_id, category_data)
        if category is not None:
            return JSONResponse(
                content={"message": f"Category {category_id} updated successfully"},
                status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={"error": "Category not found"},
                status_code=status.HTTP_404_NOT_FOUND
            )
    except Exception as e:
        logger.error(f"Error updating category {category_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the category"
        )


# Soft Delete Category
@router.delete("/categories/{category_id}", summary="Delete category",  tags=["categories"])
def soft_delete_category(category_id, payload: TokenPayload = Depends(get_current_user)):

    if payload.role != "admin":
        return Response(json.dumps({"error": "only admin can create categories"}),
                        status_code=status.HTTP_403_FORBIDDEN)

    try:
        category = category_service.soft_delete_category(category_id)
        if category:
            return JSONResponse(
                content={"message": f"Category {category_id} deleted successfully"},
                status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={"error": "Category not found"},
                status_code=status.HTTP_404_NOT_FOUND
            )
    except Exception as e:
        logger.error(f"Error soft deleting category {category_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while soft deleting the category"
        )