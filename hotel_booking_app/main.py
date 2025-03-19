# flake8: noqa: E501
import pandas as pd

df_hotels = pd.read_csv("hotels.csv")
df_cards = pd.read_csv("cards.csv", dtype=str)
df_security = pd.read_csv("card_security.csv", dtype=str)


class Hotel:
    def __init__(self, hotel_id: int) -> None:
        self.hotel_id = hotel_id
        self._name = df_hotels.loc[df_hotels["id"] == self.hotel_id, "name"].squeeze()  # noqa: E501
        self._city = df_hotels.loc[df_hotels["id"] == self.hotel_id, "city"].squeeze()  # noqa: E501

    def book(self):
        df_hotels.loc[df_hotels["id"] == self.hotel_id, "available"] = "no"  # noqa: E501
        df_hotels.to_csv("hotels.csv", index=False)

    def available(self) -> bool:
        availability = df_hotels.loc[df_hotels["id"] == self.hotel_id, "available"].squeeze()  # noqa: E501
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


class CreditCard:
    def __init__(self, number: str, expiration: str,
                 cvc: str, holder: str) -> None:
        self.number = number
        self.expiration = expiration
        self.cvc = cvc
        self.holder = holder.upper()

    def validate(self) -> bool:
        card_data = df_cards.loc[  # noqa: E501
            (df_cards["number"] == self.number) &  # noqa: E501
            (df_cards["expiration"] == self.expiration) &  # noqa: E501
            (df_cards["cvc"] == self.cvc) &  # noqa: E501
            (df_cards["holder"] == self.holder)  # noqa: E501
        ]
        return not card_data.empty


class SecureCreditCard(CreditCard):
    def authenticate(self, user_password: str) -> bool:
        password = df_security.loc[df_security["number"] == self.number, "password"].squeeze()  # noqa: E501
        return password == user_password


if __name__ == "__main__":
    print(df_hotels.to_string(index=False))  # noqa: E501
    hotel_id = int(input("Enter the id of the hotel: "))
    hotel = Hotel(hotel_id)
    if hotel.available():
        card_number = input("Enter your credit card number: ")
        card_expiration = input(
            "Enter your credit card expiration date (MM/YY): ")
        card_cvc = input("Enter your credit card CVC: ")
        card_holder = input("Enter the card holder name: ")

        credit_card = SecureCreditCard(
            card_number, card_expiration, card_cvc, card_holder)
        if credit_card.validate():
            password = input("Enter your password: ")
            if credit_card.authenticate(password):
                hotel.book()
                name = input("Enter your name: ")
                reservation = Reservation(hotel, name)
                print(reservation.generate())
            else:
                print("Incorrect password.")
        else:
            print("Credit card not valid.")
    else:
        print("Hotel is not available.")
