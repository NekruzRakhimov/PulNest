import uvicorn
from fastapi import FastAPI

from configs.config import settings
from db.models import migrate_tables
from pkg.controllers.default import router as default_router
from pkg.controllers.auth import router as auth_router
from pkg.controllers.wallet import router as wallet_router
from pkg.controllers.cards import router as cards_router
from pkg.controllers.transactions import router as transactions_router
from pkg.controllers.history import router as history_router
from pkg.controllers.service import router as service_router
from pkg.controllers.category import router as category_router



from pkg.controllers.service import router as service_router



app = FastAPI() 


if __name__ == "__main__":
    # Создание таблиц
    migrate_tables()

    # Создание роутера
    app = FastAPI()
    # Подключаем маршруты
    app.include_router(default_router)
    app.include_router(auth_router)
    app.include_router(wallet_router)
    app.include_router(cards_router)
    app.include_router(transactions_router)
    app.include_router(history_router)
    app.include_router(service_router)
    app.include_router(category_router)


    app.include_router(service_router)


    

    uvicorn.run(app, port=settings.port, host=settings.host)

