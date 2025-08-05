import logging

import uvicorn
from fastapi import FastAPI

from app.dependencies import err_handlers
from app.src.api.v1.heroes import hero_router


app = FastAPI(debug=True)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

for exception, handler in err_handlers.items():
    app.add_exception_handler(exception, handler)

app.include_router(hero_router, tags=["Heroes"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
