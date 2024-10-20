from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class ArticleCreate(BaseModel):
    title: str
    link: str
    content: str
    tags: list

class ArticleUpdate(BaseModel):
    tags: str