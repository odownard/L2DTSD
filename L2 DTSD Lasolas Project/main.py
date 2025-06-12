from flask import Flask, render_template, g
import sqlite3
#render_template is used to render the content from python in order to connect it with HTML.

DATABASE = 'menu.db'

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

@app.route("/")
def home():
    #home page
    sql = "SELECT * FROM pictures"
    results = query_db(sql)
    return render_template("index.html",results=results)
    
if __name__ == "__main__":
    app.run(debug=True)