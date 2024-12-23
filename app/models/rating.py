from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, Text, Date
from sqlalchemy.orm import relationship
from app.models import *


class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True, index=True)
    grade = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    is_active = Column(Boolean, default=True)

    user = relationship('User', back_populates='ratings')
    products = relationship('Product', back_populates='ratings')
    reviews = relationship("Review", back_populates="ratings")