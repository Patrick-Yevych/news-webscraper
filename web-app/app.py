from werkzeug import datastructures
import mysql.connector, json
#sys.path.append('../')
from flask import Flask, render_template, request
from DatabaseConnection import DatabaseConnection
from GoogleScraper import GoogleScraper

app = Flask(__name__)

@app.route("/results")
def get_results():
    db = DatabaseConnection("./config.json")
    data = db.res_selectall()
    db.destroy()
    return render_template('results.html', data=data)

@app.route("/scrapers", methods=['GET', 'POST'])
def get_scrapers():
    db = DatabaseConnection("./config.json")

    if request.method == 'POST':
        query = request.values.get("search_query")
        engine = request.values.get("engine")

        if request.values.get("action_type") == "run_scraper":
            print("Running Scraper ("+query+", "+engine+")")
            max_pages = request.values.get("max_pages")
            page_step = request.values.get("page_step") 

            if engine.lower() == 'google':
                s = GoogleScraper(query, int(max_pages), int(page_step))
                db.res_insert({"search_query": query, "engine": engine, "max_pages": max_pages, "page_step": page_step}, s.build_table())

        elif request.values.get("action_type") == "delete_scraper":
            print("Deleting Scraper ("+query+", "+engine+")")
            db.scraper_delete(query, engine)

        elif request.values.get("action_type") == "create_scraper":
            max_pages = request.values.get("max_pages")
            page_step = request.values.get("page_step")
            print("Creating Scraper ("+query+", "+engine+")")
            db.scraper_insert({"search_query": query, "engine": engine, "max_pages": max_pages, "page_step": page_step})
        
    data = db.scraper_selectall()
    db.destroy()
    return render_template('scrapers.html', data=data)
    

if __name__ == "__main__":
    app.run(host="0.0.0.0")

# use bokeh for data viz