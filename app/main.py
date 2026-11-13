from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI(
    title = "LoaclLink",
    description = "Локальный обмен файлами и сообщениями",
    version = "0.1.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home():
    return"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">
        <title>LocalLink</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 650px;
                margin: 60px auto;
                padding: 20px;
                background: #f3f6fa;
                color: #172033;
            }
            .card {
                background: white;
                padding: 28px;
                border-radius: 16px;
                box-shadow: 0 4px 20px #00000010;
            }
            .status {
                color: #16834a;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Вроде работает</h1>
        </div>
    </body>
    </html>
    """
@app.get("/api/health")
async def health():
    return{
        "status" : "ok",
        "application" : "LocalLink",
        "version" : "0.1.0"
    }
        

