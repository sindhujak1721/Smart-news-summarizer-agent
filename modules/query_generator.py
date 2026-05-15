from groq import Groq
from langchain_core.prompts import PromptTemplate
from utils.api_keys import get_groq_key

client = Groq(api_key=get_groq_key())

query_prompt = PromptTemplate(
    input_variables=["topic"],
    template="""
Generate a refined and short news search query for the topic: "{topic}".
Return ONLY the search query.
"""
)

def generate_search_query(topic: str) -> str:
    try:
        prompt = query_prompt.format(topic=topic)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        # ✅ Correct extraction of LLM output
        return response.choices[0].message.content.strip()

    except Exception as e:
        print("❌ Error in generate_search_query:", e)
        return topic
