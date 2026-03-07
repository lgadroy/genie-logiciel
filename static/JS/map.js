const map=L.map('map').setView([46.8,2.5],6);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap'
}).addTo(map);

function setRegion(){
    fetch("/static/data/regions.geojson")
    .then(response => response.json()) 
    .then(data => {
        L.geoJSON(data , {
            style: {
                color: "#333",
                weight: 1,
                fillColor: "#cce5ff",
                fillOpacity: 0.7
            },
            onEachFeature: function(feature, layer) {
                layer.on({
                    click: function() {
                        alert("Région: " + feature.properties.nom);
                    }
                });
            }
        }).addTo(map);
    });
}
function setDep(){
    fetch("/static/data/departements.geojson")
    .then(response => response.json()) 
    .then(data => {
        L.geoJSON(data , {
            style: {
                color: "#333",
                weight: 1,
                fillColor: "#cce5ff",
                fillOpacity: 0.7
            },
            onEachFeature: function(feature, layer) {
                layer.on({
                    click: function() {
                        alert("Département: " + feature.properties.nom);
                    }
                });
            }
        }).addTo(map);
    });
}

document.querySelectorAll('input[name="donnees"]').forEach(radio =>{
    radio.addEventListener('change', function(){
        if(this.value === "Region"){
            setRegion();
        }
        if(this.value === "departement"){
            setDep();
        }
    });
});

setRegion();
