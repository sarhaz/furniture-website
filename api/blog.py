from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from database import ENGINE, Session
from models import Blog
from schemas import BlogModel
blog_router = APIRouter(prefix="/blog")

session = Session(bind=ENGINE)


@blog_router.get("/")
async def get_all_categories():
    blogs = session.query(Blog).all()
    context = [
        {
            "id": blog.id,
            "title": blog.title,
            "author": blog.author,
            "created_at": blog.created_at,
        }
        for blog in blogs
    ]

    return jsonable_encoder(context)


@blog_router.post("/create")
async def create_category(blog: BlogModel):

    check_blog = session.query(Blog).filter(Blog.id == blog.id).first()
    if check_blog:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Blog already exists")

    new_blog = Blog(
        id=blog.id,
        title=blog.title,
        author=blog.author,
        comments_id=blog.comments_id,
        created_at=blog.created_at,
    )

    session.add(new_blog)
    session.commit()
    return jsonable_encoder({"status": "successfully created"})


@blog_router.put("/{id}")
async def update_category(id: int, blog: BlogModel):

    existed_blog_id = session.query(Blog).filter(Blog.id == id).first()
    if existed_blog_id:
        for key, value in blog.dict(exclude_unset=True).items():
            setattr(existed_blog_id, key, value)
        session.commit()
        return jsonable_encoder({"code": 200, "message": "Blog updated successfully"})
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Blog does not exist")


@blog_router.delete("/{id}")
async def delete_category(id: int):

    existed_blog_id = session.query(Blog).filter(Blog.id == id).first()
    if existed_blog_id:
        session.delete(existed_blog_id)
        session.commit()
        return jsonable_encoder({"code": 200, "message": "Blog deleted successfully"})

