var scraperForm = document.getElementById("new-scraper-form");
var scraperTable = document.getElementById("scraper-table");
var newScraper = document.getElementById("new-scraper-btn");
var closeScraper = document.getElementById("close-scraper-btn");
var createScraper = document.getElementById("create-scraper-btn");

newScraper.onclick = function() {
    scraperForm.style.display = "block";
}

closeScraper.onclick = function() {
    scraperForm.style.display = "none";
}

// set pause button visibility
for (i = 0; i < scraperTable.rows.length; i++) {
    var row = scraperTable.rows[i];
    if (row.cells[6].innerHTML == "manual") {
        row.cells[8].getElementsByClassName("toggle-scraper-form")[0].getElementsByClassName("link-button").toggle_btn.style.display = "none";
    }
}
