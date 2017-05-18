
function processForm(short_name) {
    "use strict";

    let votes = document.getElementById('id_votes').value;
    let cand = document.getElementById('id_kandydat').value;

    let url = 'http://127.0.0.1:8000/polska/edit_votes_dynamic/' + short_name + '/';

    let xhr;
    xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    let csrftoken = Cookies.get('csrftoken');
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.addEventListener("readystatechange", processRequest, false);

    function processRequest() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let response = JSON.parse(xhr.responseText);
            fill_unit_data('obwód', response.name);
        }
    }

    //xhr.send(JSON.stringify({votes: votes, kandydat: cand}));
    xhr.send('votes=' + votes +'&' + 'kandydat=' + cand);
    /* do what you want with the form */

    // You must return false to prevent the default form behavior
    return false;
}

