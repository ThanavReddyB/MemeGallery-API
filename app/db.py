# orm -> object relational mapping
from collections.abc import AsyncGenerator
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column,String,Text,DateTime,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from fastapi_users.db import SQLAlchemyUserDatabase,SQLAlchemyBaseUserTableUUID
from fastapi import Depends
DATABASE_URL = "sqlite+aiosqlite:///./test.db" #aiosqlite is asynchronous sqlite , test.db is local db 


class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTableUUID,Base):
    posts = relationship(argument="Post",back_populates="user")



#data models , type of data we want to store (specify structure)
class Post(Base):
    __tablename__ = "posts"
    #as_uuid helps store it in form of a uuid , primary key true makes it unique ,default generates a random uuid automatically
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True),ForeignKey("user.id"),nullable=False)
    caption = Column(Text)
    url = Column(String,nullable=False)
    file_type = Column(String,nullable=False)
    file_name = Column(String,nullable=False)
    Created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship(argument="User",back_populates="posts")

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine,expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        # inherit all classes inheriting declarative class and creates them in database
        await conn.run_sync(Base.metadata.create_all)


# get a session that lets use write and read to the database
async def get_async_session() -> AsyncGenerator[AsyncSession,None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session,User)