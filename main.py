from fastapi import Depends, FastAPI, Response, Request
from fastapi.security import OAuth2PasswordRequestForm

from fastapi.staticfiles import StaticFiles 
from fastapi.templating import Jinja2Templates 

from typing import List

from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse

from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

from model import Base, User, Product
from crud import db_register_user, db_add_product, db_del_product, db_get_product, db_search_product
from database import SessionLocal, engine
from schema import ProductSchema, UserSchema

from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

class NotAutentificated(Exception):
    pass

app=FastAPI()

templates = Jinja2Templates(directory="templates") 
app.mount("/static", StaticFiles(directory="static"), name="static") 

SECRET = "super-secret-key"
manager = LoginManager(SECRET, '/login', use_cookie=True, custom_exception = NotAutentificated)

@app.exception_handler(NotAutentificated)
def auth_exception_handler(request: Request, exc: NotAutentificated):
    return RedirectResponse(url='/login')

###특정 유저 불러오기###

@manager.user_loader
def get_user(username : str, db: Session = None):
    if not db:
        with SessionLocal() as db:
            return db.query(User).filter(User.name == username).first()
    return db.query(User).filter(User.name == username).first()

###메인###

@app.get("/" , response_class=HTMLResponse)
def get_root(req: Request):
    return templates.TemplateResponse("login.html",{"request": req})

###회원가입###

@app.post("/register")
def register_user(response: Response, data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    username = data.username
    password = data.password

    user = db_register_user(db, username, password)
    if user:
        access_token = manager.create_access_token(
            data={'sub': username}
        )
        manager.set_cookie(response, access_token)
        return "User created"
    else:
        return "Failed"
    
###로그인 페이지###

@app.get("/main")
def get_login(req: Request):
    return templates.TemplateResponse("main.html",{"request": req})

###로그인 기능###

@app.post("/token")
def login(response:Response, data:OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password

    user = get_user(username)

    if not user:
        raise InvalidCredentialsException
    if user.password != password:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data={'sub': username}
    )
    manager.set_cookie(response, access_token)
    return {'access_token': access_token}

###로그아웃###

@app.get("/logout")
def logout(response: Response):
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie(key="access-token")
    return response

###상품 등록###

@app.post("/add_product")
def add_product(product : ProductSchema, db: Session=Depends(get_db), user=Depends(manager)):
    result = db_add_product(db, user, product)
    if not result:
        return None
    return "success"

###상품 삭제###

@app.delete("/delete_product")
def delete_product(product : ProductSchema, db:Session=Depends(get_db), user=Depends(manager)):
    result = db_del_product(db, user, product)
    return

###모든 상품 불러오기###

@app.get("/get_product")
def get_product(db:Session=Depends(get_db)):
    return db_get_product(db, None)

###판매자 기준 상품 불러오기###

@app.get("/get_product_by_seller")
def get_product_by_seller(seller: int, db:Session=Depends(get_db)):
    return db_get_product(db, seller)

###상품 검색###

@app.post("/product_search", response_model=List[ProductSchema])    
def search_todo(product: ProductSchema, db: Session = Depends(get_db)):
    result = db_search_product(db, product)
    if not result:
        return []
    return result

###상품 상세페이지###

@app.get("/get_product_detail/", response_class=HTMLResponse)
def get_product_detail(id: int, req: Request):
    return templates.TemplateResponse("product_detail.html",{"request":req, "id":id})

