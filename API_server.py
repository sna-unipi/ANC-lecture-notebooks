import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request

app = Flask(__name__)
app.config["SECRET_KEY"] = "4YrzfpQ4kGXjuP6w"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

def create_db():
    with open("data/network.csv") as f:
        for line in f:
            uid, vid = line.strip().split(",")
            graph = Graph(uid=uid, vid=vid)
            db.session.add(graph)
        db.session.commit()


class Graph(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(15), nullable=False)
    vid = db.Column(db.String(15), nullable=False)

@app.route("/random_node", methods=["GET"])
def random_node():
    """
    Get a random node.

    :return: a json object
    """

    node = Graph.query.order_by(db.func.random()).first()
    return json.dumps({"status": 200, "node": node.uid})

@app.route("/friends", methods=["POST"])
def get_friends():
    """
    Get friends ids.

    :return: a json object
    """

    data = json.loads(request.get_data())
    uid = data["uid"]
    page = int(data["page"])

    if page < 1:
        page = 1

    nodes = []

    try:
        friends = Graph.query.filter_by(uid=uid).paginate(page=page, per_page=5)
        for node in friends.items:
            nodes.append(node.vid)
    except:
        pass

    return json.dumps({"status": 200, "friends": nodes})


if __name__ == "__main__":
    db.session.query(Graph).delete()
    create_db()
    app.run(debug=True)
