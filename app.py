from flask import Flask, render_template, request
import datetime
from pymongo import MongoClient
import os 
from dotenv import load_dotenv
load_dotenv()

def create_app():
    app = Flask(__name__)
    MONGO_URL = os.environ.get("MONGO_URL")
    mongo_client= MongoClient(MONGO_URL)
    db = mongo_client["microblog"]
    collection = db["entries"]

    @app.route("/", methods = ["POST", "GET"])
    def home():

        if request.method == "POST":
            entry_content = request.form.get("content")
            collection.insert_one({"content":entry_content , "time":datetime.datetime.now().strftime("%Y-%m-%d")})
        
        collection_contents = collection.find({})
        past_entries = [(entry["content"], entry["time"], datetime.datetime.strptime(entry["time"], "%Y-%m-%d").strftime("%b %d")) for entry in collection_contents]
        return render_template("home.html", entries = past_entries)
    
    return app

#app = create_app()
#app.run(port=8089)