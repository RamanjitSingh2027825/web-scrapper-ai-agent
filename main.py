from config import PINECONE_API_KEY, PINECONE_INDEX_NAME
from utils import load_crawl_docs, load_scrape_docs
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import PromptTemplate
from pinecone import Pinecone
from dotenv import load_dotenv
load_dotenv()

# Connect to Pinecone INDEX
pinecone_client = Pinecone(api_key=PINECONE_API_KEY)
INDEX = pinecone_client.Index(PINECONE_INDEX_NAME)

# # Take the link
link = input("Enter the link: ")

# # load the documents from scrape
docs = load_crawl_docs(link)
while docs == []:
    docs = load_scrape_docs(link)
print(docs)

# # create embeddings
EMBEDDINGS = OpenAIEmbeddings()

# # update the vector store
vector_store = PineconeVectorStore(INDEX, EMBEDDINGS)
vector_store.add_documents(docs)

# user query
query = input("Enter the query: ")
relevant_docs = vector_store.similarity_search_with_score(query, k=4)

# prompt
template = f'''
# Relevant Documents : \n{relevant_docs}
# Query : {query}
'''

prompt = PromptTemplate.from_template(template)

LLM = ChatOpenAI()

chain = prompt | LLM

print(chain.invoke({'query':query}).content)
