import streamlit as st
from send_email import send_email

st.header("Contact Me")

with st.form(key="contact_form"):
    user_email = st.text_input("Your email address:",
                               placeholder="Please enter your email address")
    user_message = st.text_area(
        "Your message:", placeholder="Enter your message here")
    submit_button = st.form_submit_button("Send")

    if submit_button:
        message = f"""\
Subject: Contact Form Message

From: {user_email}\nMessage:\n{user_message}
"""
        send_email(message)
        st.info("Your message has been sent.")
