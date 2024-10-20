import uuid
from app.database import execute_query, execute_non_query

class User:
    @staticmethod
    def get_by_username(username: str):
        users = execute_query("SELECT id, username, hashed_password FROM users WHERE username = %s", (username,))
        if users:
            user = users[0]
            return {"id": user[0], "username": user[1], "hashed_password": user[2]}
        return None

    @staticmethod
    def create(username: str, hashed_password: str):
        execute_non_query(
            "INSERT INTO users (id, username, hashed_password) VALUES (%s, %s, %s)",
            (str(uuid.uuid4()), username, hashed_password)
        )

class SavedArticle:
    @staticmethod
    def create(article_id: str,title: str, link: str, content: str, tags: str, user_id: str):
        execute_non_query(
            "INSERT INTO saved_articles (id, title, link, content, tags, user_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (article_id, title, link, content, tags, user_id)
        )

    @staticmethod
    def get_by_user(user_id: str):
        articles = execute_query(
            "SELECT id, title, link, content, tags FROM saved_articles WHERE user_id = %s", (user_id,)
        )

        if not articles:
            return list()

        formatted_articles = list()
        for article in articles:
            formatted_article = {
                "article_id": article[0],
                "title": article[1],
                "link": article[2],
                "content": article[3],
                "tags": article[4]
            }
            formatted_articles.append(formatted_article)

        return formatted_articles

    @staticmethod
    def update_tags(article_id: str, tags: str):
        execute_non_query(
            "UPDATE saved_articles SET tags = %s WHERE id = %s",
            (tags, article_id)
        )

    @staticmethod
    def get_by_id_and_user(article_id: str, user_id: str):
        return execute_query(
            "SELECT id FROM saved_articles WHERE id = %s AND user_id = %s", (article_id, user_id)
        )