import openai
import requests
from news_api_key import api_key

url = f"https://newsapi.org/v2/top-headlines?country=si&apiKey={api_key}"

# API: https://newsapi.org/s/slovenia-news-api
class GetArticles:
    def __init__(self, url):
        self.url = url
        self.res = requests.get(url)
        self.article_urls = ""

    # List authors
    def list_authors(self, data):
        authors = []
        for article in data["articles"]:
            authors.append(article['author'])

        return authors

    # List titles
    def list_titles(self, data):
        titles = []
        for article in data["articles"]:
            titles.append(article["title"].split("-")[0])
        return titles

    def get_dates(self, data):
        dates = []
        for article in data["articles"]:
            dates.append(article["publishedAt"])
        return dates
    
    def get_urls(self, data):
        urls = []
        for article in data["articles"]:
            urls.append(article["url"])

    def author_title_list(self):
        if (self.res.status_code == 200):
            data = self.res.json()

            # Get important features
            authors = self.list_authors(data)
            titles = self.list_titles(data)
            dates = self.get_dates(data)
            self.article_urls = self.get_urls(data)
            
            for a in range(len(authors)):
                print(f"{authors[a]}: {titles[a]} ({dates[a]})")
        else:
            print("Error", self.res.status_code)


    def get_article_from_url(self):
        # TODO: get article from url in the object

        pass

if __name__ == "__main__":
    ga = GetArticles(url)
    ga.author_title_list()
