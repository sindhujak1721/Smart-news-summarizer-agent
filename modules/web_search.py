try:
    from tavily import TavilyClient
except:
    from tavily.client import TavilyClient

from groq import Groq
from langchain_core.prompts import PromptTemplate
from utils.api_keys import get_groq_key, get_tavily_key

client = Groq(api_key=get_groq_key())
tavily = TavilyClient(api_key=get_tavily_key())

filter_prompt = PromptTemplate(
    input_variables=["results"],
    template="""
You are a news filtering agent.
Given the search results:
{results}

Pick ONLY the 3–5 most relevant URLs.
Return only URLs, one per line.
"""
)

def perform_web_search(query: str):
    try:
        response = tavily.search(query=query, max_results=10)
        return response.get("results", [])
    except Exception as e:
        print("❌ Tavily error:", e)
        return []

def select_relevant_articles(search_results):
    """
    Use LLM to autonomously filter and select the most relevant articles.
    
    Args:
        search_results: List of search results from Tavily
        
    Returns:
        List of URLs of the most relevant articles
    """
    try:
        # Filter out articles that are likely to be problematic
        filtered_results = []
        for r in search_results:
            url = r.get('url', '')
            title = r.get('title', '')
            
            # Skip main category/index pages (no real content)
            problematic_patterns = [
                '/politics/$',  # Main politics page
                '/topics/',     # Topic index pages
                '/category/',   # Category pages
                '/tag/',        # Tag pages
                '/search',      # Search results pages
                '/latest',      # Latest posts
            ]
            
            skip = False
            for pattern in problematic_patterns:
                if pattern in url.lower():
                    skip = True
                    break
            
            if not skip and len(title) > 10:  # Ensure has meaningful title
                filtered_results.append(r)
        
        # Use remaining results for filtering
        if not filtered_results:
            filtered_results = search_results
        
        formatted = ""
        for r in filtered_results[:7]:  # Take top 7 for LLM filtering
            formatted += f"Title: {r.get('title')}\nURL: {r.get('url')}\nSnippet: {r.get('snippet')}\n\n"

        prompt = filter_prompt.format(results=formatted)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=200
        )

        # Extract URLs from response
        raw_output = response.choices[0].message.content.strip()
        urls = []
        
        for line in raw_output.split("\n"):
            line = line.strip()
            if line.startswith("http"):
                urls.append(line)
        
        return urls[:5]  # Return top 5 URLs

    except Exception as e:
        print("❌ Error in select_relevant_articles:", e)
        return []
