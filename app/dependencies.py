from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.database import get_db
from app.src.api.exceptions.exceptions import AppError, ExternalAPIError
from app.src.infrastructure.external_services.superhero_api_service import (
    SuperheroAPIService,
)
from app.src.infrastructure.repositories.superhero_repo import SuperheroRepository
from app.src.infrastructure.services.superhero import SuperheroService


async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "type": exc.__class__.__name__},
    )


err_handlers = {AppError: app_error_handler, ExternalAPIError: app_error_handler}


async def get_api_service() -> SuperheroAPIService:
    client = SuperheroAPIService()
    yield client
    await client.close()


def get_hero_service(
    db: AsyncSession = Depends(get_db),
    api_client: SuperheroAPIService = Depends(get_api_service),
) -> SuperheroService:
    try:
        repo = SuperheroRepository(db)
        return SuperheroService(repo, api_client)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Service initialization error: {str(e)}"
        )
