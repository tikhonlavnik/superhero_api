import logging

import httpx
from app.config import settings
from app.src.api.exceptions.exceptions import ExternalAPIError


logger = logging.getLogger(__name__)


class SuperheroAPIService:
    def __init__(self):
        self.base_url = settings.SUPERHERO_API_URL
        self.token = settings.SUPERHERO_API_TOKEN
        self.client = httpx.AsyncClient()

    async def get_hero_data(self, name: str) -> dict | None:
        try:
            response = await self.client.get(
                f"{self.base_url}/{self.token}/search/{name}",
            )
            result = response.json()
            if result.get("error") == "character with given name not found":
                return None
            if result.get("response") == "error":
                logger.error(result.get("error"))
                raise ExternalAPIError(f"Superhero API error: {result.get("error")}")
            if result.get("response") == "success" and len(result.get("results")) > 0:
                for hero in result.get("results"):
                    if hero.get("name") == name:
                        return hero
        except httpx.HTTPError as e:
            logger.error({str(e)})
            raise ExternalAPIError(f"Unexpected API error")

    async def close(self):
        await self.client.aclose()
