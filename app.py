from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_info"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def index():
    data = mongo.db.data.find_one()
    return render_template("index.html", mars=data)


@app.route("/scrape")
def scrape():
    mongo.db.data.drop()
    data = scrape_mars.scrape()
    mongo.db.data.insert_one(data)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
