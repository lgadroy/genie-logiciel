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
let selectedYear = "2022";

//récupère les données des gares depuis l'API Flask (connection avec la BDD)
function loadGaresData() {
    d3.json(`/api/gares?annee=${selectedYear}`).then(function(data){
        garesData = data;
        updateColorMap();
        drawLegend();
    });
}

loadGaresData();

// Affichage de la carte de france avec les données geojson des départements
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
            let pourcentageProptrete = moyenneNonconf !== "N/A" ? (100 - moyenneNonconf).toFixed(2) : "N/A";
            
            let infoText = "Département: " + d.properties.nom +
                "<br>Nombre de gares: " + garesDep.length;
            
            if(selectedData === "frequentation"){
                infoText += "<br>Nombre de visiteurs: " + totalVoyageurs.toLocaleString();
            } else if(selectedData === "propre"){
                infoText += "<br>Pourcentage de propreté: " + pourcentageProptrete + "%";
            }
            
            document.getElementById("info-Departement").innerHTML = infoText;
        });
    
    drawLegend();

});

// Fonction pour afficher les département en couleur en fonction de leur fréquentation 
// Ou de leur propréte 
// Changement de la couleur par rapport au choix de l'utilisateur.
document.querySelectorAll('input[name="donnees"]').forEach(radio =>{
    radio.addEventListener('change', function(){
        selectedData = this.value;
        updateColorMap();
        drawLegend();
    });
});

// Écouteur pour le changement d'année
document.getElementById('annee').addEventListener('change', function(){
    selectedYear = this.value;
    loadGaresData();
});

function updateColorMap(){
    let depData = getDataByDepartement();
    let propData = getPropreteByDepartement();

    d3.selectAll("path")
    .attr("fill", function(d){

        let codeDep = d.properties.code;

        if(selectedData === "frequentation"){
            let value = depData[codeDep] || 0;
            if(value === 0) return "#bdc3c7";
            if(value > 10000000) return "#922b21";
            if(value > 5000000) return "#e74c3c";
            if(value > 1000000) return "#f1948a";
            return "#fadbd8";
        }

        if(selectedData === "propre"){
            let value = propData[codeDep] || 0;
            if(value === 0) return "#bdc3c7";
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

function drawLegend(){
    // Supprimer l'ancienne légende s'il en existe une
    d3.select("#legend").remove();
    
    const legendX = width - 250;
    const legendY = 20;
    const legendItemHeight = 30;
    
    const legend = svg.append("g")
        .attr("id", "legend")
        .attr("transform", `translate(${legendX}, ${legendY})`);
    
    // Fond de la légende
    legend.append("rect")
        .attr("width", 230)
        .attr("height", selectedData === "frequentation" ? 160 : 140)
        .attr("fill", "white")
        .attr("stroke", "#333")
        .attr("stroke-width", 1)
        .attr("rx", 4);
    
    // Titre de la légende
    legend.append("text")
        .attr("x", 115)
        .attr("y", 20)
        .attr("text-anchor", "middle")
        .attr("font-weight", "bold")
        .attr("font-size", "12px")
        .text(selectedData === "frequentation" ? "Fréquentation" : "Propreté");
    
    if(selectedData === "frequentation"){
        const frequentationLegend = [
            { color: "#922b21", label: "> 10 millions" },
            { color: "#e74c3c", label: "> 5 millions" },
            { color: "#f1948a", label: "> 1 million" },
            { color: "#fadbd8", label: "< 1 million" }
        ];
        
        frequentationLegend.forEach((item, i) => {
            legend.append("rect")
                .attr("x", 15)
                .attr("y", 30 + i * legendItemHeight)
                .attr("width", 15)
                .attr("height", 15)
                .attr("fill", item.color)
                .attr("stroke", "#333")
                .attr("stroke-width", 0.5);
            
            legend.append("text")
                .attr("x", 35)
                .attr("y", 42 + i * legendItemHeight)
                .attr("font-size", "11px")
                .text(item.label);
        });
    } else {
        const propreteteLegend = [
            { color: "#145a32", label: "> 99%" },
            { color: "#27ae60", label: "97-99" },
            { color: "#82e0aa", label: "95-97%" },
            { color: "#fadbd8", label: "< 95%" }
        ];
        
        propreteteLegend.forEach((item, i) => {
            legend.append("rect")
                .attr("x", 15)
                .attr("y", 30 + i * legendItemHeight)
                .attr("width", 15)
                .attr("height", 15)
                .attr("fill", item.color)
                .attr("stroke", "#333")
                .attr("stroke-width", 0.5);
            
            legend.append("text")
                .attr("x", 35)
                .attr("y", 42 + i * legendItemHeight)
                .attr("font-size", "11px")
                .text(item.label);
        });
    }
}