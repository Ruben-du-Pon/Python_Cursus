import requests
import selectorlib
import time
import sqlite3

URL = "https://programmer100.pythonanywhere.com/tours/"


class Event:
    def scrape(self, url: str) -> str:
        """Scrape the page source from the URL."""
        response = requests.get(url)
        source = response.text
        return source

    def extract(self, source: str) -> str:
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value


class Database:
    def __init__(self, database_path: str) -> None:
        self.connection = sqlite3.connect(database_path)

    def store(self, extracted: str) -> None:
        row = extracted.split(",")
        row = [item.strip() for item in row]
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES(?, ?, ?)", row)
        self.connection.commit()

    def read(self, source: str) -> list[str]:
        row = source.split(",")
        row = [item.strip() for item in row]
        band, city, date = row
        cursor = self.connection.cursor()
        cursor.execute("""
                       SELECT * FROM events WHERE band=? AND city=? AND date=?
                       """, (band, city, date))
        rows = cursor.fetchall()
        return rows


if __name__ == "__main__":
    while True:
        event = Event()
        scraped = event.scrape(URL)
        extracted = event.extract(scraped)

        if extracted != "No upcoming tours":
            db = Database("data.db")
            row = db.read(extracted)
            if not row:
                db.store(extracted)

        time.sleep(5)
