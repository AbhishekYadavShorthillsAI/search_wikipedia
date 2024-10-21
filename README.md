# Wiki Search App

## Overview
The **Wiki Search App** is a FastAPI-based application that allows users to search for Wikipedia articles, save them, and automatically generate relevant tags using the Gemini Pro language model. This app includes features like user registration, login, searching, saving articles, and updating tags for saved content.

**Project GitHub**: [Wiki Search]

---

## Table of Contents
1. [High Level Flow](#high-level-flow)
2. [Project Structure](#project-structure)
3. [API Endpoints](#api-endpoints)
    - [Register User](#register-user)
    - [Login](#login)
    - [Search Wikipedia](#search-wikipedia)
    - [Save Article](#save-article)
    - [Get Saved Articles](#get-saved-articles)
    - [Update Tags](#update-tags)
4. [Code Flow](#code-flow)
5. [Setup and Run](#setup-and-run)
6. [Relevant Links](#relevant-links)

---

## High Level Flow
1. Users can register and log in to access the API.
2. They can search for Wikipedia articles and save selected ones to their account.
3. Upon saving an article, the Gemini Pro language model generates tags for the article.
4. Users can retrieve their saved articles and update the generated tags as needed.

---

## Project Structure

```
wiki_summary_app/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── llm.py
│   └── api/
│       ├── __init__.py
│       └── endpoints.py
│
├── requirements.txt
└── .env
```

---

## API Endpoints

### Register User
**URL**: `/register`  
**Method**: `POST`  

**Request Body**:
```json
{
  "username": "newuser",
  "password": "securepassword123"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Login
**URL**: `/token`  
**Method**: `POST`  

**Request Body**:
```json
{
  "username": "existinguser",
  "password": "userpassword123"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Search Wikipedia
**URL**: `/search?query=python programming`  
**Method**: `GET`  

**Headers**: `Authorization: Bearer <access_token>`  

**Response**:
```json
[
  {
    "title": "Python (programming language)",
    "link": "link",
    "content": "Python is a high-level, general-purpose programming language...",
    "tags": "programming, high-level language, interpreted language"
  }
]
```

### Save Article
**URL**: `/save_articles`  
**Method**: `POST`  

**Headers**: `Authorization: Bearer <access_token>`  

**Request Body**:
```json
[
  {
    "title": "Python (programming language)",
    "link": "link",
    "content": "Python is a high-level, general-purpose programming language...",
    "tags": ["programming", "scripting", "object-oriented"]
  }
]
```

**Response**:
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Python (programming language)",
    "link": "link",
    "content": "Python is a high-level, general-purpose programming language...",
    "tags": ["programming", "scripting", "object-oriented"]
  }
]
```

### Get Saved Articles
**URL**: `/saved_articles`  
**Method**: `GET`  

**Headers**: `Authorization: Bearer <access_token>`  

**Response**:
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Python (programming language)",
    "link": "link",
    "content": "Python is a high-level, general-purpose programming language...",
    "tags":  ["programming", "scripting", "object-oriented"]
  }
]
```

### Update Tags
**URL**: `/update_tags/{article_id}`  
**Method**: `PUT`  

**Headers**: `Authorization: Bearer <access_token>`  

**Request Body**:
```json
{
  "tags": ["sample_tag"]
}
```

**Response**:
```json
{
  "message": "Tags updated successfully"
}
```

---

## Code Flow

1. **User Registration and Authentication**:
    - New users register via `/register` endpoint (`endpoints.py`).
    - User credentials are hashed and stored in the database (`auth.py`, `models.py`).
    - Users log in via `/token`, receiving a JWT for authentication.

2. **Wikipedia Search**:
    - Users search Wikipedia using the `/search` endpoint (`endpoints.py`).
    - The app uses the `wikipedia` library to fetch search results.

3. **Saving Articles**:
    - Authenticated users save articles via `/save_article` endpoint.
    - The app uses the Gemini Pro model to generate tags (`llm.py`).
    - Article details and tags are stored in the database (`models.py`).

4. **Retrieving Saved Articles**:
    - Users fetch their saved articles using `/saved_articles` endpoint.
    - Articles are retrieved from the database for authenticated users.

5. **Updating Tags**:
    - Users update tags for their saved articles via `/update_tags/{article_id}`.
    - The app verifies article ownership and updates the tags in the database.

---

## Setup and Run

1. **Clone the repository** and navigate to the project directory.
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows: `venv\Scripts\activate`
   - Unix or MacOS: `source venv/bin/activate`

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up your `.env` file** with necessary environment variables:
   ```bash
   DATABASE_URL=your_database_url_here
   SECRET_KEY=your_secret_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   ```

6. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

---

## 🛠️🔗 Relevant Links
- [Getting started with Wikimedia APIs](https://api.wikimedia.org/wiki/Getting_started_with_Wikimedia_APIs)
- [Build a Python app with CockroachDB](https://www.cockroachlabs.com/docs/v24.2/build-a-python-app-with-cockroachdb)
- [Google Gemini API documentation](https://ai.google.dev/gemini-api/docs)
