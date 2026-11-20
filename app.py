from flask import Flask, render_template, request
import sqlite3, os

app = Flask(__name__)
DB = "gta6.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if os.path.exists(DB):
        return
    db = get_db()
    db.execute("CREATE TABLE guides (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, category TEXT, money_per_hour TEXT, description TEXT, steps TEXT)")
    db.execute("CREATE TABLE locations (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, type TEXT, area TEXT, description TEXT)")
    db.execute("INSERT INTO guides (title, category, money_per_hour, description, steps) VALUES (?,?,?,?,?)",
        ('Best Money Route - Beginner', 'Money', '25k per hour', 'Best for new players with no money', '1. Do taxi missions 2. Sell cars 3. Do first heist'))
    db.execute("INSERT INTO guides (title, category, money_per_hour, description, steps) VALUES (?,?,?,?,?)",
        ('How To Lose 5-Star Wanted', 'Police', '0', 'Escape police fast', '1. Go to swamp 2. Hide in garage 3. Change car'))
    db.execute("INSERT INTO guides (title, category, money_per_hour, description, steps) VALUES (?,?,?,?,?)",
        ('Fastest Car Location', 'Cars', '0', 'Find fastest car free', 'Go to Vice Beach parking, near blue building'))
    db.execute("INSERT INTO locations (name, type, area, description) VALUES (?,?,?,?)",
        ('Fastest Car', 'Car', 'Vice Beach', 'Parked near blue building, behind hotel'))
    db.execute("INSERT INTO locations (name, type, area, description) VALUES (?,?,?,?)",
        ('Best Gun Shop', 'Shop', 'Little Havana', 'Cheapest guns in game'))
    db.commit()
    db.close()

init_db()

@app.route("/")
def home():
    db = get_db()
    guides = db.execute("SELECT * FROM guides LIMIT 6").fetchall()
    db.close()
    return render_template("index.html", guides=guides)

@app.route("/guides")
def guides():
    q = request.args.get("q", "")
    db = get_db()
    if q:
        guides = db.execute("SELECT * FROM guides WHERE title LIKE ? OR description LIKE ? OR category LIKE ?", (f"%{q}%", f"%{q}%", f"%{q}%")).fetchall()
    else:
        guides = db.execute("SELECT * FROM guides").fetchall()
    db.close()
    return render_template("guides.html", guides=guides, q=q)

@app.route("/locations")
def locations():
    db = get_db()
    locations = db.execute("SELECT * FROM locations").fetchall()
    db.close()
    return render_template("locations.html", locations=locations)

if __name__ == "__main__":
    app.run(debug=True)