import mysql.connector, json, sys
sys.path.append('../')
from flask import Flask, render_template
from DatabaseConnection import DatabaseConnection

app = Flask(__name__)

@app.route("/results")
def GET_results():
    db = DatabaseConnection("../config.json")
    data = db.res_selectall()
    db.destroy()
    return render_template('results.html', data=data)

@app.route("/scrapers")
def GET_scrapers():
    db = DatabaseConnection("../config.json")
    data = db.scraper_selectall()
    db.destroy()
    return render_template('scrapers.html', data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0")

# use bokeh for data viz