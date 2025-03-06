import dotenv
import os
import requests

dotenv.load_dotenv()

APIkey = os.getenv("API_KEY")


def get_data(place: str,
             days: int = 1,) -> dict:
    """

    """
    url = "https://api.openweathermap.org/data/2.5/forecast?"\
          f"q={place}&appid={APIkey}"
    response = requests.get(url)

    data = response.json()

    # get the data for the next days
    filtered_data = data["list"]
    # filter the data per 3 hours for the number of days specified by the user
    filtered_data = filtered_data[:8*days]
    return filtered_data


if __name__ == "__main__":
    print(get_data(place="Tokyo", days=3, kind="Temperature"))
    print(len(get_data(place="Tokyo", days=3, kind="Temperature")))
