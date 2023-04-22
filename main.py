from fastapi import FastAPI, Depends, HTTPException, UploadFile
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
import boto3

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Order(BaseModel):
    productName: str
    productPrice: str
    purchaseByName: str
    purchaseDate: str


class Profile(BaseModel):
    profileName: str


@app.get("/orders")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Orders).all()


@app.post("/order")
async def create_order(order: Order,
                      db: Session = Depends(get_db)):

    order_model = models.Orders()
    order_model.product_name = order.productName
    order_model.product_price = order.productPrice
    order_model.purchase_by_name = order.purchaseByName
    order_model.purchase_date = order.purchaseDate
    db.add(order_model)
    db.commit()

    return successful_response(201)


@app.get("/profile/{name}")
async def read_all(name: str,
                   db: Session = Depends(get_db)):
    profile_model = db.query(models.Profile)\
        .filter(models.Profile.profile_name.contains(name))\
        .first()
    if profile_model is not None:
        return profile_model
    raise http_exception()


@app.post("/profile")
async def create_profile(profilename: str,
                         file: UploadFile,
                         db: Session = Depends(get_db)):

    s3 = boto3.resource("s3")

    bucket = s3.Bucket("dallas-hanuman-s3")
    bucket.upload_fileobj(file.file, file.filename, ExtraArgs={"ACL": "public-read"})

    uploaded_file_url = "https://dallas-hanuman-s3.s3.amazonaws.com/{file.filename}"

    profile_model = models.Profile()
    profile_model.profile_name = profilename
    profile_model.profile_picture_url = uploaded_file_url
    db.add(profile_model)
    db.commit()

    return successful_response(201)


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }

def http_exception():
    return HTTPException(status_code=404, detail="Profile not found")


















