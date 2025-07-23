from openai import OpenAI
from config.config import OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)

def summarize_article(article_text):
    prompt = (
        "You are an expert journalist. Carefully analyze the following news article and write a clear, factual, and professionally written summary. "
        "Your summary should be in paragraph form and should:\n"
        "- Clearly explain what the article is about\n"
        "- Include major facts, statistics, or poll results\n"
        "- Describe any public or political reactions\n"
        "- Mention key viewpoints or developments\n"
        "- Maintain a neutral and journalistic tone\n\n"
        "Do not include the headline, author, or date—they will be displayed separately.\n\n"
        f"{article_text}"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.5
    )

    return response.choices[0].message.content.strip()
