from sqlalchemy import Column, Integer, String
from passlib.context import CryptContext
from core.database import Base, engine, SessionLocal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

Base.metadata.create_all(bind=engine)

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

def register_user(username, password):
    db = SessionLocal()
    if db.query(User).filter(User.username == username).first():
        db.close()
        return False

    new_user = User(username=username, password=hash_password(password))
    db.add(new_user)
    db.commit()
    db.close()
    return True

def login_user(username, password):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()

    if not user:
        return False

    return verify_password(password, user.password)
