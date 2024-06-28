from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from database import ENGINE, Session
from models import Team, User
from fastapi.encoders import jsonable_encoder
from schemas import TeamModel

team_router = APIRouter(prefix="/team")
session = Session(bind=ENGINE)

@team_router.get("/")
async def get_teams():
    teams = session.query(Team).all()
    context = [
        {
            "id": team.id,
            "first_name": team.first_name,
            "last_name": team.last_name,
            "position": team.position,
            "description": team.description
        }
        for team in teams
    ]
    return jsonable_encoder(context)


@team_router.post("/create")
async def create_team(team: TeamModel):
    existed_team = session.query(Team).filter(Team.id == team.id).first()
    if existed_team is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Team already exists")

    team_user = session.query(User).filter(User.id == team.user_id).first()
    if team_user:
        new_team = Team(
            id=team.id,
            first_name=team.first_name,
            last_name=team.last_name,
            position=team.position,
            description=team.description,
            user_id=team.user_id
        )
        session.add(new_team)
        session.commit()
        return jsonable_encoder({"status": "successfully created"})
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")

@team_router.put("/{id}")
async def update_team(id: int, team: TeamModel):
    existed_team = session.query(Team).filter(Team.id == id).first()
    if existed_team:
        for key, value in team.dict(exclude_unset=True).items():
            setattr(existed_team, key, value)
        session.commit()
        data = {
            "code": 200,
            "message": "Team updated successfully",
        }
        return jsonable_encoder(data)
    return jsonable_encoder({"code": 404, "message": "Team's id not found."})

@team_router.delete("/{id}")
async def delete_team(id: int):
    existed_team = session.query(Team).filter(Team.id == id).first()
    if existed_team:
        session.delete(existed_team)
        session.commit()
        return jsonable_encoder({"code": 200, "message": "Team deleted successfully."})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
