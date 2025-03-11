import json
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.responses import Response

from logger.logger import logger
from pkg.services import service as service_service
from pkg.services import category as service_category
from schemas.service import ServiceResponse,  ServiceSchema



router = APIRouter()


# Create Service
@router.post("/services", summary="Create service", tags=["services"])
def create_service(service_data: ServiceSchema):
    try:
        service = service_service.create_service(service_data)
   
        return Response(json.dumps({'message': 'Service created successfully'}), status.HTTP_201_CREATED)
   
    except Exception as e:
        logger.error(f"Error creating service: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the service"
        )


# Get Service by ID
@router.get("/services/{service_id}", summary="Get service by ID", tags=["services"])
def get_service_by_id(service_id):
    try:
        service = service_service.get_service_by_id(service_id)
        if service is not None:
            category_name = service_category.get_category_by_id(service.category_id).name
            service_response = ServiceResponse(
                id = service.id,
                provider_name = service.provider_name,
                category_name =  category_name
            )
    
            return JSONResponse(
                content={"Service": service_response.dict()},
                status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(content={"error" : "Service not found"}, 
                                status_code=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        logger.error(f"Error retrieving service {service_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the service"
        )


# Get All Services
@router.get("/services", summary="Get service all services", tags=["services"])
def get_all_services():
    try:
        services = service_service.get_all_services()
        if services is not None:
            services_list = []
            for service in services:
                category_name = service_category.get_category_by_id(service.category_id).name
                service_response = ServiceResponse(
                    id = service.id,
                    provider_name = service.provider_name,
                    category_name = category_name
                )
                
                services_list.append(service_response.dict())

            return JSONResponse(
                content={"Services": services_list},
                status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={"error" : "Service not found"}, 
                status_code=status.HTTP_404_NOT_FOUND
            )
    except Exception as e:
        logger.error(f"Error retrieving all services: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving services"
        )


# Get Services by Category ID
@router.get("/services-by-category/{category_id}", summary="Get service by category ID", tags=["services"])
def get_services_by_category_id(category_id):
    try:
        services = service_service.get_services_by_category_id(category_id)
        if services is not None:
            services_list =[]
            for service in services:
                category_name = service_category.get_category_by_id(service.category_id).name
                service= ServiceResponse(
                    id = service.id,
                    provider_name = service.provider_name,
                    category_name = category_name
                )
                services_list.append(service.dict())        

            return JSONResponse(
            content={'Services': services_list},
            status_code=status.HTTP_200_OK
        )
        else:
            return JSONResponse(
                content={"error" : "Service not found"}, 
                status_code=status.HTTP_404_NOT_FOUND
            )
    except Exception as e:
        logger.error(f"Error retrieving services for category {category_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving services"
        )


# Deactivate Service
@router.patch("/services/{service_id}", summary="Deactivate service by ID", tags=["services"])
def deactivate_service(service_id):
    try:
        service = service_service.deactivate_service(service_id)
        if service is not None:
            return JSONResponse(
                content={"message" : f"Service {service_id} is deactivated"},
                status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={"error" : "Service not found"}, 
                status_code=status.HTTP_404_NOT_FOUND
            )
    except Exception as e:
        logger.error(f"Error deactivating service {service_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deactivating the service"
        )


# Soft Delete Service
@router.delete("/services/{service_id}", summary="Delete service by ID", tags=["services"])
def soft_delete_service(service_id):
    try:
        service = service_service.soft_delete_service(service_id)
        if service:
            return JSONResponse(
                content={"message" : f"Service {service_id} deleted successfully"},
                status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={"error" : "Service not found"}, 
                status_code=status.HTTP_404_NOT_FOUND
            )
    except Exception as e:
        logger.error(f"Error soft deleting service {service_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while soft deleting the service"
        )