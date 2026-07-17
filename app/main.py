from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi import WebSocket, WebSocketDisconnect
from app.websockets import manager
from app.errors import AppError

from app.api import root_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(debug=True)


@app.websocket("/api/ws/{user_id}")
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
    except Exception as e:
        print(f"WS error for user {user_id}: {e}")
        manager.disconnect(user_id, websocket)


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# load_dotenv()
# @app.on_event("startup")
# async def startup_event():
#     # Создать таблицы, если их нет
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     print("Tables created successfully")


app.include_router(root_router)
