from contextlib import asynccontextmanager
from asyncpg import PostgresError
from fastapi import FastAPI
from server.routers import health, interactions
from infra.db.postgres_repository import PostgresRepository
import asyncio

MAX_ATTEMPTS = 5
INITIAL_DELAY = 2.0

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1 repository handling the connection pool instead of making connections on request
    # global repository
    repository = PostgresRepository()

    last_exc = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            await repository._make_connection_pool()
            app.state.repository = repository
            print("Database connection pool initialized")
            break
        except (PostgresError, OSError) as exc:
            last_exc = exc
            if attempt == MAX_ATTEMPTS:
                raise
            sleep_for = INITIAL_DELAY * attempt
            print(f"DB not ready (attempt {attempt}/{MAX_ATTEMPTS}), retrying in {sleep_for}s...")
            await asyncio.sleep(sleep_for)
    try:
        yield # app is running

    finally:
        # Cleanup
        if repository._connection_pool:
            await repository._connection_pool.close()
            print("Database connection pool closed")

app = FastAPI(lifespan=lifespan)
# app.state.repository = repository

app.include_router(interactions.router)
app.include_router(health.router)