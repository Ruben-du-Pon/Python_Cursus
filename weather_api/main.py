import pandas as pd
import numpy as np
from flask import Flask, render_template, redirect, url_for  # , request

app = Flask(__name__)

stations = pd.read_csv("data/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]
stations.columns = ["ID", "Name"]


@app.route("/")
def index():
    return render_template("index.html", data=stations.to_html(index=False))


@app.route("/api/v1/<station>/<date>")
def api(station, date):
    if len(date) == 4:
        return redirect(url_for('yearly', station=station, year=date))
    filename = "TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv("data/" + filename, skiprows=20, parse_dates=["    DATE"])
    df['TG0'] = df['   TG'].mask(df[' Q_TG'] != 0, np.nan)
    df['TG'] = df['TG0'] / 10
    temperature = df.loc[df['    DATE'] == date]['TG'][0]
    return {"station": station, "date": date, "temperature": temperature}


@app.route("/api/v1/<station>")
def all_data(station):
    filename = "TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv("data/" + filename, skiprows=20, parse_dates=["    DATE"])
    df['TG0'] = df['   TG'].mask(df[' Q_TG'] != 0, np.nan)
    df['TG'] = df['TG0'] / 10
    result = df.to_dict(orient="records")
    return result


@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station, year):
    filename = "TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv("data/" + filename, skiprows=20)
    df['TG0'] = df['   TG'].mask(df[' Q_TG'] != 0, np.nan)
    df['TG'] = df['TG0'] / 10
    df['    DATE'] = df['    DATE'].astype(str)
    df = df[df['    DATE'].str.startswith(str(year))]
    result = df.to_dict(orient="records")
    return result


if __name__ == "__main__":
    app.run(debug=True)
