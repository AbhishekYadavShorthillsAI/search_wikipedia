from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import GOOGLE_API_KEY

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
prompt_template = PromptTemplate.from_template(
"""You are an expert on giving tags to article, you will be provided with the article title and its content. Your task it to provide relevant tag to the article. You have respond only with tags, and they should be comma separated.

INPUT:
Article Title: {title}
Article Content: {content}
"""
)
tag_chain = LLMChain(llm=llm, prompt=prompt_template)

def generate_tags(title: str, content: str):
    return tag_chain.run(title=title, content=content)

