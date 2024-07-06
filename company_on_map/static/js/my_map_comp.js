let counter = 0;
let globalMap = 0;

ymaps.ready(init);
function init(){
    myMap = new ymaps.Map("map", {
                center: [59.94, 30.39],
                zoom: 10
            }, {
            searchControlProvider: 'yandex#search'
            });



    let req = new XMLHttpRequest();

    req.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let companies = JSON.parse(this.responseText);

            for (const comp of Object.values(companies)) {
                let object = ymaps.geocode(`${comp['addr'][0]['PROVINCE']}, ${comp['addr'][0]['CITY']}, ${comp['addr'][0]['ADDRESS_1']}`)
                object.then(function (res) {
                    let coor = res.geoObjects.properties._data.metaDataProperty.GeocoderResponseMetaData.Point.coordinates
                    myMap.geoObjects.add(new ymaps.Placemark([coor[1], coor[0]], {balloonContent: `<strong>${comp['title']}</strong>` + '\n' + `${comp['addr'][0]['PROVINCE']}, ${comp['addr'][0]['ADDRESS_1']}`}, ));
                    add_button(comp, coor)
                })
            }
        }
    };

    req.open("GET", "/company_on_map/companies");
    req.send();
    globalMap = myMap;
}


function add_button(comp, coor) {
    let target = document.getElementById("info");
    let text = get_text(comp);
    let worker = get_worker(coor);
    let finish = '<div class="c_item">' + worker + text + "</button></div>"
    target.innerHTML += finish
};

function get_worker(coor) {
    res = `<button class="c_but" onclick="centered([${coor[1]},${coor[0]}])">`
    return res
};

function centered(coor) {
    console.log(coor);
    globalMap.setCenter(coor, 15);
}

function get_text(comp) {
    return `<strong>${comp['title']}</strong>` + '<br>' + `${comp['addr'][0]['PROVINCE']}, ${comp['addr'][0]['ADDRESS_1']}`
}
