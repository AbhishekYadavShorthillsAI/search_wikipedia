import requests
from bs4 import BeautifulSoup
from ..llm import generate_tags


# Function to get article content by pageid
def get_article_content(pageid):
    url = "https://en.wikipedia.org/w/api.php"
    
    params = {
        "action": "parse",
        "pageid": pageid,
        "format": "json",
        "prop": "text",
        "utf8": 1,
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "parse" in data:
        return data["parse"]["text"]["*"]  # Returns the full HTML content of the article
    else:
        return None

# Function to extract plain text from HTML content
def extract_plain_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()

def fetch_wikipedia_articles(query):
    """Fetch titles, links, and content of Wikipedia articles based on the search query."""

    # Main search functionality
    url = "https://en.wikipedia.org/w/api.php"
    
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "utf8": 1,
        "srlimit": 5,  # Limit to 5 results
    }

    response = requests.get(url, params=params)
    data = response.json()

    articles = []

    # Check if the response contains search results
    if "query" in data and "search" in data["query"]:
        results = data["query"]["search"]
        for article in results:
            title = article["title"]
            pageid = article["pageid"]
            link = f"https://en.wikipedia.org/?curid={pageid}"  # Constructing the URL
            
            # Get the full content of the article
            article_content = get_article_content(pageid)
            plain_text = extract_plain_text(article_content) if article_content else "Content not available."

            tags = generate_tags(title=title, content=plain_text)

            # Append article details to the list
            articles.append({
                "title": title,
                "link": link,
                "content": plain_text[:100],  # Store only the first 500 characters of the content
                "tags": tags
            })
    
    return articles
