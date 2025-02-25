import streamlit as st
from send_email import send_email

st.header("Contact Me")

with st.form(key="contact_form"):
    user_email = st.text_input("Your email address:",
                               placeholder="Please enter your email address")
    user_topic = st.selectbox("What topic do you want to discuss?",
                              ["Job Inquiries",
                               "Project Proposals",
                               "Other"])
    user_message = st.text_area(
        "Your message:", placeholder="Enter your message here")
    message = f"""\
Subject: Contact Form Message from {user_email} about {user_topic}

From: {user_email}
Topic: {user_topic}\n
Message:\n{user_message}
"""
    submit_button = st.form_submit_button("Send")

    if submit_button:
        send_email(message)
        st.info("Your message has been sent.")
