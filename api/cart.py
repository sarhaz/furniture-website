from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from database import ENGINE, Session
from models import Cart, User, Product
from schemas import CartModel, UserOrderModel
cart_router = APIRouter(prefix="/cart")

session = Session(bind=ENGINE)


@cart_router.get("/")
async def get_orders():
    products = session.query(Product).all()
    context = [
        {
            "id": product.id,
            "user": {
                "id": product.user.id,
                "first_name": product.user.first_name,
                "last_name": product.user.last_name,
                "username": product.user.username,
                "email": product.user.email,
                "is_active": product.user.is_active,
                "is_staff": product.user.is_staff,
            },
            "product": {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "price_type": product.price_type,
                "description": product.description,
                },
        }
        for product in products
    ]
    return jsonable_encoder(context)


@cart_router.post("/create")
async def create_order(cart: CartModel):
    check_order = session.query(Cart).filter(Cart.id == cart.id).first()
    check_user = session.query(User).filter(User.id == cart.user_id).first()
    check_product = session.query(Product).filter(Product.id == cart.product_id).first()
    if check_order:
        raise HTTPException(status_code=status.HTTP_201_CREATED, detail="Order already exists")
    if not check_product and not check_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product or User id not found")

    new_order = Cart(
        id=cart.id,
        user_id=cart.user_id,
        product_id=cart.product_id,
    )
    session.add(new_order)
    session.commit()
    data = {
        "created": "successfully created",
        "id": new_order.id,
        "user": {
            "id": check_user.id,
            "first_name": check_user.first_name,
            "last_name": check_user.last_name,
            "username": check_user.username,
            "email": check_user.email,
            "is_active": check_user.is_active,
            "is_staff": check_user.is_staff,
        },
        "product": {
            "id": check_product.id,
            "name": check_product.name,
            "price": check_product.price,
            "price_type": check_product.price_type,
            "description": check_product.description,
        }
    }
    return jsonable_encoder(data)


@cart_router.put("/{id}")
async def update_order(id: int, cart: CartModel):
    existed_order = session.query(Cart).filter(Cart.id == id).first()
    existed_user_id = session.query(User).filter(User.id == cart.id).first()
    existed_product_id = session.query(Product).filter(Product.id == cart.id).first()
    if existed_order is None:
        if existed_user_id and existed_product_id:
            for key, value in cart.dict(exclude_unset=True).items():
                setattr(existed_order, key, value)
            session.commit()
            return jsonable_encoder({"message": "cart updated"})
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User's id or product's id does not exist")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cart not found")


@cart_router.delete("/{id}")
async def delete_order(id: int):
    existed_order = session.query(Cart).filter(Cart.id == id).first()
    if existed_order:
        session.delete(existed_order)
        session.commit()
        return jsonable_encoder({"message": "Order deleted"})


@cart_router.get("/{id}")
async def get_order(id: int):
    existed_order = session.query(Cart).filter(Cart.id == id).first()
    if existed_order:
        data = {
            "id": existed_order.id,
            "user": {
                "id": existed_order.user.id,
                "first_name": existed_order.user.first_name,
                "last_name": existed_order.user.last_name,
                "username": existed_order.user.username,
                "email": existed_order.user.email,
                "is_active": existed_order.user.is_active,
                "is_staff": existed_order.user.is_staff,
            },
            "product": {
                "id": existed_order.id,
                "name": existed_order.name,
                "price": existed_order.price,
                "price_type": existed_order.price_type,
                "description": existed_order.description,
            },
            "count": existed_order.count,
            "status": existed_order.status
        }
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")


@cart_router.get("/user/order")
async def users_order(user_order: UserOrderModel):
    check_username = session.query(User).filter(User.username == user_order.username).first()
    if not check_username:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username does not exist")
    check_order = session.query(Cart).filter(Cart.user_id == check_username.id)
    if not check_order:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User's order does not exist")
    data = [
        {
            "id": order.id,
            "count": order.count,
            "status": order.status,
            "total_cost": order.product.price * order.count,
            "cost_with_promo_code": order.product.price * order.count,
            "user": {
                "id": order.id,
                "first_name": order.user.first_name,
                "last_name": order.user.last_name,
                "username": order.user.username,
                "email": order.user.email,
                "is_active": order.user.is_active,
                "is_staff": order.user.is_staff,
            },
            "product": {
                "id": order.product.id,
                "name": order.product.name,
                "price": order.product.price,
                "count": order.product.count,
                "category_id": order.product.category_id,
            }
        }
        for order in check_order
    ]
    return jsonable_encoder(data)
