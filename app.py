from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

#setting up Flask
app = Flask(__name__)

#We  need to tell Python how to connect to Mongo using PyMongo. Next, add
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#app.config["MONGO_URI"] tells Python that our app will connect to Mongo using a URI, 
# a uniform resource identifier similar to a URL.
#"mongodb://localhost:27017/mars_app" is the URI we'll be using to connect our app to Mongo. 
# This URI is saying that the app can reach Mongo through our localhost server, using port 27017,
#  using a database named "mars_app".

#Define the routes for the HTML page
@app.route("/")         #sets up homgpage
def index():
    mars =mongo.db.mars.find_one()              #uses pymongo to find the 'mars' collection in our database. Assingning that path to mars variable for later.
    return render_template("index.html", mars=mars)             #tells flask to return an HTML template using an index.html file. we'll create this file after the routes are created

    #MArs = mars tells python to use the 'mars' collection in mongoDB

#adding next route that will scrape the web with a 'button'
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)
if __name__ == "__main__":
   app.run(debug=True)