from flask import Flask, render_template, request
from newspaper import Article
from dotenv import load_dotenv
from openai import OpenAI
from urllib.parse import urlparse
import os
from datetime import datetime

# Load environment variables from .env
load_dotenv()

# Create OpenAI client using API key from .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

# Summarize article text using ChatGPT
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

# Extract article metadata from a URL
def scrape_article(url):
    article = Article(url)
    article.download()
    article.parse()

    # Fallbacks
    title = article.title.strip() if article.title else "Headline not available"
    authors = ', '.join(article.authors) if article.authors else "Unknown"
    publish_date = (
        article.publish_date.strftime("%B %d, %Y") if article.publish_date else "Date not available"
    )
    text = article.text.strip() if article.text else ""
    source_domain = urlparse(url).netloc or "Source not available"

    return {
        "title": title,
        "authors": authors,
        "date": publish_date,
        "source": source_domain,
        "source_url": url,
        "text": text
    }

# Web route to display and handle the summarizer
@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    error = None
    metadata = {}

    if request.method == 'POST':
        article_url = request.form.get('article_url')
        if article_url:
            try:
                article_data = scrape_article(article_url)
                if article_data["text"]:
                    summary = summarize_article(article_data["text"])
                    metadata = {
                        "title": article_data["title"],
                        "author": article_data["authors"],
                        "date": article_data["date"],
                        "source": article_data["source"],
                        "source_url": article_url
                    }
                else:
                    error = "Failed to extract article content."
            except Exception as e:
                error = f"Error: {e}"
        else:
            error = "Please enter a URL."

    return render_template('index.html', summary=summary, metadata=metadata, error=error)

if __name__ == '__main__':
    app.run(debug=True)
