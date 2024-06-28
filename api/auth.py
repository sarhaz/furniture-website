from fastapi import HTTPException, Depends, APIRouter, status
from fastapi.encoders import jsonable_encoder
from database import ENGINE, Session
from models import User
from schemas import RegisterModel, LoginModel
from werkzeug import security

session = Session(bind=ENGINE)
auth_router = APIRouter(prefix="/auth")


@auth_router.get("/users")
async def users_list():
    users = session.query(User).all()
    context = [
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "username": user.username,
            "is_staff": user.is_staff,
            "is_active": user.is_active
        }
        for user in users
    ]
    return jsonable_encoder(context)


@auth_router.get('/login')
async def login():
    return {
        'status': 'it is login page',
    }


@auth_router.post('/login')
async def login(user: LoginModel):
    username = session.query(User).filter(User.username == user.username).first()
    if username is None:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Username does not exists")

    user_check = session.query(User).filter(User.username == user.username).first()
    if security.check_password_hash(user_check.password, user.password):
        return HTTPException(status_code=status.HTTP_200_OK, detail=f"Login successful")

    return HTTPException(status_code=status.HTTP_404_SERVICE_UNAVAILABLE, detail=f"Incorrect username or password",)


@auth_router.get('/register')
async def register():
    return {
        'status': 'it is register page',
    }


@auth_router.post('/register')
async def register(user: RegisterModel):
    username = session.query(User).filter(User.username == user.username).first()
    if username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username already exists')

    email = session.query(User).filter(User.email == user.email).first()
    if email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists')

    new_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        password=security.generate_password_hash(user.password),
        id=user.id,
        email=user.email,
        is_staff=user.is_staff,
        is_active=user.is_active,
    )
    session.add(new_user)
    session.commit()
    return jsonable_encoder({"status": "successfully registered"})


@auth_router.get('/logout')
async def logout():
    return {
        'status': 'success',
    }


@auth_router.put('/{id}')
async def update_user(id: int, user: RegisterModel):

    existing_user = session.query(User).filter(User.id == id).first()
    if existing_user:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(existing_user, key, value)
        session.commit()
        data = {
            'code': 200,
            'status': 'success',
        }
        return jsonable_encoder(data)
    return jsonable_encoder({"code": 404, "message": "User not found."})


@auth_router.delete('/{id}')
async def update_user(id: int):

    existed_user = session.query(User).filter(User.id == id).first()
    if existed_user:
        session.delete(existed_user)
        session.commit()
        return HTTPException(status_code=status.HTTP_200_OK, detail=f"User {id} has been deleted!")
