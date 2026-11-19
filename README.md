# MemeGallery API

A backend-first media upload and delivery service built to learn how APIs, authentication, databases, and file storage work together.

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| **Framework** | FastAPI | Async Python web framework that auto-generates OpenAPI docs and handles request validation through type hints |
| **Server** | Uvicorn | ASGI server that actually runs the FastAPI app and listens for HTTP requests on a port |
| **Database** | SQLite + aiosqlite | Lightweight file-based DB (`test.db`) with an async driver so DB calls don't block the server |
| **ORM** | SQLAlchemy (async) | Maps Python classes to database tables — write Python, not SQL |
| **Auth** | fastapi-users + JWT | Handles registration, login, password reset, and token-based sessions out of the box |
| **File Storage** | ImageKit (v5 SDK) | Cloud media storage and CDN — files upload via the SDK and come back as public URLs |
| **Config** | python-dotenv | Loads secrets from a `.env` file so they stay out of source code |
| **Package Manager** | uv | Fast Python package manager — `pyproject.toml` defines deps, `uv.lock` pins them |

## How the API is Built

### FastAPI basics

FastAPI is a **Python web framework** — it takes HTTP requests and routes them to Python functions. The core idea:

```python
app = FastAPI()

@app.get("/feed")       # decorator binds this function to GET /feed
async def get_feed():   # async so the server can handle many requests at once
    ...
    return {"posts": posts_data}  # returns JSON automatically
```

The `@app.get`, `@app.post`, `@app.delete` decorators are what make a function an **API endpoint**. The decorator says *which HTTP method* and *which URL path* triggers the function.

### Request → Response lifecycle

```
Client sends HTTP request
        ↓
Uvicorn receives it on port 8000
        ↓
FastAPI matches the URL + method to a decorated function
        ↓
Dependency injection resolves parameters (DB session, current user, etc.)
        ↓
Your function runs and returns data
        ↓
FastAPI serializes it to JSON and sends the HTTP response
```

### Dependency injection with `Depends()`

Instead of manually creating database sessions or checking auth in every endpoint, FastAPI injects them:

```python
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),              # from the request body (multipart form)
    caption: str = Form(""),                   # from a form field
    user: User = Depends(current_active_user), # injected — checks JWT, returns User or 401
    session: AsyncSession = Depends(get_async_session),  # injected — yields a DB session
):
```

`Depends()` calls the function you give it and passes the result as the parameter. This is how auth, database access, and other shared logic stay out of your endpoint code.

### Routers and `include_router`

Instead of defining every route on the `app` object, routes can live in separate **routers** and get mounted:

```python
from app.frontend import router as frontend_router
app.include_router(frontend_router)  # all routes from frontend.py are now live

# fastapi-users generates auth routes automatically:
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",  # all routes in this router start with /auth/jwt
)
```

This is how the app has `/auth/jwt/login`, `/auth/register`, etc. without writing those endpoints by hand — `fastapi-users` generates them and you mount them with a prefix.

### Database layer (SQLAlchemy ORM)

Models are Python classes that map to database tables:

```python
class Post(Base):
    __tablename__ = "posts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    caption = Column(Text)
    url = Column(String, nullable=False)
    ...
```

The ORM translates Python operations into SQL:
- `session.add(post)` → `INSERT INTO posts ...`
- `session.execute(select(Post))` → `SELECT * FROM posts`
- `session.delete(post)` → `DELETE FROM posts WHERE ...`
- `session.commit()` → actually writes the changes to the DB file

The session is created via an **async generator** (`yield`) so it's automatically opened before and closed after each request.

### Authentication (JWT)

The auth flow uses JSON Web Tokens:

1. **Register** → `POST /auth/register` — hashes password, stores user in DB
2. **Login** → `POST /auth/jwt/login` — verifies credentials, returns a signed JWT
3. **Authenticated requests** → client sends `Authorization: Bearer <token>` header
4. **Verification** → `Depends(current_active_user)` decodes the JWT using the server's secret key, looks up the user, and either returns the User object or rejects the request with 401

The JWT is signed with HMAC-SHA256 — the server's secret key creates the signature. You can read the payload (it's just base64), but you can't forge a valid signature without the secret.

### File upload flow

```
Client sends file (multipart form)
        ↓
FastAPI parses it into an UploadFile object
        ↓
File is written to a temp file on disk (tempfile)
        ↓
Temp file is opened and sent to ImageKit's SDK
        ↓
ImageKit returns a URL for the hosted file
        ↓
A Post record (URL, caption, file type) is saved to the DB
        ↓
Temp file is deleted in a finally block
```

## Project Structure

```
├── main.py              # entry point — runs uvicorn
├── app/
│   ├── app.py           # FastAPI app, all route definitions
│   ├── db.py            # SQLAlchemy models, engine, session factory
│   ├── schemas.py       # Pydantic models for request/response validation
│   ├── users.py         # fastapi-users config (auth backend, user manager)
│   ├── images.py        # ImageKit SDK setup
│   └── frontend.py      # serves the HTML frontend at /
├── pyproject.toml       # dependencies and project metadata
├── uv.lock              # pinned dependency versions
├── .env                 # secrets (IMAGEKIT_PRIVATE_KEY) — not committed
└── test.db              # SQLite database file — auto-created on first run
```

## Running

```bash
uv run python main.py
# → server starts at http://localhost:8000
# → API docs at http://localhost:8000/docs (auto-generated by FastAPI)
```
