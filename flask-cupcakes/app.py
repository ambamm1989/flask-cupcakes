"""Flask app for Cupcakes"""

from flask import Flask, jsonify, render_templates, request

from models import connect_db, db, Cupcake

app = Flask(__name__)

app.config['SQALCHEMY_DATABASE_URL'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "sweet-secret"

connect_db(app)

@app.route("/")
def root():
    return render_templates("index.html")

@app.route("/api/cupcakes")
def list_cupcakes():
    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    data = request.json 
    cupcake = Cupcake(
        flavor = data ['flavor'],
        rating = data ['rating'],
        size = data ['size'],
        image=data ['image'] or None
    )

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.to_dict()), 201)

@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake = cupcake.to_dict())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()
    return jsonify(cupcake=cupcake.to_dict())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def remove_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_40(cupcake_id)

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")