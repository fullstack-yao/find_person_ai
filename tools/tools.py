# import os

# from dotenv import load_dotenv
# from langchain.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults

# load_dotenv()


def get_profile_url_tavily(name: str):
    """Seaches for Linkedin or Twitter Profile page."""
    # tavily_search_wrapper = TavilySearchAPIWrapper(
    #     tavily_api_key=os.getenv("TAVILY_API_KEY")
    # )
    # search = TavilySearchResults(api_wrapper=tavily_search_wrapper)
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res
