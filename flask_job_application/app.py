from static.models import db, Form
from flask import Flask, render_template, request, flash
from datetime import datetime


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "the_most_secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app


app = create_app()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_object = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]

        form = Form(first_name=first_name, last_name=last_name,
                    email=email, date=date_object, occupation=occupation)
        db.session.add(form)
        db.session.commit()
        flash("Form submitted successfully.", "success")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
