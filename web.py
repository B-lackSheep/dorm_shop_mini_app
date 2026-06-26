import os
import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from telegram_bot import start_bot_polling


@asynccontextmanager
async def lifespan(app: FastAPI):
    threading.Thread(target=start_bot_polling, daemon=True).start()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from endpoints.category import router as category_router
from endpoints.order import router as order_router

app.include_router(category_router)
app.include_router(order_router)


@app.get("/")
async def root_get():
    return JSONResponse({"message": "Bot is running"})


@app.head("/")
async def root_head():
    return Response(status_code=200)
