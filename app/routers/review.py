from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.db_depends import get_db
from app.schemas import CreateReview
from app.models.review import Review
from app.models.rating import Rating
from app.models.products import Product
from app.routers.auth import get_current_user


router = APIRouter(prefix='/reviews', tags=['/reviews'])


@router.get('/')
async def all_reviews(db: Annotated[AsyncSession, Depends(get_db)]):
    reviews = await db.scalars(select(Review).where(Review.is_active == True))
    ratings = await db.scalars(select(Rating).where(Rating.is_active == True))

    if not reviews.all() and not ratings.all():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no reviews or ratings'
        )
    return {
        'reviews': reviews.all(),
        'ratings': ratings.all()
    }


@router.get('/{product_id}')
async def products_reviews(db: Annotated[AsyncSession, Depends(get_db)], product_id: int):
    reviews = await db.scalar(select(Review).where(Review.is_active == True, Review.product_id == product_id))
    ratings = await db.scalar(select(Rating).where(Rating.is_active == True, Rating.product_id == product_id))

    if not reviews and not ratings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no reviews or ratings'
        )
    return {
        'reviews': reviews,
        'ratings': ratings
    }


@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_review(db: Annotated[AsyncSession, Depends(get_db)], get_user: Annotated[dict, Depends(get_current_user)],
                    create_review: CreateReview):
    if not get_user.get('is_customer'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You are not authorized to use this method'
        )
    product = await db.scalar(select(Product).where(Product.id == create_review.product_id))
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no product'
        )
    await db.execute(insert(Rating).values(
        grade=create_review.grade,
        user_id=get_user.get('user_id'),
        product_id=create_review.product_id
    ))
    await db.commit()
    last_rating = await db.scalar(select(Rating).order_by(Rating.id.desc()))
    await db.execute(insert(Review).values(
        user_id=get_user.get('user_id'),
        product_id=create_review.product_id,
        rating_id=last_rating.id,
        comment=create_review.comment
    ))
    await db.commit()
    old_rating = await db.scalars(select(Product.rating).where(Product.id == create_review.product_id))
    all_rating = [last_rating.grade] + [x for x in old_rating.all()]
    avg_rating = sum(all_rating) / (len(all_rating) - 1)
    await db.execute(update(Product).where(Product.id == create_review.product_id).values(rating=avg_rating))
    await db.commit()
    return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
        }


@router.delete('/{product_id}')
async def delete_reviews(db: Annotated[AsyncSession, Depends(get_db)],
                         get_user: Annotated[dict, Depends(get_current_user)], product_id: int):
    if not get_user.get('is_admin'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You are not authorized to use this method'
        )
    review_to_del = await db.scalar(select(Product).where(Product.id == product_id))
    if not review_to_del:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no product'
        )
    await db.execute(update(Review).where(Review.product_id == product_id).values(is_active=False))
    await db.execute(update(Rating).where(Rating.product_id == product_id).values(is_active=False))
    await db.commit()
    return {
                'status_code': status.HTTP_200_OK,
                'transaction': 'Reviews delete is successful'
    }
