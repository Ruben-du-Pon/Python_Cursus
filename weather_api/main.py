import pandas as pd
import numpy as np
from flask import Flask, render_template  # , request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/v1/<station>/<date>")
def api(station, date):
    filename = "TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv("data/" + filename, skiprows=20, parse_dates=["    DATE"])
    df['TG0'] = df['   TG'].mask(df[' Q_TG'] != 0, np.nan)
    df['TG'] = df['TG0'] / 10
    temperature = df.loc[df['    DATE'] == date]['TG'][0]
    return {"station": station, "date": date, "temperature": temperature}


if __name__ == "__main__":
    app.run(debug=True)
