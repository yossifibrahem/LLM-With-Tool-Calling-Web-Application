import json
import asyncio

from web_tool.duck_duck_go_search import DuckDuckGoSearchManager
from web_tool.test import scrape_multiple_websites
from web_tool.embedding_similarity import find_most_similar_content

ddg = DuckDuckGoSearchManager()


def text_search(query: str, prompt, num_websites: int = 4, citations: int = 5) -> str:
    """Conducts a general web text search and retrieves information from the internet in response to user queries.

    This function is best used when the user's query is seeking broad information available on various websites. It
    is ideal for queries that require diverse perspectives or data from multiple sources, not limited to current
    events or specific topics. Use this function for general inquiries, research, or when the user's query is not
    explicitly news-related. It fetches relevant data from the internet in response to user queries, enhancing GPT's
    knowledge base.

    :param query: The search query string for finding relevant web text results.
    :param num_results: The maximum number of URLs to return. Defaults to 3 if not provided. (optional)

    :return: A JSON-formatted string. Each element in the JSON represents the result of scraping a single URL,
    containing either the scraped content or an error message.
    """
    try:
        num_websites = min(num_websites, 8)  # Maximum 8 websites
        citations = min(citations, 10)        # Maximum 10 citations
        
        urls = ddg.text_search(query, int(num_websites))
        scraped_data = asyncio.run(scrape_multiple_websites(urls))
        filtered_data = find_most_similar_content(scraped_data, prompt, citations)
    except Exception as e:
        return {"url": "error", "citation": str(e)}
    return filtered_data


def images_search(query, num_results=3):
    """Performs the image search for a specific query. For example, "puppies". If possible, the output should be in Markdown format.

    This function enables real-time image search and information retrieval for GPT models. It fetches relevant data from the internet in response to user queries, enhancing GPT's knowledge base.

    :param query: The search query string for the image search.
    :param num_results: The maximum number of URLs to return. Defaults to 3 if not provided. (optional)

    :return: A list of dictionaries, where each dictionary contains 'image' (URL of the actual image) and 'thumbnail' (URL of the image's thumbnail).
    """
    try:
        image_info = ddg.images_search(query, int(num_results))
        return image_info
    except Exception as e:
        return {"image": "error", "thumbnail": str(e)}
    


def webpage_scraper(url):
    """Scrape a webpage for its text content.

    This function enables web scraping for GPT models. It fetches the text content of a webpage and returns it to the
    model. Use this function if user queries include a URL.

    :param url: The URL of the webpage to scrape.
    :return: A JSON-formatted string containing the scraped text. In case of an error, it returns a JSON-formatted string with an error message.
    """
    try:
        result = asyncio.run(scrape_multiple_websites([url]))
        return result[0]
    except Exception as e:
        return json.dumps({"error": str(e)})
