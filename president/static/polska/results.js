/**
 * Created by michal on 15.05.17.
 */

/**
 * Fill votes block.
 * @param response
 */
function fill_votes(response) {
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
    let stats_items = document.getElementsByClassName('votes')[1];
    let rows = stats_items.getElementsByTagName('tr');
    for (let i = 0; i < rows.length; i++) {
        let columns = rows[i].getElementsByTagName('td');
        if (rows.length - i > 1)
            columns[1].innerText = response.stats[i];
        else
            columns[1].innerText = response.stats[i].toFixed(2);
    }
}


/**
 * Fill topnav with unit ancestors.
 * @param response
 */
function fill_topnav(response) {
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

    if (response.results_pdf != '')
        document.getElementById('upload').innerHTML = '<h2> <a href=' + response.results_pdf + '> Protokół z wynikami obwodu </a> </h2>'

    }

/**
 * Fill all blocks with data.
 * @param response
 */
function fill_all(response) {
    fill_votes(response);
    fill_stats(response);
    fill_topnav(response);
    fill_subunits(response);
    show_pdf(response);
}

/**
 * Fill the page with unit data.
 * @param typ
 * @param short_name
 */
function fill_unit_data(typ, short_name) {
    let url = 'http://127.0.0.1:8000/polska/data/' + typ + '/' + short_name;

    let local_response = localStorage.getItem('unit_data');
    if (local_response != null)
        fill_all(JSON.parse(local_response));

    let xhr;
    xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.send();
    xhr.addEventListener("readystatechange", processRequest, false);

    function processRequest(e) {
        if (xhr.readyState == 4 && xhr.status == 200) {
            let response = JSON.parse(xhr.responseText);
            fill_all(response);
            localStorage.setItem('unit_data', xhr.responseText);
        }
    }


}
