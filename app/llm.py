from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import GOOGLE_API_KEY

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

prompt_template = PromptTemplate.from_template(
"""You are an expert in generating precise and relevant tags for articles. You will be provided with the title and part of article's content. Your task is to analyze the information and provide a concise list of highly relevant, comma-separated tags. Keep the tags generic and don't keep them similar.

INPUT:
Article Title: {title}
Article Content: {content}

OUTPUT:
Provide only the relevant tags, comma-separated."""
)
tag_chain = LLMChain(llm=llm, prompt=prompt_template)

def generate_tags(title: str, content: str):
    comma_sep_tags_str = tag_chain.run(title=title, content=content)
    
    tags_list = tags_list = [tag.strip() for tag in comma_sep_tags_str.split(",")]
    return tags_list

