from flask import Flask, render_template  # , request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/v1/<station>/<date>")
def api(station, date):
    return {"station": station, "date": date}


if __name__ == "__main__":
    app.run(debug=True)
