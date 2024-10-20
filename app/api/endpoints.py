from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import UserCreate, Token, ArticleCreate, ArticleUpdate
from app.models import User, SavedArticle
from app.auth import authenticate_user, create_access_token, get_current_user, get_password_hash
from app.api.utils import fetch_wikipedia_articles
import uuid
from typing import List
from fastapi import HTTPException


router = APIRouter()

@router.post("/register", response_model=Token)
async def register(user: UserCreate):
    existing_user = User.get_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(user.password)
    User.create(user.username, hashed_password)

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/search")
async def search_wikipedia(query: str, current_user: dict = Depends(get_current_user)):
    try:
        search_results = fetch_wikipedia_articles(query=query)
        return search_results
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error in llm call: " + str(e))


@router.post("/save_articles")
async def save_multiple_articles(articles: List[ArticleCreate], current_user: dict = Depends(get_current_user)):
    saved_articles = []
    
    for article in articles:
        try:
            article_id = str(uuid.uuid4())
            
            SavedArticle.create(article_id, article.title, article.link, article.content, article.tags, current_user["id"])
            
            saved_articles.append({
                "article_id": article_id,
                "title": article.title,
                "content": article.content,
                "tags": article.tags,
            })
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving article {article.title}: {str(e)}")
    
    return saved_articles


@router.get("/saved_articles")
async def get_saved_articles(current_user: dict = Depends(get_current_user)):
    saved_articles = SavedArticle.get_by_user(current_user["id"])
    return saved_articles


@router.put("/update_tags/{article_id}")
async def update_tags(article_id: str, article_update: ArticleUpdate, current_user: dict = Depends(get_current_user)):
    article = SavedArticle.get_by_id_and_user(article_id, current_user["id"])
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    SavedArticle.update_tags(article_id, article_update.tags)
    return {"message": "Tags updated successfully"}