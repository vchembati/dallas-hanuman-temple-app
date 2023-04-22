from sqlalchemy import Column, Integer, String
from database import Base


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    product_price = Column(String)
    purchase_by_name = Column(String)
    purchase_date = Column(String)

class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    profile_name = Column(String)
    profile_picture_url = Column(String)
