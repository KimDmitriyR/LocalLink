from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.services.chat import chat_manager

app = FastAPI(
    title = "LoaclLink",
    description = "Локальный обмен файлами и сообщениями",
    version = "0.3.0"
)

templates = Jinja2Templates(
    directory="app/templates"
)

#монтаж папки
#app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.get("/api/health")
async def health():
    return{
        "status" : "ok",
        "application" : "LocalLink",
        "version" : "0.3.0"
    }
        
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await chat_manager.connect(websocket)

    username = "Неизвестый пользователь"

    try:
        while True:
            data = await websocket.receive_json()
            message_type = data.get("type")

            if message_type == "join":
                username = str(
                    data.get("username", "")
                ).strip()

                if not username:
                    username = "Гость"

                username = username[:30]

                await chat_manager.broadcast({
                    "message": f"{username} подключиься к чату"
                })
            elif message_type == "message":
                message = str(
                    data.get("message", "")
                ).strip()

                if not message:
                    continue

                message = message[:1000]
                await chat_manager.broadcast({
                    "message": f"{username}: {message}"
                })

    except WebSocketDisconnect:
        chat_manager.disconnect(websocket)
        await chat_manager.broadcast({
            "message": f"{username} покинул чат"
        })