//VARIABLES GLOBALES
const couleur_votants = ["#ffff7a", "#ffd540", "#ffa700", "#ff7000", "#ff0000", "Silver"];
const couleur_candidats = 'Indigo';
const couleur_gagnant = 'MediumSeaGreen';
const couleur_selection = 'DodgerBlue';
const couleur_font = "#ca83e0";

const desc=["Nombres de veto (candidat classé dernier)",
            "Ordre des éliminations (chaque tour, le candidat qui est le moins classé 1er est éliminé)",
            "Scores selon la règle de Copeland (1 pt par duel gagné, 0.5 pt par égalité, 0 par duel perdu)",
            "Nombres de 1er",
            "Scores selon le classement des candidats dans chaque vote",
            "Scores selon la règle de Copeland (1 pt par duel gagné, 0.5 pt par égalité, 0 par duel perdu)",
            "Défaites maximale"]

//MEMO : [veto, stv, condorcet, pluralité, borda, copeland, simpson]

var chart=null; //pour le graphique de stats



/*-----------------------------------------------------------*/
//FONCTIONS GLOBALES
//Fonction tracer un point
function tracerpoint(context, x, y, couleur, lineWidth){
  context.lineWidth=lineWidth;
  context.strokeStyle='black';
  context.fillStyle = couleur;
  context.beginPath();
  context.ellipse(x, y, 7, 7, 0, 0, Math.PI * 2);
  context.fill();
  context.stroke();
}

//Affichage de tous les votants (points)
function affichervotants(context){
  // context : context -> canvas sur lequel tracer les points
  let showDeleg = document.getElementById('showDeleg').checked;
  for (let i = 0; i < liste_xv.length; i++) {
    let x = liste_xv[i] + 10;
    let y = liste_yv[i] + 10;
    if(liste_deleg[i]) n=5;
    else var n = Math.floor(liste_poids[i]*4/Math.max(...liste_poids));
    if((n!=5)||(showDeleg&&(n==5))) tracerpoint(context, x, y, couleur_votants[n], 1);
  }
}

//Affichage de tous les candidats (points)
function affichercandidats(context){
  // context : context -> canvas sur lequel tracer les points
    for (let i = 0; i < liste_xc.length; i++) {
      let x = liste_xc[i] + 10;
      let y = liste_yc[i] + 10;
      tracerpoint(context, x, y, couleur_candidats, 2);
    }
}

//Affichage des points sur la boussole
function afficherBoussole(){
  const canvas = document.getElementById("myCanvas");
  const ctx = canvas.getContext("2d");
  ctx.reset();
  let showCand = document.getElementById('showCand').checked;
  let showVotant = document.getElementById('showVot').checked;

  if(showVotant) affichervotants(ctx);
  if(showCand) affichercandidats(ctx);
  
}

//Affichage du boutton de vote cliqué
function butt(btn){
  // btn : int -> indice de la méthode de vote
  const meth = ['buttVeto', 'buttSTV', 'buttCond', 'buttPlur', 'buttBord', 'buttCope', 'buttSimp']
	const butts = document.getElementsByClassName("butt");
  for(var i=0; i<butts.length;i++){
    butts[i].style.backgroundColor='white';
  }
	document.getElementById(meth[btn]).style.backgroundColor = 'lightgrey';
}

//Affiche un element par son id nom
function showDiv(nom) {
  //nom : str -> identifiant du div
  document.getElementById(nom).style.display = "block";
}

//Cache un element par son id nom
function hideDiv(nom) {
  //nom : str -> identifiant du div
  document.getElementById(nom).style.display = "none";
}

/*-----------------------------------------------------------*/
//AU LANCEMENT DE LA PAGE
window.onload = function() {
  const canvas = document.getElementById("myCanvas");
  const ctx = canvas.getContext("2d");
  
  ctx.lineWidth=2;
  ctx.strokeStyle='black';
  afficherBoussole(ctx);

  /*------------------------*/
  //Affichage de la satisfatcion
  var field_sat = document.getElementById("satisfaction");
  for(var i=0 ; i<liste_candidat.length ; i++){
    var nom = document.createElement('strong');
    nom.append(liste_candidat[i]+" : ");
    field_sat.append(nom);
    field_sat.append(liste_satisf[i]+" %");
    field_sat.appendChild(document.createElement('br'));
  }
  
  /*-----------------------------------------------------------*/
  //Affichage légende
  const canvas2 = document.getElementById("legende");
  const ctx2 = canvas2.getContext("2d");

  ctx2.fillStyle = 'black';
  ctx2.font = "20px Arial";
  ctx2.fillText(": candidats", 30, 20);
  tracerpoint(ctx2, 15, 15, couleur_candidats, 2);

  ctx2.fillStyle = 'black';
  ctx2.font = "20px Arial";
  ctx2.fillText(": gagnant", 30, 50);
  tracerpoint(ctx2, 15, 45, couleur_gagnant, 1);

  ctx2.fillStyle = 'black';
  ctx2.font = "20px Arial";
  ctx2.fillText(": vote délégué", 30, 80);
  tracerpoint(ctx2, 15, 75, "silver", 1);


  //Affichage scale
  const canvas3 = document.getElementById("scale");
  const ctx3 = canvas3.getContext("2d");

  ctx3.fillStyle = 'black';
  ctx3.font = "20px Arial";
  ctx3.fillText("Poids des votants:", 30, 20);
  for(let i=0;i<5;i++){
    ctx3.fillStyle=couleur_votants[i];
    ctx3.fillRect(30+i*30,30,30,30);
    ctx3.fillStyle = 'black';
    ctx3.fillText(i+1, 40+i*30, 80);
  }
}


/*-----------------------------------------------------------*/
//AFFICHAGE EN FONCTION DES MÉTHODES DE VOTE
/*MEMO:
  - ordre des méthodes dans la liste reçu: [veto, stv, condorcet, pluralité, borda, copeland, simpson]
*/

function methode(methode){
  document.getElementById("description_meth_vote").innerHTML=desc[methode]; //affichage d'une courte description de la méthode
  document.getElementById("canvas_elu").getContext("2d").reset(); //reset du point gagnant
  
  if(methode == 1){ //affichage pour stv
    hideDiv("list_stats");
    document.getElementById("canvas_selection").getContext("2d").reset();
    showDiv("stv");
    var cand='';
    for(let i=0; i<liste_candidat.length-1;i++){
      cand+="Eliminé au tour "+(i+1)+" : "+liste_resultats_votes[1][i];
      cand+="<br>";
    }
    document.getElementById("stv_list").innerHTML=cand;

  }else{
    hideDiv("stv");
    showDiv("list_stats");
    indice = 0; //variable globale déclaré dans les statistiques
    affiche_stats(methode);
    
    drawGraphe(methode);
  }

  butt(methode); //affiche du boutton de la méthode clické.
  //affichage du candidat élu en fonction de la méthode methode
  const canvas = document.getElementById("canvas_elu");
  const ctx = canvas.getContext("2d");
  tracerpoint(ctx, liste_resultats[methode][0]+10, liste_resultats[methode][1]+10, couleur_gagnant, 2);
  if(liste_resultats[methode][2]!='n') document.getElementById("res").innerHTML=liste_resultats[methode][2];
  else document.getElementById("res").innerHTML="Aucun candidat élu";
}


/*-----------------------------------------------------------*/
//AFFICHAGE DES STATISTIQUES POUR LES FONCTIONS NÉCESSAIRES
var indice = 0; //Candidats actuellement selectionné

//Choisir le candidat précédent
function gauche(){
  document.getElementById("statistiques").childNodes[indice].style.color = couleur_font;
  if(indice>0) indice--;
  else indice = liste_candidat.length-1;
  selection();
}

//Choisir le candidat suivant
function droite(){
  document.getElementById("statistiques").childNodes[indice].style.color = couleur_font;
  if(indice<liste_candidat.length-1) indice++;
  else indice=0;
  selection();
}

//Affichage des stastistiques en fonction de la méthode de vote choisie
function affiche_stats(n){
  // n : int -> numéro de la méthode de vote
  var stats = document.getElementById("statistiques");

  //reset de l'élément d'affichage des statistique sur la page html
  while(stats.childNodes.length>0){
    stats.removeChild(stats.lastChild);
  }

  //boucle d'affichage des stats de chaque candidat
  for(let i=0; i<liste_candidat.length;i++){
    var nom = document.createElement('div');
    nom.append(liste_candidat[i]+" : "+liste_resultats_votes[n][i]);
    stats.appendChild(nom);
  }
  
  selection();
}

//Affichage du candidat selectionné
function selection(){
  //affichage du nom du candidat selectionné
  document.getElementById("nom_candidat").innerHTML=liste_candidat[indice];

  //reset de la canvas de selection + point du candidat selectionné en rouge après
  var canvas = document.getElementById("canvas_selection");
  var ctx = canvas.getContext("2d");
  ctx.reset();
  tracerpoint(ctx, liste_xc[indice]+10, liste_yc[indice]+10, couleur_selection, 2);

  //mise en couleur du candidat selectionné
  var stats = document.getElementById("statistiques");
  stats.childNodes[indice].style.color = couleur_selection;
}

//Affichage du graphe de statisitques
function drawGraphe(n){
  var xValues = liste_candidat;
  var yValues = liste_resultats_votes[n];
  var barColors = ["red", "green","blue","orange","brown", "yellow", "pink", "purple", "lightgreen", "lightblue", "turquoise", "violet", "lime" , "deeppink" , "teal"];


  //reset du graphe
  if(chart) chart.destroy();

  //echelle des bars du graphe
  let max_echelle=0;
  if(n==2){
    max_echelle=xValues.length-1;
  } else {
    max_echelle=Math.max(...liste_resultats_votes[n]);
  }

  //Création du nouveau graphe
  chart = new Chart("graphe", {
    type: "horizontalBar",
    data: {
    labels: xValues,
    datasets: [{
      backgroundColor: barColors,
      data: yValues
    }]
  },
    options: {
      legend: {display: false},
      title: {
        display: true,
        text: ""
      },
      scales: {
        xAxes: [{ticks: {min: 0, max:max_echelle}}]
      }
    }
  });

}