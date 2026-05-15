# 📰 Smart News Summarizer Agent



🔗 Live Demo

https://huggingface.co/spaces/Sornambal/Smart_News_Summarizer_Agent


**Build an agent that automatically finds recent news on a topic and creates a brief summary.**

## 🎯 Goal

The agent makes **2 autonomous decisions**:
1. What search query to use
2. Which articles are most relevant to summarize



## 🏗️ 4-Module Architecture

```
User Topic
    ↓
[Module 1: Query Generation] 
    ↓
[Module 2: Web Search & Article Selection] 
    ↓
[Module 3: Article Extraction & Summarization] 
    ↓
[Module 4: Report Generation & Error Handling] 

```

### Modules Overview

| Module | Owner | File | What It Does |
|--------|-------|------|--------------|
| **1** | Sornambal | `modules/query_generator.py` | Generates optimized search queries |
| **2** | Sornambal | `modules/web_search.py` | Searches API & filters relevant articles |
| **3** | Kiruthika | `modules/summarizer.py` | Fetches & summarizes articles |
| **4** | Kiruthika | `modules/report_generator.py` | Creates professional reports |

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Add API Keys
Create `.env` file:
```
GROQ_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

### 3. Run the Flask API Server (Web UI)
```bash
python main.py
```

Open: **http://localhost:5000**

## 📂 Project Structure

```
Smart-News-Summarizer-Agent/
├── modules/
│   ├── query_generator.py      # Module 1
│   ├── web_search.py           # Module 2
│   ├── summarizer.py           # Module 3
│   └── report_generator.py     # Module 4
├── app/
│   └── app.py                  # Orchestrator with run_news_summarizer_agent function
├── main.py                    # Flask API Server (Web UI)
├── .env                      # API Keys
└── requirements.txt
```





## 📊 Sample Output

```
================================================================================
📰 NEWS SUMMARY REPORT: YOUR TOPIC
================================================================================

📋 EXECUTIVE SUMMARY
[LLM-synthesized overview of all articles]

📄 ARTICLE SUMMARIES
[Individual 3-4 sentence summaries with URLs]

```

## 🔧 Technologies

- **Groq API** - LLM for query generation and summarization
- **Tavily API** - News search and article discovery
- **newspaper3k** - Article content extraction
- **LangChain** - LLM framework and prompts
- **Python 3.11** - Runtime environment

## 👥 Team

- **Modules 1 & 2** - Sornambal.P
- **Modules 3 & 4** - Kiruthika. S

## ✅ Status

**COMPLETE ✅** - All modules implemented, tested, and ready for production!

---


