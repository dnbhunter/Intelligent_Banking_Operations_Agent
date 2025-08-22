import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.core.config import get_settings

# Import API routes (implemented incrementally)
try:
	from src.channels.banking_api_routes import router as banking_router
except Exception as import_exc:  # Avoid hard failure during initial scaffold
	banking_router = None
	logging.getLogger(__name__).warning(
		"Banking API routes not yet available: %s", import_exc
	)


@asynccontextmanager
async def lifespan(app: FastAPI):
	"""Application startup/shutdown hooks.

	- Load configuration
	- Later: initialize DB connections, vector stores, etc.
	"""
	settings = get_settings()
	logging.basicConfig(level=logging.INFO)
	logging.getLogger(__name__).info("Starting Banking Ops API in %s mode", "debug" if settings.allow_debug else "prod")
	yield
	logging.getLogger(__name__).info("Shutting down Banking Ops API")


app = FastAPI(
	title="Intelligent Banking Operations Agent",
	version="0.1.0",
	lifespan=lifespan,
)


@app.get("/")
async def root():
	return {"status": "ok", "service": "banking-ops"}


if banking_router is not None:
	app.include_router(banking_router, prefix="/api/v1")


def run():
	"""Convenience entry to run with `python main.py`.
	Prefer `uvicorn main:app --reload` in development.
	"""
	import uvicorn
	settings = get_settings()
	uvicorn.run(
		"main:app",
		host=os.getenv("API_HOST", "0.0.0.0"),
		port=int(os.getenv("API_PORT", "8000")),
		reload=settings.allow_debug,
	)


if __name__ == "__main__":
	run()


