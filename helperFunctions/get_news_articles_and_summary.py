import os
from datetime import datetime

import requests

from helperFunctions.generate_open_ai_summary import generate_open_ai_summary


def get_news_articles_and_summary():
    today = datetime.now().strftime("%Y-%m-%d")

    url = (f'https://newsapi.org/v2/everything?'
           f'q=finance&'
           f'from={today}&'
           f'sortBy=popularity&'
           f'apiKey={os.getenv("NEWS_API_KEY")}')

    response = requests.get(url)

    articles = []
    if response.status_code == 200:
        data = response.json()
        all_articles = data.get('articles', [])

        if all_articles:
            articles = all_articles[:5]
        else:
            print("No articles found.")
    else:
        print(f"Failed to fetch news. Status code: {response.status_code}")

    news_summary = ""
    if articles:
        headlines = "\n".join([f"- {article['title']} ({article['source']['name']})"
                               for article in articles])

        summary_prompt = (
            f"Here are today's top financial news headlines:\n{headlines}\n\n"
            f"Create a brief, insightful summary of these financial headlines in 1-2 sentences. "
            f"Focus on the most important trends or events."
        )

        try:
            generate_open_ai_summary(summary_prompt)
        except Exception as e:
            print(f"Error generating news summary: {e}")
            news_summary = "Unable to generate news summary."

    return {
        "articles": [
            {
                "title": article["title"],
                "source": article["source"]["name"],
                "url": article["url"],
                "published_at": article["publishedAt"]
            }
            for article in articles
        ],
        "summary": news_summary
    }