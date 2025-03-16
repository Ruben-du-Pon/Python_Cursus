import pandas as pd

df = pd.read_csv("hotels.csv")


class Hotel:
    def __init__(self, hotel_id: int) -> None:
        self.hotel_id = hotel_id
        self._name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()
        self._city = df.loc[df["id"] == self.hotel_id, "city"].squeeze()

    def book(self):
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self) -> bool:
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False

    def __str__(self) -> str:
        return f"{self._name}, {self._city}."


class Reservation:
    def __init__(self, hotel: Hotel, name: str) -> None:
        self.hotel = hotel
        self.name = name

    def generate(self) -> str:
        content = f"""
        Thank you for your reservation!
        Here are your booking details:
        Name: {self.name}
        Hotel: {self.hotel}
        """
        return content


if __name__ == "__main__":
    print(df.to_string(index=False))
    hotel_id = int(input("Enter the id of the hotel: "))
    hotel = Hotel(hotel_id)
    if hotel.available():
        hotel.book()
        name = input("Enter your name: ")
        reservation = Reservation(hotel, name)
        print(reservation.generate())
    else:
        print("Hotel is not available")
