/**
 * Created by michal on 15.05.17.
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

function fill_unit_data(typ, short_name) {
    let url = 'http://127.0.0.1:8000/polska/data/' + typ + '/' + short_name;

    let xhr;
    xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.send();
    xhr.addEventListener("readystatechange", processRequest, false);

    function processRequest(e) {
        if (xhr.readyState == 4 && xhr.status == 200) {
            let response = JSON.parse(xhr.responseText);
            fill_votes(response);
            fill_stats(response);

        }
    }



}
