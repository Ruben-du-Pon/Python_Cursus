import streamlit as st
import plotly.express as px
from backend import get_data
from datetime import datetime

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
            dates = [d["dt_txt"] for d in filtered_data]

            # Process 8 items at a time (one day = 8 three-hour intervals)
            for i in range(0, len(sky_conditions), 8):
                # Get the next 8 items (or remaining items if less than 8)
                day_conditions = sky_conditions[i:i + 8]
                day_dates = dates[i:i + 8]

                # Create 8 columns for this row
                cols = st.columns(8)

                # Fill the columns with available data
                for col, condition, date in zip(cols,
                                                day_conditions,
                                                day_dates):
                    with col:
                        st.image(images[condition], width=115)

                        time_string = datetime.strptime(
                            date, "%Y-%m-%d %H:%M:%S").strftime("%d-%m %H:%M")
                        st.markdown("<span style='font-size: 0.75em;"
                                    "font-weight: bold;'>"
                                    f"{time_string}</span>",
                                    unsafe_allow_html=True)

                # Add some spacing between rows
                st.write("")

    except KeyError:
        st.info("That place is unknown.")
