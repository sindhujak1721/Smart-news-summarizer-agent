"""
Module 3: Article Extraction & Summarization
Fetches article content from URLs and generates clean, concise summaries using LLM.
Handles network errors, parsing failures, and missing content gracefully.
"""

from newspaper import Article
from groq import Groq
from langchain_core.prompts import PromptTemplate
from utils.api_keys import get_groq_key
from typing import Optional, Dict, Tuple

client = Groq(api_key=get_groq_key())

# ✅ LLM prompt for summarization
summarize_prompt = PromptTemplate(
    input_variables=["article_content"],
    template="""
You are a news summarization expert.
Summarize the following article in 3-4 sentences, capturing the key points.
Keep it concise, informative, and neutral.

Article:
{article_content}

Summary:
"""
)


def fetch_article_content(url: str) -> Optional[Tuple[str, str]]:
    """
    Fetch article content from a URL using newspaper3k.
    
    Args:
        url (str): The URL of the article
        
    Returns:
        Tuple[str, str]: (title, text) if successful, None if failed
    """
    try:
        article = Article(url, request_timeout=10)
        article.download()
        article.parse()
        
        # Validate that we got meaningful content
        text = article.text.strip() if article.text else ""
        
        # Check for minimum content length (relaxed to 80 chars)
        if len(text) < 80:
            print(f"⚠️  Article at {url} has insufficient content (likely paywalled or blocked)")
            return None
        
        # Filter out pages that are just copyright notices or navigation
        spam_keywords = ["copyright", "all rights reserved", "cookie", "terms of service", "privacy policy"]
        text_lower = text.lower()
        spam_count = sum(1 for keyword in spam_keywords if keyword in text_lower)
        
        # If almost entire page is spam keywords, reject it
        if spam_count >= 4:
            print(f"⚠️  Article at {url} appears to be navigation/legal text, not news content")
            return None
        
        # Validate we have a proper title
        if not article.title or len(article.title.strip()) < 5:
            print(f"⚠️  Article at {url} has no valid title")
            return None
        
        return (article.title, text)
    
    except Exception as e:
        error_msg = str(e).lower()
        if "404" in error_msg or "not found" in error_msg:
            print(f"⚠️  Article not found (404): {url}")
        elif "403" in error_msg or "forbidden" in error_msg:
            print(f"⚠️  Article blocked/forbidden (403): {url}")
        elif "timeout" in error_msg:
            print(f"⚠️  Connection timeout: {url}")
        else:
            print(f"❌ Error fetching article from {url}: {str(e)}")
        return None


def summarize_article(article_text: str) -> Optional[str]:
    """
    Generate a summary of article content using Groq LLM.
    
    Args:
        article_text (str): The full text of the article
        
    Returns:
        str: The summary, or None if summarization fails
    """
    try:
        # Truncate very long articles to avoid token limits
        max_chars = 4000
        if len(article_text) > max_chars:
            article_text = article_text[:max_chars] + "..."
        
        prompt = summarize_prompt.format(article_content=article_text)
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        
        summary = response.choices[0].message.content.strip()
        return summary
    
    except Exception as e:
        print(f"❌ Error summarizing article: {str(e)}")
        return None


def process_article(url: str) -> Optional[Dict]:
    """
    Complete pipeline: fetch article and generate summary.
    
    Args:
        url (str): The article URL
        
    Returns:
        Dict with 'url', 'title', 'summary' if successful, None if failed
    """
    # Step 1: Fetch article content
    result = fetch_article_content(url)
    if not result:
        return None
    
    title, text = result
    
    # Step 2: Generate summary
    summary = summarize_article(text)
    if not summary:
        return None
    
    # Step 3: Return structured data
    return {
        "url": url,
        "title": title,
        "summary": summary
    }


def process_multiple_articles(urls: list) -> Dict:
    """
    Process multiple article URLs and return results and failures.
    
    Args:
        urls (list): List of article URLs
        
    Returns:
        Dict with 'processed' (successful articles) and 'failed' (failed URLs)
    """
    processed = []
    failed = []
    
    for url in urls:
        print(f"🔄 Processing: {url}")
        result = process_article(url)
        
        if result:
            processed.append(result)
            print(f"✅ Successfully processed: {result['title']}")
        else:
            failed.append(url)
            print(f"⚠️  Failed to process: {url}")
    
    return {
        "processed": processed,
        "failed": failed
    }
