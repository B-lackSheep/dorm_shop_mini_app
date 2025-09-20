import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from telegram_bot import start_bot_polling


@asynccontextmanager
async def lifespan(app: FastAPI):
    threading.Thread(target=start_bot_polling, daemon=True).start()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root_get():
    return JSONResponse({"message": "Bot is running"})


@app.head("/")
async def root_head():
    return Response(status_code=200)
