"""Flask app for Cupcakes"""
from flask import Flask, render_template, flash, redirect, request, jsonify
from models import connect_db, db, Cupcake

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cupcake_store.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "oh-so-secret"

connect_db(app)
# makes it so we could communicate with the app in a terminal
app.app_context().push()


@app.route("/")
def home():
    all_cupcakes = Cupcake.query.all()
    return render_template("index.html", all_cupcakes=all_cupcakes)


@app.route("/api/cupcakes")
def get_all_cupcakes():
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)


@app.route("/api/cupcakes/<int:id>")
def get_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes", methods=["POST"])
def add_cupcake():
    cupcake = Cupcake(
        flavor=request.json["flavor"],
        size=request.json["size"],
        rating=request.json["rating"],
        # using .get() method here in order to avoid errors in user does not send image
        # then we'll just use default image which was set up in model.py
        image=request.json.get("image"),
    )
    db.session.add(cupcake)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize()), 201


@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")


if __name__ == "__main__":
    app.run(debug=True)
