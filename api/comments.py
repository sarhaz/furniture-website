from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from database import ENGINE, Session
from models import Comments, User
from fastapi.encoders import jsonable_encoder
from schemas import CommentModel

comments_router = APIRouter(prefix="/comments")
session = Session(bind=ENGINE)

@comments_router.get("/")
async def get_comments():
    comments = session.query(Comments).all()
    context = [
        {
            "id": comment.id,
            "text": comment.text,
            "user": {
                "id": comment.user.id,
                "first_name": comment.user.first_name,
                "last_name": comment.user.last_name,
                "username": comment.user.username,
                "email": comment.user.email,
                "is_active": comment.user.is_active,
                "is_staff": comment.user.is_staff,
            }
        }
        for comment in comments
    ]
    return jsonable_encoder(context)

@comments_router.post("/create")
async def create_comment(comment: CommentModel):
    existed_comment = session.query(Comments).filter(Comments.id == comment.id).first()
    if existed_comment is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Comment already exists")

    comment_user = session.query(User).filter(User.id == comment.user_id).first()
    if comment_user:
        new_comment = Comments(
            id=comment.id,
            text=comment.text,
            user_id=comment.user_id
        )
        session.add(new_comment)
        session.commit()
        return jsonable_encoder({"status": "successfully created"})
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")

@comments_router.put("/{id}")
async def update_comment(id: int, comment: CommentModel):
    existed_comment = session.query(Comments).filter(Comments.id == id).first()
    if existed_comment:
        for key, value in comment.dict(exclude_unset=True).items():
            setattr(existed_comment, key, value)
        session.commit()
        data = {
            "code": 200,
            "message": "Comment updated successfully",
        }
        return jsonable_encoder(data)
    return jsonable_encoder({"code": 404, "message": "Comment's id not found."})

@comments_router.delete("/{id}")
async def delete_comment(id: int):
    existed_comment = session.query(Comments).filter(Comments.id == id).first()
    if existed_comment:
        session.delete(existed_comment)
        session.commit()
        return jsonable_encoder({"code": 200, "message": "Comment deleted successfully."})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
