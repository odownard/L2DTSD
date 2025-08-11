from flask import Flask, render_template, g, redirect, request
import sqlite3
#render_template is used to render the content from python in order to connect it with HTML.

# This is the database for the application but I can't change the name :)
DATABASE = 'drinks.db'

#initialises app
app = Flask(__name__)

#Connects the databases to python
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Closes the database connection after the task is completed.
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Executes queries and returns results.
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    cur.row_factory = sqlite3.Row  # This makes rows behave like dictionaries
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# Try commenting out the above parts and running the app to see if it works without them^^^

cart = []
@app.route("/cart")
def view_cart():
    total_price = sum(int(item['price']) for item in cart)
    item_count = len(cart)
    # for item in cart:
    #     if item in cart:
    #         quantity = quantity + 1
    #     else:
    #         quantity = 1
    return render_template("cart.html", cart=cart, item_count=item_count, total_price=total_price)

# Routes for different pages
@app.route("/")
def home():
    #home page
    sql = "SELECT * FROM drinks"
    results = query_db(sql)
    item_count = len(cart)
    return render_template("index.html", results=results, item_count=item_count)

@app.route("/drinks")
def drinks():
    # drinks page
    sql = "SELECT * FROM drinks"
    results = query_db(sql)
    item_count = len(cart)
    return render_template("drinks.html", results=results, item_count=item_count)

@app.route("/meals")
def meals():
    sql = "SELECT * FROM meals"
    results = query_db(sql)
    item_count = len(cart)
    return render_template("meals.html", results=results, item_count=item_count)

@app.route("/snacks")
def snacks():
    sql = "SELECT * FROM snacks"
    results = query_db(sql)
    item_count = len(cart)
    return render_template("snacks.html", results=results, item_count=item_count)

# Below is the code that adds items (drinks or meals) to the cart
@app.route("/add_to_cart/<string:item_type>/<int:itemID>", methods=["POST"])
def add_to_cart(item_type, itemID):
    # Get the item details from the form
    item = request.form.get("item")
    price = request.form.get("price")
    cart.append({
        "itemID": itemID,
        "item_type": item_type,
        "item": item,
        "price": price
    })
    if item_type == "drink":
        return redirect("/drinks")
    elif item_type == "meal":
        return redirect("/meals")
    elif item_type == "snack":
        return redirect("/snacks")
    else:
        return redirect("/")
    
@app.route("/remove_cart", methods=["POST"])
def remove_cart():
    global cart # Makes the cart list a global variable instead of a local one meaning that it can connect throughout the whole website.
    cart = []
    return render_template("cart.html", cart=cart)

if __name__ == "__main__":
    app.run(debug=True)