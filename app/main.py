import subprocess

from fastapi import FastAPI, Depends, status
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


# ⚠️ ثغرة 1: Shell Injection (B602 - High)
@app.get("/ping-host")
def ping_host(host: str):
    result = subprocess.run(
        f"ping -c 1 {host}", shell=True, capture_output=True, text=True
    )
    return {"output": result.stdout}


# ⚠️ ثغرة 2: استخدام eval() لتنفيذ كود عشوائي (B307 - Medium)
@app.get("/calculate")
def calculate(expression: str):
    result = eval(expression)
    return {"expression": expression, "result": result}
