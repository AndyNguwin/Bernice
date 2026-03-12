from contextlib import asynccontextmanager
from fastapi import FastAPI
from server.routers import health, interactions
from infra.db.postgres_repository import PostgresRepository

# repository: PostgresRepository

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1 repository handling the connection pool instead of making connections on request
    # global repository
    repository = PostgresRepository()
    await repository._make_connection_pool()
    app.state.repository = repository
    print("Database connection pool initialized")

    yield # app is running

    # Cleanup
    if repository._connection_pool:
        await repository._connection_pool.close()
        print("Database connection pool closed")

app = FastAPI(lifespan=lifespan)
# app.state.repository = repository

app.include_router(interactions.router)
app.include_router(health.router)