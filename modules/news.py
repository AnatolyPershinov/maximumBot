import requests


class NewsProcessor:
    token = "dd8782a265284e17b3e9d85ec46b8caa"

    def __init__(self, *args):
        message: str

    def get_news(self):
        url = f"http://newsapi.org/v2/top-headlines?country=ru&apiKey={self.token}"
        res = requests.get(url)
        return res.json()["articles"][:10]

    def format_response(self, news):
        return "\n\n".join(f"{post['title']}\nИсточник:{post['url']}" for post in news)

    def run(self):
        news = self.get_news()
        self.message = self.format_response(news)
