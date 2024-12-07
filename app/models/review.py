from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, Text, Date
from sqlalchemy.orm import relationship
from datetime import date
from app.models import *


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'), nullable=True)
    rating_id = Column(Integer, ForeignKey('ratings.id'))
    comment = Column(Text)
    comment_date = Column(Date, default=date.today())
    is_active = Column(Boolean, default=True)

    user = relationship('User', back_populates='reviews')
    product = relationship("Product", back_populates="reviews")
    ratings = relationship("Rating", back_populates="reviews")

