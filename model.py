from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    name = Column(String)
    password = Column(String)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key = True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    seller_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    buyer_id = Column(Integer)
    owner = relationship("User")

# class Wishlist(Base):
#     __tablename__ = "wishlists"

#     product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
#     buyer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

