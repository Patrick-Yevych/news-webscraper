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


for (i = 0; i < scraperTable.rows.length; i++) {
    // set pause button visibility
    var row = scraperTable.rows[i];
    if (row.cells[6].innerHTML == "manual") {
        row.cells[8].getElementsByClassName("toggle-scraper-form")[0].getElementsByClassName("link-button").toggle_btn.style.display = "none";
    }

    // set onclick handler
    var cellClickHandler = function(row) {
        return function() {
            var query = row.getElementsByTagName("td")[0].innerHTML;
            var engine = row.getElementsByTagName("td")[1].innerHTML;
            window.location.href = "./results/"+engine+"/"+query+".html";
        }
    }

    for (j = 0; j < row.cells.length; j++) {
        if (j != 8) {
            row.cells[j].onclick = cellClickHandler(row);
        }
    }
}
