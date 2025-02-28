import requests
import os
from dotenv import load_dotenv
from send_email import send_email

load_dotenv()

topic = "tech"
api_key = os.getenv("API_KEY")
url = "https://newsapi.org/v2/everything?" \
      f"q={topic}&" \
      "sortBy=publishedAt&" \
      f"apiKey={api_key}&" \
      "language=en"

response = requests.get(url)
content = response.json()

articles = content["articles"][:20]

email_body = ""
for article in articles:
    email_body = email_body + article["title"] + "\n" + \
        article["description"] + "\n" + article["url"] + 2*"\n"

email_body = email_body.encode("utf-8")

message = f"""\
Subject: US Business News

{email_body}
"""

send_email(message)
