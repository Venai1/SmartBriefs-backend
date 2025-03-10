import os
from datetime import datetime
import requests
from dotenv import load_dotenv
from helperFunctions.generate_open_ai_summary import generate_open_ai_summary

def get_news_articles_and_summary():
    """Get latest business news articles and generate a summary"""
    load_dotenv()
    # Use the top-headlines endpoint for more reliable results
    url = (f'https://newsapi.org/v2/top-headlines?'
           f'country=us&'
           f'category=business&'
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
        if response.content:
            try:
                print(response.json())
            except:
                print(response.content)
    
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
            news_summary = generate_open_ai_summary(summary_prompt)
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