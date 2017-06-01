/**
 * Created by michal on 15.05.17.
 */

/**
 * Fill votes block.
 * @param response
 */
function fill_votes(response) {
    "use strict";
    let votes_items = document.getElementsByClassName('votes')[0];
    let rows = votes_items.getElementsByTagName('tr');

    for (let i = 1; i < rows.length; i++) {
        let columns = rows[i].getElementsByTagName('td');
        columns[1].innerText = response.votes[i - 1];
        columns[2].innerText = response.percentage[i - 1].toFixed(2);
    }
}

/**
 * Fill block with stats.
 * @param response
 */
function fill_stats(response) {
    "use strict";
    let stats_items = document.getElementsByClassName('votes')[1];
    let rows = stats_items.getElementsByTagName('tr');
    for (let i = 0; i < rows.length; i++) {
        let columns = rows[i].getElementsByTagName('td');
        if (rows.length - i > 1) {
            columns[1].innerText = response.stats[i];
        }
        else {
            columns[1].innerText = response.stats[i].toFixed(2);
        }
    }
}


/**
 * Fill topnav with unit ancestors.
 * @param response
 */
function fill_topnav(response) {
    "use strict";
    document.getElementsByClassName('topnav')[0].innerHTML = '';
    for (let i = 0; i < response.ancestors.length; i++) {
        let link = '/polska/' + response.menu_links[i];
        document.getElementsByClassName('topnav')[0].innerHTML += '<li><a href =' + link + '> ' + unit_name(response.ancestors[i]) + '</a></li>';
    }
}

/**
 * Print all subunits into the block.
 * @param response
 */
function fill_subunits(response) {
    "use strict";
    document.getElementsByClassName('subunits')[0].getElementsByTagName('ul')[0].innerHTML = '';

    for (let i = 0; i < response.subunits.length; i++) {
        let link = '/polska/' + response.links[i];
        document.getElementsByClassName('subunits')[0].getElementsByTagName('ul')[0].innerHTML +=
            '<li><a href=' + link + '> ' + unit_name(response.subunits[i]) + '</a></li>';
    }
}

/**
 * Replace upload form with the link to the uploaded file.
 * @param response
 */
function show_pdf(response) {
    "use strict";
    if (response.results_pdf !== '' && response.is_obwod === true) {
        document.getElementById('pdf_file').innerHTML = '<h2> <a href=' + response.results_pdf + '> Protokół z wynikami obwodu </a> </h2>';
        }
    else if (response.is_obwod === true)
    {
        document.getElementById('pdf_file').innerHTML = '';
    }

    }


/**
 * Fill all blocks with data.
 * @param response
 */
function fill_all(response) {
    "use strict";
    fill_votes(response);
    fill_stats(response);
    fill_topnav(response);
    fill_subunits(response);
    show_pdf(response);
}

/**
 * Display results as a pie chart.
 * @param diagram headers and results list for the pie chart.
 */
function display_pie_chart(diagram) {
    "use strict";
    google.charts.load('current', {'packages': ['corechart']});
    google.charts.setOnLoadCallback(drawChart);
    function drawChart() {
        let data = google.visualization.arrayToDataTable(
            diagram
        );
        let options = {
            title: 'Wyniki wyborów',
            sliceVisibilityThreshold: .0
        };
        let chart = new google.visualization.PieChart(document.getElementById('piechart'));
        chart.draw(data, options);

    }
}


/**
 * Fill the page with unit data.
 * @param typ
 * @param short_name
 */
function fill_unit_data(typ, short_name) {
    "use strict";
    let key = 'unit_data';
    if (typ === 'obwód') {
        key = 'obwod_data';
    }

    key += '_' + 'typ' + '_' + short_name;

    let url = 'http://127.0.0.1:8000/polska/data/' + typ + '/' + short_name;

    let local_response = localStorage.getItem(key);
    if (local_response !== null) {
        fill_all(JSON.parse(local_response));
    }

    let xhr;
    xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.send();
    xhr.addEventListener("readystatechange", processRequest, false);

    function processRequest() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let response = JSON.parse(xhr.responseText);
            fill_all(response);

            let votes_form = document.getElementById('id_votes');
            if (votes_form !== null) {
                votes_form.value = 0;
            }

            display_pie_chart(response.diagram);

            localStorage.setItem(key, xhr.responseText);
        }
    }


}
