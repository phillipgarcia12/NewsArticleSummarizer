from flask import Flask, render_template, request
from Core.scraperLogic import scrape_article
from Core.summarizer import summarize_article


app = Flask(__name__)

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
