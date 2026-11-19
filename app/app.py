from fastapi import FastAPI , HTTPException , File , UploadFile, Form, Depends 
from app.schemas import PostCreate,PostResponse,UserRead,UserCreate,UserUpdate

from app.db import Post,create_db_and_tables,get_async_session,User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from app.images import ImageKit
from app.users import auth_backend,current_active_user,fastapi_users
import os
import shutil
import uuid
import tempfile

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

from app.frontend import router as frontend_router
app.include_router(frontend_router)

app.include_router(fastapi_users.get_auth_router(auth_backend),prefix='/auth/jwt',tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead,UserCreate),prefix='/auth',tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(),prefix='/auth',tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead),prefix='/auth',tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead,UserUpdate),prefix='/auth',tags=["auth"])


#we do app.method("/endpoint")
# @app.get("/hello-world") #decorator is used
# def hello_world():
#     return {"message" : "Hello  world"} #JSON --> javascript object notation

# text_posts = {
#     1: {"title": "I Built a SaaS in 7 Days and Made $2,000", "content": "I challenged myself to build and ship a complete SaaS product in just one week using FastAPI, React, and Stripe. Here's how it went, what broke, and how much money it made on launch day."},
#     2: {"title": "Why Every Developer Should Learn SQL Before ORMs", "content": "ORMs are great, but if you don't understand raw SQL you're going to hit a wall. I walk through 5 real production bugs I encountered that were impossible to debug without knowing what queries were actually running."},
#     3: {"title": "I Cold Emailed 1000 CEOs on LinkedIn — Here's What Happened", "content": "Using a Python bot and some clever prompt engineering, I sent personalized outreach messages to 1000 startup CEOs. 73 replied, 12 booked calls, and 3 became paying clients. Full breakdown inside."},
#     4: {"title": "The Tech Stack Nobody Talks About", "content": "Everyone's using Next.js and Vercel but I switched my entire startup to FastAPI + HTMX and my server costs dropped 90%. No build step, no JavaScript fatigue, just pure productivity."},
#     5: {"title": "How I Processed 500 Million Rows in 24 Hours Using Python", "content": "I tackled a dataset with over 500 million rows of e-commerce transactions to find purchasing patterns. Used Pandas, DuckDB, and some clever chunking strategies. The results were wild."},
#     6: {"title": "Stop Using .env Files Wrong — 5 Mistakes Developers Make", "content": "Most tutorials teach you to use .env files but never explain the security pitfalls. I cover the 5 most common mistakes including committing secrets, not validating variables, and ignoring rotation."},
#     7: {"title": "I Built a Chat App With Just Python — No JavaScript", "content": "Built a full real-time chat app using FastAPI for the backend, WebSockets for messaging, and Redis for pub/sub. Deployed it on a $5 VPS and it handles 10k concurrent users."},
#     8: {"title": "Docker in 10 Minutes — Everything You Need to Know", "content": "I break down Docker containers, images, volumes, and docker-compose in the simplest way possible. By the end of this post you'll be able to containerize any Python app and deploy it anywhere."},
#     9: {"title": "Why Junior Developers Should Stop Grinding LeetCode", "content": "Hot take: LeetCode is not the best use of your time if you're trying to get hired. Here's a breakdown of what actually got me and 15 other devs our first jobs — and it wasn't inverting binary trees."},
#     10: {"title": "Building a REST API From Scratch — No Framework", "content": "Ever wondered what FastAPI does under the hood? I built a REST API using nothing but Python's built-in socket library and the ASGI spec. It was painful, enlightening, and made me truly appreciate frameworks."},
# }

# @app.get("/posts")
# def get_all_posts(limit: int): #type hinting to trigger errors for any other data type
#     if limit:
#         return list(text_posts.values())[:limit]
#     return text_posts

# @app.get("/posts/{id}")
# # id: int maps the id value inside the path parameter in decorator
# def get_posts(id: int):
#     if id not in text_posts:
#         raise HTTPException(status_code=404,detail="Post not found")
#     return text_posts.get(id)


# @app.post('/posts')
# def create_post(post: PostCreate):
#     # since we have defined the types in schemas , it makes sure only strings are passed and no other data type in this case'
#     new_post = {"title": post.title, "content":post.content}
#     text_posts[max(text_posts.keys()) + 1] = {"title": post.title, "content":post.content} 
#     return new_post


@app.post('/upload')
async def upload_file(file: UploadFile = File(...),
                     caption: str = Form(""),
                     user: User = Depends(current_active_user),
                      session: AsyncSession = Depends(get_async_session) ):

    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False,suffix =
                                     os.path.splitext(file.filename or "")[1],) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file,temp_file)


        with open(temp_file_path, "rb") as f:
            upload_result = ImageKit.files.upload(
                file=f,
                file_name=file.filename or "upload",
                use_unique_file_name=True,
                tags=["backend-upload"],
            )

        post = Post(
            user_id=user.id,
            caption=caption,
            url=upload_result.url,
            file_type="video" if (file.content_type or "").startswith("video/") else "image",
            file_name=upload_result.name,
        )
        session.add(post)
        await session.commit()
        await session.refresh(post)
        return post
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()




@app.get('/feed')
async def get_feed(session: AsyncSession = Depends(get_async_session),
                   user: User = Depends(current_active_user),
):
    result = await session.execute(select(Post).order_by(Post.Created_at.desc()))
    posts = [row[0] for row in result.all()]

    result = await session.execute(select(User))
    users = [row[0] for row in result.all()]
    user_dict = {u.id:u.email for u in users}

    posts_data = []
    for post in posts:
        posts_data.append({
            "user_id":str(post.user_id),
            "id": str(post.id),
            "caption": post.caption,
            "url": post.url,
            "file_type": post.file_type,
            "file_name": post.file_name,
            "created_at": post.Created_at,
            "is_owner": post.user_id == user.id,
            "email": user_dict.get(post.user_id)
        })
    return {"posts":posts_data}



@app.delete('/posts/{post_id}')
async def delete_post(post_id:str,
                      user: User = Depends(current_active_user),
                      session: AsyncSession = Depends(get_async_session)):
    try:
        post_uuid = uuid.UUID(post_id)
        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first()

        if not post:
            raise HTTPException(status_code=404,detail="Post not found")

        if str(post.user_id) != str(user.id):
            raise HTTPException(status_code=403,detail="Unauthorized")

        await session.delete(post)
        await session.commit()

        return {"success": True, "message": "Post deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
        