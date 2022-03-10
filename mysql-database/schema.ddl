DROP TABLE IF EXISTS Results;
DROP TABLE IF EXISTS Scrapers;

CREATE TABLE Scrapers(
    search_query VARCHAR(100),
    engine VARCHAR(10),
    max_pages INTEGER NOT NULL CHECK (max_pages >= 0),
    page_step INTEGER NOT NULL CHECK (page_step >= 0),
    per_page INTEGER NOT NULL CHECK (per_page >= 0),
    run_interval_value INTEGER NOT NULL,
    run_interval_metric VARCHAR(6) NOT NULL,
    last_run DATETIME,
    PRIMARY KEY (search_query, engine)
);

CREATE TABLE Results(
    headline VARCHAR(500),
    source VARCHAR(100),
    url VARCHAR(300),
    published_date DATE,
    search_query VARCHAR(100),
    engine VARCHAR(10),
    PRIMARY KEY (headline, source),
    FOREIGN KEY (search_query, engine) REFERENCES Scrapers (search_query, engine) ON DELETE CASCADE
);