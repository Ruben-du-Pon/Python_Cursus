import requests
import selectorlib
import time
import sqlite3
from mailing import send_email

URL = "https://programmer100.pythonanywhere.com/tours/"

connection = sqlite3.connect("data.db")


def create_table() -> None:
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        band TEXT,
        city TEXT,
        date TEXT
    )
    """)
    connection.commit()


def scrape(url: str) -> str:
    """Scrape the page source from the URL."""
    response = requests.get(url)
    source = response.text
    return source


def extract(source: str) -> str:
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def store(extracted: str):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?, ?, ?)", row)
    connection.commit()


def read(source: str) -> str:
    row = source.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",
                   (band, city, date))
    rows = cursor.fetchall()
    return rows


if __name__ == "__main__":
    create_table()
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)

        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:
                store(extracted)
                send_email(extracted)

        time.sleep(5)
