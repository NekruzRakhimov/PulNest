from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from db.models import Service
from db.postgres import engine
from logger.logger import logger 


def create_service(provider_name, category_id):
    with Session(bind=engine) as db:
        try:
            service = Service(
                provider_name=provider_name,
                balance=0,
                category_id=category_id,
                is_active=True,
                created_at=datetime.now()
            )
            db.add(service)
            db.commit()
            
            logger.info(f"Service created for provider {provider_name} in DB.")
            
            return service
          
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating service for provider {provider_name}: {e} in DB")
            raise


def get_service_by_id(service_id):
    with Session(bind=engine) as db:
        try:
            service = db.query(Service).filter(Service.id == service_id, Service.is_active == True, Service.deleted_at == None).first()
            if service:
                logger.info(f"Service {service_id} retrieved from DB.")
                return service
            else:
                logger.warning(f"No service found with ID {service_id} in DB.")
                return None
        except Exception as e:
            logger.error(f"Error retrieving service {service_id}: {e} from DB")
            raise


def get_all_services():
    with Session(bind=engine) as db:
        try:
            services = db.query(Service).filter(Service.is_active == True, Service.deleted_at == None).all()
            return services
        except Exception as e:
            logger.error(f"Error retrieving all services from DB: {e}")
            raise


def get_services_by_category_id(category_id):
    with Session(bind=engine) as db:
        try:
            services = db.query(Service).filter(Service.category_id == category_id, Service.is_active == True, Service.deleted_at == None).all()
            return services
        except Exception as e:
            logger.error(f"Error retrieving services by category id from DB: {e}")
            raise


def update_service(service_id, provider_name = None, category_id = None, is_active = None, ):
    with Session(bind=engine) as db:
        try:
            service = db.query(Service).filter(Service.id == service_id, Service.deleted_at == None).first()
            if service is not None:

                logger.info(f"Service instance in session: {service in db}")


                if provider_name is not None:
                    service.provider_name = provider_name
                    
                if category_id is not None:
                    service.category_id = category_id
                    
                if is_active is not None:
                    service.is_active = is_active
                
                db.commit()
                logger.info(f"Service {service_id} updated.")
                return service.id
            else:
                logger.warning(f"No service found with ID {service_id} in DB.")
                return None
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating service {service_id}: {e} in DB")
            raise


def soft_delete_service(service_id):
    with Session(bind=engine) as db:
        try:
            service = db.query(Service).filter(Service.id == service_id, Service.deleted_at == None).first()
            if service:
                service.deleted_at = datetime.now()
                db.commit()
                logger.info(f"Service {service_id} soft deleted in DB.")
                return service.id
            else:
                logger.warning(f"No service found with ID {service_id} in DB.")
                return None
        except Exception as e:
            db.rollback()
            logger.error(f"Error soft deleting service {service_id}: {e} in DB")
            raise


def update_service_balance(service_id, amount):
    with Session(bind=engine) as db:
        try:
            service = db.query(Service).filter(Service.id == service_id).first()
            if service:
                if amount > 0:
                    service.balance += amount
                    db.commit()
                    logger.info(f"Updated service {service_id} balance to {service.balance}.")
                    return service.balance
                else:
                    logger.error("Amount cannot be negative.")
                    return -1    
            else:
                logger.error(f"Service with ID {service_id} not found.")
                return -1
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating service balance: {e}")
            raise
