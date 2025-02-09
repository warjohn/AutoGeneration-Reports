import uvicorn
import pkg_resources
import os

from starlette.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, Form, File, Depends, HTTPException, status, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from .database.database import Database

TMP_FOLDER = ".tmp"
app = FastAPI()
db = Database()

static_path = pkg_resources.resource_filename('reportGeneration', 'web/static')
app.mount("/static", StaticFiles(directory=static_path), name="static")

templates_path = pkg_resources.resource_filename('reportGeneration', 'web/templates')
templates = Jinja2Templates(directory=templates_path)



@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    response = templates.TemplateResponse("login.html", {"request": request})
    return response

@app.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/login")
    response.delete_cookie("user")
    return response

@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    file_names = []
    os.mkdir(TMP_FOLDER)
    for file in files:
        file_path = os.path.join(TMP_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        file_names.append(file.filename)
    return templates.TemplateResponse("index.html", {"request": Request, "user": "User", "files": file_names})


@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), action: str = Form(...)):
    if action == "signin":
        user = db.get_user_by_username(username)
        if user is None or user[2] != password:  # user[2] — это поле с паролем
            # При неверном логине или пароле перенаправляем с ошибкой
            return RedirectResponse(url="/login?error=Неверный логин или пароль", status_code=status.HTTP_302_FOUND)
        # Если логин и пароль правильные, перенаправляем на главную страницу
        response = RedirectResponse(url="/", status_code=status.HTTP_200_OK)
        response.set_cookie(key="user", value=username)
        return response

    elif action == "signup":
        user = db.get_user_by_username(username)
        if user:
            raise HTTPException(status_code=400, detail="Пользователь уже существует")
        db.add_user(username, password)  # Добавляем пользователя в базу данных
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="user", value=username)
        return response
    else:
        raise HTTPException(status_code=400, detail="Неизвестная операция")

@app.get("/")
async def home(request: Request):
    user = request.cookies.get("user")
    if user is None:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


def run_server(host="127.0.0.1", port=8000):
    uvicorn.run(app, host=host, port=port)
