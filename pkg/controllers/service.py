import json
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.responses import Response

from logger.logger import logger
from pkg.services import service as service_service
from schemas.service import ServiceResponse,  ServiceSchema



router = APIRouter()


# Create Service
@router.post("/services", tags="service")
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
@router.get("/services/{service_id}", tags="service")
def get_service_by_id(service_id):
    try:
        service = service_service.get_service_by_id(service_id)
        if service is not None:
            service_response = ServiceSchema(
                merchant_name = service.merchant_name,
                category_id = service.category_id
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


# Get Service by Merchant Name
@router.get("/services/merchant/{merchant_name}", tags="service")
def get_service_by_merchant_name(merchant_name):
    try:
        merchant_name = merchant_name.strip()
        service = service_service.get_service_by_merchant_name(merchant_name)
        if service is not None:
            service_response = ServiceResponse(
                id = service.id,
                merchant_name = service.merchant_name,
                category_id = service.category_id
                ) 
                
            return JSONResponse(
                content={"Service": service_response.dict()},
                status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={"error" : "Service not found"}, 
                status_code=status.HTTP_404_NOT_FOUND
            )
        
    except Exception as e:
        logger.error(f"Error retrieving service for merchant {merchant_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the service"
        )


# Get All Services
@router.get("/services", tags="service")
def get_all_services():
    try:
        services = service_service.get_all_services()
        if services is not None:
            services_list = []
            for service in services:
                service_response = ServiceSchema(
                    merchant_name=service.merchant_name,
                    category_id=service.category_id
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
@router.get("/services-by-category/{category_id}", tags="service")
def get_services_by_category_id(category_id):
    try:
        services = service_service.get_services_by_category_id(category_id)
        if services is not None:
            services_list =[]
            for service in services:
                service= ServiceSchema(
                    merchant_name=service.merchant_name,
                    category_id=service.category_id
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
@router.patch("/services/{service_id}/deactivate", tags="service")
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
@router.delete("/services/{service_id}/soft-delete", tags="service")
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