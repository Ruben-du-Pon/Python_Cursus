# import smtplib
# import os
# from dotenv import load_dotenv
# from email.message import EmailMessage

# load_dotenv()


# def send_email(tour: str) -> None:
#     host = "smtp.gmail.com"
#     port = 587

#     username = os.getenv("EMAIL_USERNAME")
#     password = os.getenv("EMAIL_PASSWORD")
#     receiver = os.getenv("EMAIL_RECEIVER")

#     message = EmailMessage()
#     message["Subject"] = "New Tour Alert"
#     message.set_content("New upcoming tour:\n" + tour)

#     gmail = smtplib.SMTP(host, port)
#     gmail.ehlo()
#     gmail.starttls()
#     gmail.login(username, password)
#     gmail.sendmail(username, receiver, message.as_string())
#     gmail.quit()


def send_email(tour: str) -> None:
    print("New upcoming tour:\n" + tour)
