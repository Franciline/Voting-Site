const couleur_font = '#ca83e0';
const couleur_votants = "lightCyan";
const couleur_candidats = 'yellow';
const couleur_comite = 'MediumSeaGreen';
const couleur_selection = 'Red';

/*-----------------------------------------------------------------*/
//FONCTIONS GLOBALES

//Fonction tracer un point
function tracerpoint(context, x, y, couleur, lineWidth){
  /*context : context -> canvas sur lequel tracer les points
    x : int ; y : int -> coordonnées x et y
    couleur : str -> couleur du point
    lineWidth : int -> épaisseur du bord du point
  */
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
  for (let i = 0; i < liste_xv.length; i++) {
    let x = liste_xv[i] + 10;
    let y = liste_yv[i] + 10;
    tracerpoint(context, x, y, couleur_votants, 1);
  }
}

//Affichage de tous les candidats (points)
function affichercandidats(context){
  // context : context -> canvas sur lequel tracer les points
  for (let i = 0; i < liste_candidat.length; i++) {
    let x = liste_candidat[i][1] + 10;
    let y = liste_candidat[i][2] + 10;
    tracerpoint(context, x, y, couleur_candidats, 2);
  }
}

//Affichage des points sur la boussole
function afficherBoussole(){
  const canvas = document.getElementById("myCanvas");
  const ctx = canvas.getContext("2d");
  ctx.reset();
  let showCand = (document.getElementById('showCand').checked);
  let showVotant = (document.getElementById('showVot').checked);

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



/*-----------------------------------------------------------*/
//AU LANCEMENT DE LA PAGE
window.onload = function() {
  const canvas = document.getElementById("myCanvas");
  const ctx = canvas.getContext("2d");
  
  ctx.lineWidth=2;
  ctx.strokeStyle='black';
  afficherBoussole(ctx);  //traçage des points sur la boussole

  
  /*------------------------*/
  //Affichage points de la légende
  const canvas2 = document.getElementById("legende");
  const ctx2 = canvas2.getContext("2d");

  ctx2.fillStyle = 'black';
  ctx2.font = "20px Arial";
  ctx2.fillText(": candidats", 30, 20);
  tracerpoint(ctx2, 15, 15, couleur_candidats, 2);

  ctx2.fillStyle = 'black';
  ctx2.font = "20px Arial";
  ctx2.fillText(": électeurs", 30, 50);
  tracerpoint(ctx2, 15, 45, couleur_votants, 1);
  

  /*-------------------------*/
  //Affichage de la liste de tous les candidats (à gauche de la page)
  var field_candidats = document.getElementById('liste_candidats');
  affiche_comite(field_candidats, liste_candidat);



  /*-------------------------*/
  //AFFICHAGE CONTRAINTES GLOBALES
  var field_glob = document.getElementById('contraintes_glob');
  if(liste_cont_glob[0].length==0 && liste_cont_glob[1].length==0) field_glob.append('Aucune contrainte globale');
  else{
    //Contrainte globale pour la parité
    if(liste_cont_glob[0].length==2){ 
      var bold = document.createElement('strong');
      bold.append("Parité :");
      field_glob.appendChild(bold);
      field_glob.append(' Homme : '+ (Number(liste_cont_glob[0][0])*100) + '% ,');
      field_glob.append(' Femme : '+ (Number(liste_cont_glob[0][1])*100) + '%');
      field_glob.appendChild(document.createElement('br'));
    }
    //Contrainte globale sur la distance
    if(liste_cont_glob[1].length==2){ 
      var bold = document.createElement('strong');
      bold.append("Distance :");
      field_glob.appendChild(bold);
      field_glob.append(' Minimale : '+ liste_cont_glob[1][0]);
      field_glob.append(' , Maximale : '+ liste_cont_glob[1][1]);
    }
  }


  /*-------------------------*/
  //AFFICHAGE DES CONTRAINTES INDIVIDUELLES
  //document.getElementById('machin').innerHTML = liste_cont_ind;
  var field_ind = document.getElementById('contraintes_ind');
  const attributs = ['Nom', 'Coordonnée x', 'Coordonnée y', 'Visibilité', 'Sexe', 'Age'];
  
  for(var i in liste_cont_ind){
    //creer une contrainte
    var contrainte = document.createElement('div');
    contrainte.style.width = '250px';
    contrainte.style.border = 'solid';
    contrainte.style.margin = "0px 0px 5px 0px";
    contrainte.style.padding = "5px 5px 5px 10px"
  
    var titre = document.createElement('strong');
    titre.append('Contraintes '+(Number(i)+1));
    titre.style.textDecoration = "underline";
    contrainte.appendChild(titre);
    contrainte.appendChild(document.createElement('br'));
    
    //Affichage pour les contrainte sur le nom, les coordonnées x et y, la visibilité
    for(var j=0;j<4;j++){
      var bold = document.createElement('strong');
      bold.append(attributs[j]+' : ');
      contrainte.appendChild(bold);
      contrainte.append('['+liste_cont_ind[i][j]+']');
      contrainte.appendChild(document.createElement('br'));
    }

    //Affichage pour la contrainte sur le sexe
    var sexe = '';
    if(liste_cont_ind[i][4]=='N') sexe = "Neutre";
    else if(liste_cont_ind[i][4]=='F') sexe = 'Femme';
    else if(liste_cont_ind[i][4]=='H') sexe = 'Homme';
    var bold = document.createElement('strong');
    bold.append(attributs[4]+' : ');
    contrainte.appendChild(bold);
    contrainte.append(sexe);
    contrainte.appendChild(document.createElement('br'));

    //Affichage pour la contrainte sur l'age
    bold = document.createElement('strong');
    bold.append(attributs[5]+' : ');
    contrainte.appendChild(bold);
    contrainte.append('['+liste_cont_ind[i][5]+']');
    contrainte.appendChild(document.createElement('br'));

    field_ind.appendChild(contrainte);
  }

}



/*-----------------------------------------------------------------*/
//AFFICHAGE EN FONCTION DES MÉTHODES DE VOTE
/*MEMO:
  - ordre des méthodes dans la liste reçu: [veto, stv, condorcet, pluralité, borda, copeland, simpson]
*/

//Affichage des trois comités possibles en fonction de la méthode
function afficherComiteElu(methode){ 
  //methode : int -> indice dans la liste des comites élus
  var field_comite = document.getElementById('comite_elu');
  var field_comite2 = document.getElementById('comite2');
  var field_comite3 = document.getElementById('comite3');
  const liste_elus = liste_gagnants[methode];

  butt(methode);

  //reset fieldset comite
  while(field_comite.lastChild!=field_comite.childNodes[2]){
    field_comite.removeChild(field_comite.lastChild);
  }
  //reset fieldset comite 2
  while(field_comite2.lastChild!=field_comite2.childNodes[2]){
    field_comite2.removeChild(field_comite2.lastChild);
  }
  //reset fieldset comite 3
  while(field_comite3.lastChild!=field_comite3.childNodes[2]){
    field_comite3.removeChild(field_comite3.lastChild);
  }
  //reset fieldset liste candidats
  for(var e of document.getElementById('liste_candidats').querySelectorAll('div')){
    e.style.fontWeight = 'normal';
    e.style.color = couleur_font;
  }
  //reset canvas de selection
  document.getElementById("canvas_comite").getContext("2d").reset();
  document.getElementById("canvas_selection").getContext("2d").reset();


  //Affichage du premier comité (gagnant)
  if(liste_elus[0].length == 0){
    var paragraph = document.createElement('p');
    paragraph.innerHTML = 'Aucun comité élu';
    field_comite.appendChild(paragraph);
    field_comite.addEventListener('click', function(){});
  } else {
    affiche_comite(field_comite, liste_elus[0]);
    field_comite.addEventListener('click', function(){
      var canvas = document.getElementById('canvas_comite');
      var ctx = canvas.getContext("2d");
      ctx.reset();
      for(var c of liste_elus[0]){
        tracerpoint(ctx, c[1]+10, c[2]+10, couleur_comite);
      }
    });
  }

  //Affichage du deuxième comité
  if(liste_elus[1].length == 0){
    var paragraph = document.createElement('p');
    paragraph.innerHTML = 'Aucun autre comité possible';
    field_comite2.appendChild(paragraph);
    field_comite2.addEventListener('click', function(){});
  } else {
    affiche_comite(field_comite2, liste_elus[1]);
    field_comite2.addEventListener('click', function(){
      var canvas = document.getElementById('canvas_comite');
      var ctx = canvas.getContext("2d");
      ctx.reset();
      for(var c of liste_elus[1]){
        tracerpoint(ctx, c[1]+10, c[2]+10, couleur_comite);
      }
    });
  }

  //Affichage du troisième comité
  if(liste_elus[2].length == 0){
    var paragraph = document.createElement('p');
    paragraph.innerHTML = 'Aucun autre comité possible';
    field_comite3.appendChild(paragraph);
    field_comite3.addEventListener('click', function(){});
  } else {
    affiche_comite(field_comite3, liste_elus[2]);
    field_comite3.addEventListener('click', function(){
      var canvas = document.getElementById('canvas_comite');
      var ctx = canvas.getContext("2d");
      ctx.reset();
      for(var c of liste_elus[2]){
        tracerpoint(ctx, c[1]+10, c[2]+10, couleur_comite);
      }
    });
  }
}


//Affiche la liste de candidats entrée en paramètre
function affiche_comite(field, liste_elus){
  /*field : fieldset -> élément dans lequel se fera l'affichage
    liste_elus : list[Candidats] -> liste des candidats à afficher
      Candidats : [ nom:str , x:int , y:int , visibilite:int , sexe:char ; age:int ]
  */

  //creer les éléments/noms et les affiches
  for(var i=0; i<liste_elus.length; i++){
    var elu = document.createElement('div');
    elu.append(liste_elus[i][0]);
    elu.dataset.index = i;
    field.appendChild(elu);
  }

  //fonction pour chacun des noms affichés
  field.querySelectorAll('div').forEach(function(elem){
    //affichage sur la boussole au click
    elem.addEventListener('click',function(){
      selection(elem, liste_elus[elem.dataset.index][1], liste_elus[elem.dataset.index][2]);
    });
    
    //affichage des attributs après 1 sec de la souris sur le nom
    tooltips(elem, liste_elus[elem.dataset.index], elem.dataset.index);
    var timeout = null;
    elem.addEventListener("mouseover", function(){
      timeout = setTimeout(showTooltip, 1000);
    });
    elem.addEventListener("mouseout", function(){
      clearTimeout(timeout);
      hideTooltip();
    });

    //Fonctions locales pour afficher et cacher les atttributs
    function showTooltip() {
       const tooltip = elem.querySelector(".tooltip");
       tooltip.style.display = "block";
    }
    function hideTooltip() {
       const tooltip = elem.querySelector(".tooltip");
       tooltip.style.display = "none";
    }
  });
}



//Affichage du points selectionné en rouge
function selection(elem, x, y){
  /*elem : div -> div contenant le nom du candidat à afficher
    x : int -> coordonnées x du candidat
    y : int -> coordonnées y du cnadidat
  */

  //Reset de tous les éléments possiblement modifiés par la selection
  var canvas = document.getElementById("canvas_selection");
  var ctx = canvas.getContext("2d");
  ctx.reset();

  for(var e of document.getElementById('comite_elu').querySelectorAll('div')){
    e.style.fontWeight = 'normal';
    e.style.color = couleur_font;
  }

  for(var e of document.getElementById('comite2').querySelectorAll('div')){
    e.style.fontWeight = 'normal';
    e.style.color = couleur_font;
  }

  for(var e of document.getElementById('comite3').querySelectorAll('div')){
    e.style.fontWeight = 'normal';
    e.style.color = couleur_font;
  }

  for(var e of document.getElementById('liste_candidats').querySelectorAll('div')){
    e.style.fontWeight = 'normal';
    e.style.color = couleur_font;
  }
  
  //Affichage du point en rouge et selection du nom en rouge
  tracerpoint(ctx,x+10,y+10,couleur_selection,2);
  elem.style.fontWeight = 'bold';
  elem.style.color = couleur_selection;
  
}



//Création d'un tooltip (affichage des attributs du candidat entrée en paramètre)
function tooltips(div, candidat, indice){
  /*div : div -> div element dans la liste à afficher
    candidat : Candidat -> attributs du candidat à afficher
      Candidat : [ nom:str , x:int , y:int , visibilite:int , sexe:char ; age:int ]
  */
  const attributs = ['Nom', 'Coordonnée x', 'Coordonnée y', 'Visibilité', 'Sexe', 'Age'];
  //Creation de l'element
  var tooltip = document.createElement('div');
  tooltip.style.backgroundColor = "white";
  tooltip.style.width = "fit-content";
  tooltip.style.border = "solid";
  tooltip.style.padding = '2px 50px 5px 10px';
  tooltip.style.position = 'absolute';
  tooltip.classList.add('tooltip');
  var titre = document.createElement('strong');
  titre.append('Attributs');
  titre.style.textDecoration = "underline";
  tooltip.appendChild(titre);
  tooltip.appendChild(document.createElement('br'));

  //ajout de la satisfaction
  var bold = document.createElement('strong');
  bold.append('Satisfaction : ');
  tooltip.appendChild(bold);
  bold.style.margin = '0px 10px 0px 20px';
  tooltip.append(liste_satisf[indice]+" %");
  tooltip.appendChild(document.createElement('br'));

  //ajout des attributs
  for(var i=0; i<candidat.length; i++){
    bold = document.createElement('strong');
    bold.append(attributs[i] + ' : ');
    tooltip.appendChild(bold);
    bold.style.margin = '0px 10px 0px 20px';
    tooltip.append(candidat[i]);
    tooltip.appendChild(document.createElement('br'));
  }
  tooltip.style.display = 'none';
  div.appendChild(tooltip);
}