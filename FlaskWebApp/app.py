from flask import Flask, request, jsonify

app = Flask(__name__)

# in-memory database
items = []

# Get all items
@app.route("/api/v1/item", methods=["GET"])
def get_all_items():
    global items
    return jsonify(items)

# Get item with id from query param
@app.route("/api/v1/item/<int:id>", methods=["GET"])
def get_item(id):
    global items
    print(items)
    for item in items:
        print(item)
        if item["id"] == id:
            return jsonify(item)
    return jsonify({"status":404, "errormessage":"item not found"})

# Create an item
@app.route("/api/v1/item", methods=["POST"])
def post_item():
    global items
    item = request.json
    items.append(item)
    return jsonify({"status":200, "errormessage":"item added"})

# Delete an item with given ID
@app.route("/api/v1/item/<int:id>", methods=["DELETE"])
def delete_item(id):
    global items
    for item in items:
        if item["id"] == id:
            items.remove(item)
            return jsonify({"status":200, "errormessage":"item deleted"})
    return jsonify({"status":404, "errormessage":"item not found"})

# Update an item with given ID
@app.route("/api/v1/item/<int:id>", methods=["PATCH"])
def update_item(id):
    global items
    item_index = -1
    for index, item in enumerate(items):
        if item["id"] == id:
            item_index = index
            break
    if item_index == -1:
        return jsonify({"status":404, "errormessage":"item not found"})
    
    new_item = request.json
    items[item_index] =  new_item
    return jsonify({"status":200, "errormessage":"item updated"})

if __name__=="__main__":
    app.run(host='0.0.0.0', port=8080, debug=True,threaded=True)
    