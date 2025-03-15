import os
import re
from datetime import datetime
from collections import defaultdict
from bs4 import BeautifulSoup

# Input and output directories
ARTICLES_DIR = "src/articles"
TOPIC_PAGES_DIR = "src/topic_pages"


def extract_article_data(article_path):
    """Extract data from the article HTML."""
    with open(article_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        title = soup.find("h1", {"id": "title"}).text.strip()
        date_str = soup.find("time", {"id": "date"})["datetime"]
        date = datetime.strptime(date_str, "%Y-%m-%d")
        flags = [
            flag.text.strip().lower().replace(" ", "_")
            for flag in soup.find("div", {"id": "flags"}).find_all("span")
        ]
        file_name = os.path.basename(article_path).replace(".html", "")
        return {"title": title, "date": date, "flags": flags, "file_name": file_name}


def generate_topic_page(topic, articles):
    """Generate an HTML page for a specific topic."""
    topic_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="/styles/style.css">
    <script src="/general.js"></script>
</head>
<body onload="loadHeader()">
    <div id="header"></div>
    <div style="padding-left: 5%;">
    <h2>{topic.replace('_', ' ').title()}</h2>
    <ol style="list-style-type: none;">
"""
    for article in articles:
        date_str = article["date"].strftime("%Y-%m-%d")
        topic_html += f'        <li><a href="/articles/{article["file_name"]}.html">{article["title"]}</a> <br> <time datetime="{date_str}">{date_str}</time></li>\n'
    topic_html += """    </ol>
</div>
</body>
</html>
"""
    return topic_html


def main():
    # Parse all articles
    articles = []
    for file_name in os.listdir(ARTICLES_DIR):
        if file_name.endswith(".html"):
            article_path = os.path.join(ARTICLES_DIR, file_name)
            article_data = extract_article_data(article_path)
            articles.append(article_data)

    # Group articles by topic
    topics = defaultdict(list)
    for article in articles:
        for flag in article["flags"]:
            topics[flag].append(article)
        topics["all_articles"].append(article)

    # Sort articles by date (newest first) in each topic
    for topic, articles_list in topics.items():
        topics[topic] = sorted(articles_list, key=lambda x: x["date"], reverse=True)

    # Ensure topic files already exist or throw an error
    for topic in topics:
        topic_file_path = os.path.join(TOPIC_PAGES_DIR, f"{topic}.html")
        if not os.path.exists(topic_file_path):
            raise FileNotFoundError(
                f"Topic file '{topic_file_path}' does not exist. Please create it first."
            )

    # Generate topic pages
    for topic, articles_list in topics.items():
        topic_page_path = os.path.join(TOPIC_PAGES_DIR, f"{topic}.html")
        with open(topic_page_path, "w", encoding="utf-8") as file:
            file.write(generate_topic_page(topic, articles_list))


if __name__ == "__main__":
    main()
