from flask import Flask, render_template, request, redirect, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = "secret-key"

SERVICES_FILE = "services.json"
USERS_FILE = "users.json"

# -------------------------
# Helpers
# -------------------------

def load_services():
    with open(SERVICES_FILE, "r") as f:
        return json.load(f)

def save_services(data):
    with open(SERVICES_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

# -------------------------
# Routes
# -------------------------

@app.route("/")
def home():
    if "user" in session:
        return redirect("/map")
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()

        for u in users:
            if u["username"] == username and u["password"] == password:
                session["user"] = username
                return redirect("/map")

        return render_template("login.html", error="Invalid login")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/map")
def map_page():
    if "user" not in session:
        return redirect("/login")

    return render_template("map.html")

@app.route("/services")
def get_services():
    return jsonify(load_services())

@app.route("/add", methods=["POST"])
def add_service():
    if "user" not in session:
        return "Unauthorized", 401

    services = load_services()

    new_id = max([s["id"] for s in services]) + 1 if services else 1

    new_service = {
        "id": new_id,
        "name": request.form["name"],
        "city": request.form["city"],
        "category": request.form["category"],
        "emoji": request.form["emoji"],
        "lat": float(request.form["lat"]),
        "lng": float(request.form["lng"]),
        "description": request.form["description"],
        "website": request.form["website"]
    }

    services.append(new_service)
    save_services(services)

    return redirect("/map")

@app.route("/delete/<int:id>")
def delete_service(id):
    services = load_services()
    services = [s for s in services if s["id"] != id]
    save_services(services)

    return redirect("/map")

@app.route("/cities")
def get_cities():
    services = load_services()
    cities = sorted(list(set([s["city"] for s in services])))
    return jsonify(cities)

if __name__ == "__main__":
    app.run(debug=True)