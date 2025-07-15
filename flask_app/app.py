from flask import Flask, render_template, request
from newspaper import Article
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables from .env
load_dotenv()

# Create OpenAI client using API key from .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

# Summarize article text using ChatGPT
def summarize_article(article_text):
    prompt = (
        "You are an expert journalist. Summarize this article clearly and concisely:\n\n"
        f"{article_text}"
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

# Extract article content from a URL
def scrape_article(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

# Web route to display and handle the summarizer
@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    error = None
    if request.method == 'POST':
        article_url = request.form.get('article_url')
        if article_url:
            try:
                article_text = scrape_article(article_url)
                if article_text:
                    summary = summarize_article(article_text)
                else:
                    error = "Failed to extract article content."
            except Exception as e:
                error = f"Error: {e}"
        else:
            error = "Please enter a URL."
    return render_template('index.html', summary=summary, error=error)

if __name__ == '__main__':
    app.run(debug=True)
