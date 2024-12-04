from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from db.database import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST

Base = declarative_base()
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True)

def add_user(telegram_id):
    session = Session()
    try:
        if not session.query(User).filter_by(telegram_id=telegram_id).first():
            user = User(telegram_id=telegram_id)
            session.add(user)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        return False
    finally:
        session.close()
