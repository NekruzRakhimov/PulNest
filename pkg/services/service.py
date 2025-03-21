from datetime import datetime

from logger.logger import logger
from pkg.repositories import service as service_repository
from schemas.service import ServiceSchema


def create_service(service: ServiceSchema):
    try:
        created_service = service_repository.create_service(service.provider_name, service.category_id)
        return created_service
    except Exception as e:
        logger.error(f"Error creating service for provider {service.provider_name}: {e} here is the mistake")
        raise


def get_service_by_id(service_id):
    try:
        service = service_repository.get_service_by_id(service_id)
        if service is not None:
            return service
        else:
            return None
    except Exception as e:
        logger.error(f"Error retrieving service {service_id}: {e}")
        raise


def get_all_services():
    try:
        services = service_repository.get_all_services()
        logger.info(f"Retrieved {len(services)} services.")
        return services
    except Exception as e:
        logger.error(f"Error retrieving all services: {e}")
        raise


def deactivate_service(service_id, is_active):
    try:
        service = service_repository.update_service(service_id, is_active = is_active)
        if service is not None:
            logger.info(f"Service {service_id} deactivated.")
            return service
        else:
            return None
    except Exception as e:
        logger.error(f"Error deactivating service {service_id}: {e}")
        raise


def topup_provider_balance(service_id, amount):
    try:
        service = service_repository.get_service_by_id(service_id)
        if service is not None and amount > 0:
            service.balance += amount
            service.updated_at = datetime.now()
            updated_service = service_repository.update_service(service_id, balance=service.balance)
            logger.info(f"Added {amount} to balance for service {service_id}.")
            return updated_service
        else:
            return None
    except Exception as e:
        logger.error(f"Error topping up balance for service {service_id}: {e}")
        raise


def get_services_by_category_id(category_id):
    try:
        services = service_repository.get_services_by_category_id(category_id)
        logger.info(f"Retrieved {len(services)} services for category {category_id}.")
        return services
    except Exception as e:
        logger.error(f"Error retrieving services for category {category_id}: {e}")
        raise


def soft_delete_service(service_id):
    try:
        service = service_repository.soft_delete_service(service_id)
        if service:
            logger.info(f"Service {service_id} soft deleted.")
            return service
        else:
            return None
    except Exception as e:
        logger.error(f"Error soft deleting service {service_id}: {e}")

        raise


def topup_balance(service_id, amount):
        try:
            service = get_service_by_id(service_id=service_id)

            if service is None:
                logger.warning(f"No active service found with ID {service_id}.")
                return None

            new_balance = service.balance + amount 
            service_id = service_repository.update_service(service_id=service_id, new_balance=new_balance)
            logger.info(f"Balance topped up for service {service_id}. New balance: {service.balance}.")

            return service
        
        except Exception as e:
            logger.error(f"Error topping up balance for service {service_id}: {e}")
            raise Exception(f"An error occurred while updating the balance: {e}")
    

