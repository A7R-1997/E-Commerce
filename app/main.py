from sqlalchemy import text
from fastapi import FastAPI, Depends, status, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
from pydantic import BaseModel

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce Microservice API", version="2.0.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup_seed_users():
    db = SessionLocal()
    try:
        count = db.execute(text("SELECT COUNT(*) FROM public.users")).scalar()
        if count == 0:
            db.execute(text("""
                INSERT INTO public.users (username, email, hashed_password) VALUES
                ('admin', 'admin@site.com', '123'),
                ('ahmed', 'ahmed@site.com', '456'),
                ('mohamed', 'mohamed@site.com', '789')
            """))
            db.commit()
            print("تم إدخال المستخدمين التجريبيين في جدول users بنجاح!")
    except Exception as e:
        db.rollback()
        print(f"ملاحظة أو خطأ أثناء الإدخال التلقائي للمستخدمين: {e}")
    finally:
        db.close()


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int


@app.post("/products/", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = models.ProductModel(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.get("/products/")
def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(models.ProductModel).offset(skip).limit(limit).all()
    return products


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "e-commerce-api"}


@app.get("/users/search")
def search_users_unsafe(username: str, db: Session = Depends(get_db)):
    query = text(f"SELECT * FROM public.users WHERE username = '{username}'")
    result = db.execute(query).mappings().all()
    return {"users": result}


# @app.get("/calculate")
# def calculate(expression: str):
#     result = eval(expression)
#     return {"expression": expression, "result": result}