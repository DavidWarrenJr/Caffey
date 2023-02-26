from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from operator import attrgetter

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"

db = SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    map_url = db.Column(db.String(250))
    img_url = db.Column(db.String(250))
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    coffee_price = db.Column(db.Float)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


def apply_filter(filter, cafes) -> list:
    if not filter:
        filter = "name"

    cafes.sort(key=attrgetter(filter))
    return cafes


@app.route("/")
def home():
    all_cafes = db.session.query(Cafe).all()

    filter = request.args.get("filter")
    filtered_cafes = apply_filter(filter=filter, cafes=all_cafes)


    return render_template("index.html", cafes=all_cafes, selected_filter=filter)


if __name__ == "__main__":
    app.run()
