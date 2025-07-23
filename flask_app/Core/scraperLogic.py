from newspaper import Article
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

def scrape_article(url):
    try:
        # Try using newspaper3k first
        article = Article(url)
        article.download()
        article.parse()

        title = article.title.strip() if article.title else "Headline not available"
        authors = ', '.join(article.authors) if article.authors else "Unknown"
        publish_date = (
            article.publish_date.strftime("%B %d, %Y") if article.publish_date else "Date not available"
        )
        text = article.text.strip() if article.text else ""
        source_domain = urlparse(url).netloc or "Source not available"

        if text:
            return {
                "title": title,
                "authors": authors,
                "date": publish_date,
                "source": source_domain,
                "source_url": url,
                "text": text
            }

    except Exception as e:
        print(f"[Fallback triggered] Newspaper3k failed: {e}")

    # Fallback: requests + BeautifulSoup
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = "\n".join(p.get_text() for p in paragraphs if p.get_text())

        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else "Headline not available"
        source_domain = urlparse(url).netloc or "Source not available"

        return {
            "title": title,
            "authors": "Unknown",
            "date": "Date not available",
            "source": source_domain,
            "source_url": url,
            "text": text.strip()
        }

    except Exception as fallback_error:
        raise Exception(f"Both scraping methods failed: {fallback_error}")
