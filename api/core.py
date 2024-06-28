from fastapi import FastAPI
from auth import auth_router
from blog import blog_router
from cart import cart_router
from product import product_router
from team import team_router
from comments import comments_router


app = FastAPI()
app.include_router(auth_router)
app.include_router(blog_router)
app.include_router(cart_router)
app.include_router(comments_router)
app.include_router(product_router)
app.include_router(team_router)


@app.get("/")
async def landing():
    return {
        "msg": "Hello World!"
    }


@app.get("/user")
async def user():
    return {
        "msg": "it is user's page"
    }


@app.get("/user/{id}")
async def user(id: int):
    return {
        "msg": f"user-id is {id}"
    }
