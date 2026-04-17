from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"server is starting ...")
    yield
    print(f"server has been stopped!")

version = "v1"

app = FastAPI(
    # 通过生命周期时间实现让一个任务在程序启动的时候运行
    lifespan=life_span,
    version = version,
    title = "bookly",
    description = "A REST API for book review web service"
)

app.include_router(
    book_router, 
    prefix=f"/api/{version}/books",
    tags=['books']
    )