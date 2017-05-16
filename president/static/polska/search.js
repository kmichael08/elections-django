
/**
 * Write all gminy included in the response
 * @param gminy
 */
function write_gminy(gminy) {
    "use strict";
    let div_gmin = document.getElementsByClassName('subunits')[0];

     if (gminy.length === 0) {
        div_gmin.innerHTML = '<p> Brak gmin pasujących do zapytania </p>';
        return;
    }
    else {
         div_gmin.innerHTML = '<ul> </ul>';
     }

    let lista_gmin = div_gmin.getElementsByTagName('ul')[0];


    for (let i = 0; i < gminy.length; i++) {
        let gmina = gminy[i];
        lista_gmin.innerHTML += '<li><a href =' + '/polska/gmina/' + gmina.short_name + '> ' + unit_name(gmina) + '</a></li>';
    }



}

/**
 * Write all matched gminy.
 * @param gmina
 */
function get_gminy(gmina) {
    "use strict";
    let local_response = localStorage.getItem('lista_gmin');
    if (local_response !== null) {
        write_gminy(JSON.parse(local_response));
    }


    let url = 'http://127.0.0.1:8000/polska/lista_gmin/';
    let xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.addEventListener("readystatechange", processRequest, false);

    function processRequest() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let response = JSON.parse(xhr.responseText);

            write_gminy(response.gminy);

            localStorage.setItem('lista_gmin', xhr.responseText);
        }
    }

    xhr.send('gmina=' + gmina);

}