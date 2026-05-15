"""
Module 4: Final Report Generation & Error Handling
Combines summaries into a well-formatted report.
Handles failures gracefully and produces readable, structured output.
"""

from datetime import datetime
from typing import Dict, List, Optional
from groq import Groq
from langchain_core.prompts import PromptTemplate
from utils.api_keys import get_groq_key
import html as html_escape

client = Groq(api_key=get_groq_key())

# ✅ LLM prompt for generating a cohesive report
report_prompt = PromptTemplate(
    input_variables=["topic", "summaries"],
    template="""
You are a professional news report generator.
Create a brief, cohesive executive summary of the following news summaries about "{topic}".
Make it flow naturally and highlight the most important points.

Summaries:
{summaries}

Executive Summary:
"""
)


def generate_report_section(topic: str, summaries: List[str]) -> Optional[str]:
    """
    Generate an executive summary combining all article summaries.
    
    Args:
        topic (str): The news topic
        summaries (List[str]): List of individual article summaries
        
    Returns:
        str: The cohesive executive summary, or None if generation fails
    """
    if not summaries:
        return None
    
    try:
        # Combine summaries with numbering
        formatted_summaries = "\n".join(
            [f"{i+1}. {s}" for i, s in enumerate(summaries)]
        )
        
        prompt = report_prompt.format(topic=topic, summaries=formatted_summaries)
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        
        report = response.choices[0].message.content.strip()
        return report
    
    except Exception as e:
        print(f"❌ Error generating report section: {str(e)}")
        return None


def format_full_report(
    topic: str,
    processed_articles: List[Dict],
    failed_urls: List[str],
    executive_summary: Optional[str]
) -> str:
    """
    Format all components into a professional corporate report.
    
    Args:
        topic (str): The news topic
        processed_articles (List[Dict]): Processed articles with summaries
        failed_urls (List[str]): URLs that failed to process
        executive_summary (Optional[str]): The executive summary from LLM
        
    Returns:
        str: Formatted final report
    """
    report = []
    
    # Professional Corporate Header
    report.append("")
    report.append("NEWS SUMMARY REPORT")
    report.append(f"Topic: {topic}")
    report.append("=" * 80)
    report.append("")
    report.append(f"Report Date: {datetime.now().strftime('%B %d, %Y')}")
    report.append(f"Report Time: {datetime.now().strftime('%I:%M %p')}")
    report.append("")
    
    # Executive Summary
    if executive_summary:
        report.append("EXECUTIVE SUMMARY")
        report.append("-" * 80)
        report.append("")
        
        # Wrap executive summary text professionally
        summary_lines = executive_summary.split('\n')
        for line in summary_lines:
            line = line.strip()
            if not line:
                continue
            # Professional word wrapping
            if len(line) > 80:
                words = line.split()
                current_line = ""
                for word in words:
                    if len(current_line) + len(word) + 1 <= 80:
                        current_line += word + " "
                    else:
                        if current_line:
                            report.append(current_line.rstrip())
                        current_line = word + " "
                if current_line:
                    report.append(current_line.rstrip())
            else:
                report.append(line)
        
        report.append("")
        report.append("")
    
    # Articles Section - Professional Format
    if processed_articles:
        report.append("ARTICLE SUMMARIES")
        report.append("-" * 80)
        report.append("")
        
        for idx, article in enumerate(processed_articles, 1):
            report.append(f"{idx}. {article['title']}")
            report.append("")
            
            # Summary with professional formatting
            summary_text = article['summary'].strip()
            summary_lines = summary_text.split('\n')
            for line in summary_lines:
                line = line.strip()
                if not line:
                    continue
                if len(line) > 80:
                    words = line.split()
                    current_line = ""
                    for word in words:
                        if len(current_line) + len(word) + 1 <= 80:
                            current_line += word + " "
                        else:
                            if current_line:
                                report.append(current_line.rstrip())
                            current_line = word + " "
                    if current_line:
                        report.append(current_line.rstrip())
                else:
                    report.append(line)
            
            report.append("")
            report.append(f"Source: {article['url']}")
            report.append("")
            report.append("-" * 80)
            report.append("")
    
    # Professional Footer
    report.append("END OF REPORT")
    report.append("=" * 80)
    report.append("")
    
    return "\n".join(report)


def generate_final_report(
    topic: str,
    processed_articles: List[Dict],
    failed_urls: List[str]
) -> str:
    """
    Main function to generate the complete final report.
    
    Args:
        topic (str): The news topic
        processed_articles (List[Dict]): List of processed articles
        failed_urls (List[str]): List of failed URLs
        
    Returns:
        str: The complete formatted report
    """
    try:
        # Step 1: Extract summaries from processed articles
        summaries = [article["summary"] for article in processed_articles]
        
        # Step 2: Generate executive summary (optional if we have articles)
        executive_summary = None
        if summaries:
            executive_summary = generate_report_section(topic, summaries)
        
        # Step 3: Format and return the complete report
        final_report = format_full_report(
            topic,
            processed_articles,
            failed_urls,
            executive_summary
        )
        
        return final_report
    
    except Exception as e:
        print(f"❌ Error generating final report: {str(e)}")
        # Fallback report on error
        return f"⚠️  Error generating report for topic '{topic}': {str(e)}"


def save_report_to_file(report: str, filename: Optional[str] = None) -> Optional[str]:
    """
    Save the report to a file.
    
    Args:
        report (str): The report content
        filename (Optional[str]): Custom filename, or auto-generated if None
        
    Returns:
        str: The filename where report was saved, or None if save failed
    """
    try:
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"news_report_{timestamp}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"✅ Report saved to: {filename}")
        return filename
    
    except Exception as e:
        print(f"❌ Error saving report to file: {str(e)}")
        return None


def generate_html_report(report_text: str, style: str = 'corporate') -> str:
    """
    Generate a safe HTML version of a plain-text report using the selected style.

    Args:
        report_text (str): The plain-text report produced by `generate_final_report`.
        style (str): One of ('corporate', 'serif', 'times', 'mono', 'clean').

    Returns:
        str: HTML string (safe, escaped) ready to be embedded in the UI.
    """
    # Map style keys to CSS font-family and accent color
    font_map = {
        'standard': ("'Segoe UI', Tahoma, Geneva, Verdana, sans-serif", '#2a3550'),
        'serif': ("Georgia, 'Times New Roman', Times, serif", '#2a3550'),
        'mono': ("'Courier New', Courier, monospace", '#2a3550'),
        'corporate': ("'Segoe UI', Tahoma, Geneva, Verdana, sans-serif", '#2a3550')
    }

    font_family, accent = font_map.get(style, font_map['corporate'])

    # Sanitize the report content to avoid XSS
    safe_text = html_escape.escape(report_text)

    # Remove decoration lines and normalize sections
    lines = [l.rstrip() for l in safe_text.split('\n')]
    cleaned = []
    for l in lines:
        if set(l.strip()) <= set('=- ') and len(l.strip()) > 0:
            # skip separator lines like '====' or '----'
            continue
        cleaned.append(l)

    # Convert to HTML with simple section detection
    html_parts = []
    i = 0
    while i < len(cleaned):
        line = cleaned[i].strip()
        if not line:
            i += 1
            continue

        # Detect section headers (all caps short lines)
        if line.isupper() and len(line) < 60:
            header = line.title()
            html_parts.append(f'<h2 style="color:{accent}; margin-top:18px;">{header}</h2>')
            i += 1
            continue

        # Collect paragraph until blank line
        para_lines = [line]
        j = i + 1
        while j < len(cleaned) and cleaned[j].strip() != '':
            para_lines.append(cleaned[j].strip())
            j += 1

        paragraph = ' '.join(para_lines)
        paragraph = paragraph.replace('  ', ' ')
        html_parts.append(f'<p style="margin:8px 0;">{paragraph}</p>')
        i = j + 1

    html_body = '\n'.join(html_parts)

    # Build final HTML with light card styling
    html_template = f"""
    <div style="font-family: {font_family}; color:#111; line-height:1.6; padding:8px;">
      <div style="max-width:100%; padding:20px; background: #fbfdff; border-radius:10px; border:1px solid #eef3fb; box-shadow: 0 6px 18px rgba(50,70,120,0.04);">
        {html_body}
      </div>
    </div>
    """

    return html_template
