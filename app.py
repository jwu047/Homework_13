from flask import Flask, render_template
from flask import jsonify, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app)

# Route to query Mongo database and pass the mars data into an HTML template to display the data
@app.route("/")
def index():
	try:
		mars_data = mongo.db.mars_data.find_one()
		return render_template('index.html', mars_data = mars_data)
	except:
		# return the redirect
		return redirect("http://localhost:5000/scrape")

# 
@app.route("/scrape")
def scraped():
	mars_data = mongo.db.mars_data
	mars_data_scrape = scrape_mars.scrape()
	# add and update to existing
	mars_data.update({}, mars_data_scrape)
	return redirect("http://localhost:5000/")

if __name__ == "__main__":
	app.run(debug=True)