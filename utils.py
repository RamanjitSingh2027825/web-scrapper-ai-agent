import re
from langchain_community.document_loaders.firecrawl import FireCrawlLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document
from config import FIRECRAWL_API_KEY

TEXT_SPLITTER = CharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

def remove_trailing_description(data):
    pattern = re.compile(r'''\[([^\]]+)\]\(.*?\)''')
    cleaned_data = pattern.sub(r'''-    \1''', data)
    return cleaned_data

def load_scrape_docs(url: str) -> list[Document]:
    scraper = FireCrawlLoader(api_key=FIRECRAWL_API_KEY, url=url, mode="scrape")
    docs = scraper.load()[0].page_content

    lines = docs.split("\n")
    cleaned_lines = [remove_trailing_description(line) for line in lines]
    cleaned_data = "\n".join(cleaned_lines)
    return [Document(page_content=cleaned_data)]
    # return TEXT_SPLITTER.create_documents([cleaned_data])

def load_crawl_docs(url: str) -> list[Document]:
    crawler = FireCrawlLoader(api_key=FIRECRAWL_API_KEY, url=url, mode="crawl")
    docs = crawler.load()[0].page_content

    lines = docs.split("\n")
    cleaned_lines = [remove_trailing_description(line) for line in lines]
    cleaned_data = "\n".join(cleaned_lines)
    return [Document(page_content=cleaned_data)]
    # return TEXT_SPLITTER.create_documents([cleaned_data])