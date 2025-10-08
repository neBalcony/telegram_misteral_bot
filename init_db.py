from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from config import settings
from models import Base, User


def init_db():
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        admin_id = settings.ADMIN_ID
        user = session.execute(select(User).where(User.id == admin_id)).scalars().first()
        if not user:
            user = User( id=admin_id, role="admin")
            session.add(user)
            session.commit()
            
if __name__ == "__main__":
    init_db()