from werkzeug import datastructures
import json, math, datetime
from flask import Flask, render_template, request
from DatabaseConnection import DatabaseConnection
from GoogleScraper import GoogleScraper
from ScraperCache import ScraperCache
from PieChartView import PieChartView

scraper_cache = None

app = Flask(__name__)

@app.route("/sources")
def get_sources_view():
    return render_template('sources.html')

@app.route("/results", methods=['GET'])
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
            per_page = request.values.get("per_page")

            now = datetime.datetime.now()
            db.scraper_update_runtime(query, engine, now.strftime('%Y-%m-%d %H:%M:%S'))

            if engine.lower() == 'google':
                s = GoogleScraper(query, int(max_pages), int(page_step), int(per_page))
                db.res_insert({"search_query": query, "engine": engine}, s.build_table())

        elif request.values.get("action_type") == "toggle_scraper" and scraper_cache.get((query, engine)) != None:
            print("toggle request recieved")
            if (scraper_cache.get((query, engine))["running"] == True):
                scraper_cache.get((query, engine))["running"] = False
            else:
                scraper_cache.get((query, engine))["running"] = True

        elif request.values.get("action_type") == "delete_scraper":
            print("Deleting Scraper ("+query+", "+engine+")")
            db.scraper_delete(query, engine)
            scraper_cache.pop((query, engine))

        elif request.values.get("action_type") == "create_scraper":
            max_pages = float(request.values.get("max_pages"))
            page_step = float(request.values.get("page_step"))
            per_page = float(request.values.get("per_page"))
            run_interval_metric = request.values.get("run_interval_metric")
            
            if request.values.get("run_interval_value") != '' and run_interval_metric != 'manual':
                run_interval_value = float(request.values.get("run_interval_value"))
            else:
                run_interval_value = -1

            print(max_pages, page_step, per_page, run_interval_value, run_interval_metric)

            if (max_pages > 0 and page_step > 0 and per_page > 0 
                and max_pages % math.floor(max_pages) == 0 and page_step % math.floor(page_step) == 0 and per_page % math.floor(per_page) == 0
                and ((run_interval_value > 0 and run_interval_value % math.floor(run_interval_value) == 0) or (run_interval_value == -1 and run_interval_metric == 'manual'))):
                    print("Creating Scraper ("+query+", "+engine+")")
                    db.scraper_insert({"search_query": query, "engine": engine, 
                                       "max_pages": max_pages, "page_step": page_step, 
                                       "per_page": per_page, "run_interval_value": run_interval_value,
                                       "run_interval_metric": run_interval_metric})

                    if (run_interval_value > 0 and run_interval_value % math.floor(run_interval_value) == 0 and run_interval_metric != 'manual'):
                        scraper_cache.push((query, engine), run_interval_value, run_interval_metric)

        elif request.values.get("action_type") == "view_scraper":
            pie = PieChartView(db.sources_count(query, engine), './templates/sources.html')
            print("built pie chart for ", query, engine)

    data = db.scraper_selectall()
    for scraper in data:
        if (scraper["run_interval_metric"] == 'manual'):
            scraper["toggle_text"] = ""
        elif (scraper_cache.get((scraper["search_query"], scraper["engine"]))["running"] == True):
            scraper["toggle_text"] = "pause"
        else:
            scraper["toggle_text"] = "start"

    db.destroy()
    get_sources_view()
    return render_template('scrapers.html', data=data)
    

if __name__ == "__main__":
    scraper_cache = ScraperCache()
    app.run(host="0.0.0.0", debug=True)

# use bokeh for data viz