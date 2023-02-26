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


@app.route("/")
def home():
    all_cafes = db.session.query(Cafe).all()

    selected_filter = request.args.get("filter")
    if selected_filter:
        filtered_cafes = [cafe for cafe in all_cafes if getattr(cafe, selected_filter)]
    else:
        filtered_cafes = all_cafes

    sort_by = request.args.get("sort")
    if sort_by:
        filtered_cafes.sort(key=attrgetter(sort_by))

    return render_template("index.html", cafes=filtered_cafes, selected_filter=selected_filter, sort_by=sort_by)


if __name__ == "__main__":
    app.run()
