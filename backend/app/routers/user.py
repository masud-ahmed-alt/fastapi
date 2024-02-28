from fastapi import Depends,status,HTTPException, APIRouter
from sqlalchemy.orm import Session 
from .. import models,schemas, utils
from .. database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

#Create User
@router.post('/create', 
          status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,
                db: Session = Depends(get_db)):
    
    #hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    try:
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=str(e))


#Get Single User
@router.get('/{id}', 
          status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,  
                            detail=f"User with id: {id} not found.")
    return user