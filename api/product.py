from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from database import ENGINE, Session
from models import Product, User
from fastapi.encoders import jsonable_encoder
from schemas import ProductModel


product_router = APIRouter(prefix="/product")

session = Session(bind=ENGINE)


@product_router.get("/")
async def get_products():
    products = session.query(Product).all()
    context = [
        {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "price_type": product.price_type,
            "description": product.description,
            "user": {
                "id": product.user.id,
                "first_name": product.user.first_name,
                "last_name": product.user.last_name,
                "username": product.user.username,
                "email": product.user.email,
                "is_active": product.user.is_active,
                "is_staff": product.user.is_staff,

            }

        }
        for product in products
    ]
    return jsonable_encoder(context)


@product_router.post("/create")
async def create_product(product: ProductModel):
    existed_product = session.query(Product).filter(Product.id == product.id).first()
    if existed_product is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product already exists")

    product_user_id = session.query(User).filter(User.id == product.category_id).first()
    if product_user_id:
        new_product = Product(
            id=product.id,
            name=product.name,
            price_type=product.price_type,
            price=product.price,
            description=product.description
        )
        session.add(new_product)
        session.commit()
        return jsonable_encoder({"status": "successfully created"})
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")


@product_router.put("/{id}")
async def update_product(id: int, product: ProductModel):
    existed_product = session.query(Product).filter(Product.id == id).first()
    existed_user_id = session.query(User).filter(User.id == product.category_id).first()
    if existed_product and existed_user_id:
        for key, value in product.dict(exclude_unset=True).items():
            setattr(existed_product, key, value)
        session.commit()
        data = {
            "code": 200,
            "message": "Product updated successfully",
        }
        return jsonable_encoder(data)
    return jsonable_encoder({"code": 404, "message": "Product's id  or Category's id not found."})


@product_router.delete("/{id}")
async def delete_product(id: int):
    existed_product = session.query(Product).filter(Product.id == id).first()
    if existed_product:
        session.delete(existed_product)
        session.commit()
        return jsonable_encoder({"code": 200, "message": "Product deleted successfully."})
