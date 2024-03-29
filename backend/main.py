from flask import request, jsonify
from config import app, db
from models import Item
#, Mob, Zone, Class, Race, ItemSlot, Stat

@app.route("/items", methods=["GET"])
def get_items():
    items = Item.query.all()
    json_items = list(map(lambda x: x.to_json(), items))
    return jsonify({"items": json_items})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)