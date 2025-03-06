import streamlit as st
import plotly.express as px
from backend import get_data

images = {"Clear": "images/clear.png",
          "Clouds": "images/cloud.png",
          "Rain": "images/rain.png",
          "Snow": "images/snow.png"}

st.title("Weather Forecast for the Next Days")
place = st.text_input("Place: ")
days = st.slider("Forecast Days", min_value=1, max_value=5,
                 help="Select the number of forecasted days")
option = st.selectbox("Select data to view",
                      ("Temperature", "Sky"))
st.subheader(f"{option} for the next {days} days in {place}")

if place:
    try:
        filtered_data = get_data(place, days)

        if option == "Temperature":
            temperatures = [d["main"]["temp"] - 273.15 for d in filtered_data]
            dates = [d["dt_txt"] for d in filtered_data]
            figure = px.line(x=dates,
                             y=temperatures,
                             labels={"x": "Date", "y": "Temperature (C)"}
                             )
            st.plotly_chart(figure)

        if option == "Sky":
            sky_conditions = [d["weather"][0]["main"] for d in filtered_data]
            st.image([images[condition] for condition in sky_conditions],
                     width=115)

    except KeyError:
        st.info("That place is unknown.")
