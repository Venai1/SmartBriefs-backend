from datetime import datetime
import requests
from openai import OpenAI

API_KEY = "57a5daf0ef4648d8b9745841b80ee252"
OPENAI_API_KEY = "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"

def get_news_summary():
    """
    Fetches financial news and generates a summary using OpenAI.
    Returns a dictionary with news articles and their summary.
    """
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # Get today's date for the news API
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Fetch news articles
    url = (f'https://newsapi.org/v2/everything?'
           f'q=finance&'
           f'from={today}&'
           f'sortBy=popularity&'
           f'apiKey={API_KEY}')
    
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
        
    # Create summary if articles were found
    news_summary = ""
    if articles:
        # Create article headlines string for the prompt
        headlines = "\n".join([f"- {article['title']} ({article['source']['name']})" 
                             for article in articles])
        
        # Generate summary using OpenAI
        summary_prompt = (
            f"Here are today's top financial news headlines:\n{headlines}\n\n"
            f"Create a brief, insightful summary of these financial headlines in 1-2 sentences. "
            f"Focus on the most important trends or events."
        )
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial assistant that summarizes news headlines."},
                    {"role": "user", "content": summary_prompt}
                ]
            )
            news_summary = response.choices[0].message.content.strip()
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