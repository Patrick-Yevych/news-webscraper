var scraper_index = 0;

function set_new_visibility() {
    if (document.getElementById("new-scraper-form").style.display == "none") {
        document.getElementById("new-scraper-form").style.display = "block";
    }
    else {
        document.getElementById("new-scraper-form").style.display = "none";
    }
}
function set_pause_visibility() {
    for (i = 0; i < document.getElementById("scraper-table").rows.length; i++) {
        var row = document.getElementById("scraper-table").rows[i];
        if (row.cells[6].innerHTML == "manual") {
            row.cells[8].getElementsByClassName("toggle-scraper-form")[0].getElementsByClassName("link-button").toggle_btn.style.display = "none";
        }
    }
}