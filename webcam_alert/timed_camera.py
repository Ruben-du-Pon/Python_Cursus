import cv2
import streamlit as st
import time

st.title("Motion Detector")
start = st.button("Start Camera")

if start:
    streamlit_image = st.image([])
    camera = cv2.VideoCapture(0)

    while True:
        check, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        cv2.putText(img=frame,
                    text=time.strftime("%a, %d %B %Y"),
                    org=(50, 50),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.75,
                    color=(255, 125, 0),
                    thickness=2)

        cv2.putText(img=frame,
                    text=time.strftime("%H:%M:%S"),
                    org=(50, 100),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.75,
                    color=(255, 0, 0),
                    thickness=2)

        streamlit_image.image(frame)
