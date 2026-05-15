"""
Smart News Summarizer Agent
Main application that orchestrates all modules to create a news summarization agent.

Workflow:
1. User provides a topic
2. Module 1: Generate optimized search query using LLM
3. Module 2: Perform web search and autonomously select relevant articles
4. Module 3: Extract and summarize each article
5. Module 4: Generate final formatted report with error handling
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.query_generator import generate_search_query
from modules.web_search import perform_web_search, select_relevant_articles
from modules.summarizer import process_multiple_articles
from modules.report_generator import generate_final_report, save_report_to_file


def run_news_summarizer_agent(topic: str, save_to_file: bool = True) -> str:
    """
    Main function to run the complete news summarizer agent pipeline.
    
    Args:
        topic (str): The news topic to summarize
        save_to_file (bool): Whether to save the report to a file
        
    Returns:
        str: The final formatted report
    """
    
    print("\n" + "=" * 80)
    print(f"🚀 SMART NEWS SUMMARIZER AGENT")
    print(f"Topic: {topic}")
    print("=" * 80 + "\n")
    
    try:
        # ============ MODULE 1: Query Generation ============
        print("📝 [Module 1] Generating optimized search query...")
        search_query = generate_search_query(topic)
        print(f"✅ Generated query: '{search_query}'\n")
        
        # ============ MODULE 2: Web Search & Article Selection ============
        print("🔍 [Module 2] Searching for relevant articles...")
        search_results = perform_web_search(search_query)
        
        if not search_results:
            print("❌ No search results found. Agent cannot proceed.")
            return "❌ No news articles found for this topic."
        
        print(f"✅ Found {len(search_results)} results")
        
        print("\n🤖 [Module 2] Autonomously filtering relevant articles...")
        selected_urls = select_relevant_articles(search_results)
        
        if not selected_urls:
            print("⚠️  No relevant articles selected after filtering.")
            return "⚠️  Could not find relevant articles to summarize."
        
        print(f"✅ Selected {len(selected_urls)} most relevant articles\n")
        
        # ============ MODULE 3: Article Extraction & Summarization ============
        print("📥 [Module 3] Extracting and summarizing articles...")
        results = process_multiple_articles(selected_urls)
        
        processed_articles = results["processed"]
        failed_urls = results["failed"]
        
        if not processed_articles:
            print("❌ Could not process any articles.")
            return "❌ Failed to extract and summarize articles."
        
        print(f"✅ Successfully processed {len(processed_articles)} articles\n")
        
        # ============ MODULE 4: Report Generation & Error Handling ============
        print("📋 [Module 4] Generating final formatted report...")
        final_report = generate_final_report(topic, processed_articles, failed_urls)
        
        # Save report to file if requested
        if save_to_file:
            save_report_to_file(final_report)
        
        print("✅ Report generation complete!\n")
        
        return final_report
    
    except Exception as e:
        error_msg = f"❌ AGENT ERROR: {str(e)}"
        print(error_msg)
        return error_msg


def main():
    """
    Entry point for the application.
    Can be run directly or imported as a module.
    """
    
    # Example usage
    topic = input("\n🎯 Enter a news topic to summarize: ").strip()
    
    if not topic:
        print("❌ Topic cannot be empty!")
        return
    
    # Run the agent
    report = run_news_summarizer_agent(topic, save_to_file=True)
    
    # Print the report
    print("\n" + report)


if __name__ == "__main__":
    main()
