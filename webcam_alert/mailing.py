import smtplib
import os
import imghdr
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()


def send_email(image_path: str) -> None:
    host = "smtp.gmail.com"
    port = 587

    username = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

    message = EmailMessage()
    message["Subject"] = "New Movement Alert"
    message.set_content("There was a new movement.")

    with open(image_path, "rb") as file:
        content = file.read()

    message.add_attachment(content, maintype="image",
                           subtype=imghdr.what(None, content),
                           filename=image_path)

    gmail = smtplib.SMTP(host, port)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(username, password)
    gmail.sendmail(username, receiver, message.as_string())
    gmail.quit()


if __name__ == "__main__":
    send_email("images/clear.png")
