"""
BFF for recipe finder frontend.
"""

from flask import Flask, request, render_template, abort
import requests
import json

with open("/config/.config.json", "r") as f:
    CONFIG = json.load(f)
    WORKER_URL = CONFIG["frontend"]["worker_url"]

app = Flask("main")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/add-recipe", methods=["GET"])
def add_recipe():
    return render_template("add_recipe.html")

@app.route("/fetch-recipes", methods=["GET"])
def fetch_recipes():
    user_input = request.args.get("user_input", type=str, default="Lasanga")
    limit = request.args.get("limit", type=int, default=5)
    resp = requests.get(f"{WORKER_URL}/get_recipes", params={"user_input":user_input, "limit":limit})
    if resp.status_code != 200: abort(500)
    return resp.json()