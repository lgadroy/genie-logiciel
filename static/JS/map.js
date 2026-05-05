// Constantes et variable global pour les différentes fonctions. 
const width = 800;
const height = 700;
const svg = d3.select("#map");
const projection = d3.geoMercator()
.center([2.6, 46.8])
.scale(2500)
.translate([width/2, height/2]);
const path = d3.geoPath().projection(projection);

let selectedData = "propre";
let selectedDep= null;
let garesData = [];

//récupère les données des gares depuis l'API Flask (connection avec la BDD)
d3.json("/api/gares").then(function(data){
    garesData = data;
    console.log(garesData);
});

// Affichage de la carte de france avec les données geohjson des départements
d3.json("/static/data/departements.geojson").then(function(data){

    svg.selectAll("path")
        .data(data.features)
        .enter()
        .append("path")
        .attr("d", path)
        .attr("fill", "#5dade2")
        .attr("stroke", "#333")
        .on("click", function(event, d){
            let codeDep = d.properties.code;
            let garesDep = garesData.filter(g => g.cp.startsWith(codeDep));
            
            let totalVoyageurs = 0;
            let totalNonconf = 0;
            let countNonconf = 0;
            
            garesDep.forEach(g => {
                totalVoyageurs += g.voyageurs || 0;
                if(g.nonconformites != null){
                    totalNonconf += g.nonconformites;
                    countNonconf += 1;
                }
            });
            
            let moyenneNonconf = countNonconf > 0 ? (totalNonconf / countNonconf).toFixed(2) : "N/A";
            
            document.getElementById("info-Departement").innerHTML =
                "Département: " + d.properties.nom + " (" + codeDep + ")" +
                "<br>Nombre de gares avec données de propreté : " + countNonconf + "/" + garesDep.length +
                "<br>Fréquentation totale : " + totalVoyageurs.toLocaleString() +
                "<br>Taux de conformité : " + (100 - parseFloat(moyenneNonconf)) + "%";
        });

    setTimeout(() => {
        updateColorMap();
    }, 100);

});

// Fonction pour afficher les département en couleur en fonction de leur fréquentation 
// Ou de leur propréte 
// Changement de la couleur par rapport au choix de l'utilisateur.
document.querySelectorAll('input[name="donnees"]').forEach(radio =>{
    radio.addEventListener('change', function(){
        selectedData = this.value;
        updateColorMap();
    });
});

function updateColorMap(){
    let depData = getDataByDepartement();
    let propData = getPropreteByDepartement();

    d3.selectAll("path")
    .attr("fill", function(d){
        // Récupérer le code du département pour accéder aux données correspondantes
        let codeDep = d.properties.code;

        if(selectedData === "frequentation"){
            let value = depData[codeDep] || 0;
            // Si pas de données de fréquentation, colorier en gris
            if(value === 0) return "#bdc3c7";
            if(value > 10000000) return "#922b21";
            if(value > 5000000) return "#e74c3c";
            if(value > 1000000) return "#f1948a";
            return "#fadbd8";
        }

        if(selectedData === "propre"){
            let value = propData[codeDep];
            // Si pas de données de propreté, colorier en gris
            if(value === undefined) return "#bdc3c7";
            if(value < 1) return "#145a32";
            if(value < 3) return "#27ae60";
            if(value < 5) return "#82e0aa";
            return "#fadbd8"; 
        }
    });
}

function getDataByDepartement(){
    let depData = {};

    garesData.forEach(gare => {
        let dep = gare.cp.substring(0, 2); // code département

        if(!depData[dep]){
            depData[dep] = 0;
        }

        depData[dep] += gare.voyageurs;
    });

    return depData;
}

function getPropreteByDepartement(){

    let depData = {};
    let counts = {};

    garesData.forEach(gare => {
        let dep = gare.cp.substring(0, 2);

        if(gare.nonconformites == null) return;

        if(!depData[dep]){
            depData[dep] = 0;
            counts[dep] = 0;
        }

        depData[dep] += gare.nonconformites;
        counts[dep] += 1;
    });

    // moyenne
    for(let dep in depData){
        depData[dep] = depData[dep] / counts[dep];
    }

    return depData;
}