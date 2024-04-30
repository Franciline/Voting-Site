
const tmp_candidats = nb_candidate;
let canvasElem = document.querySelector("canvas");
let names = ["Emmental Macaron", "Marine Lapin", "Jean Peuplu","Marinette Dupaincheng","Harry Ko","Taylor Shift","Da Heil","Sasuke","Amelia","Chucky","Tiri Giglio","Mickey Mouse","Sara croche","Adrien Agreste","Legoshi","JungKook","Alexis Bouthier","Javier Fresan"];
let sexe_list = ["M","F"];
let axe_x = [];
let axe_y = [];
let candidat_list = [];

// Infos candidats 
let nom= document.getElementById("cand_name");
let age = document.getElementById("cand_age");
let sexe_M = document.getElementById("cand_sexe");
let popularite = document.getElementById("cand_pop");


function getMousePosition(canvas, event) {
  let rect = canvas.getBoundingClientRect();
  let x = event.clientX - rect.left;
  let y = event.clientY - rect.top;
  document.getElementById("x").innerHTML=x;
  document.getElementById("y").innerHTML=y;
}

function tracerpoint(context, x, y, couleur){
  context.lineWidth=2;
  context.strokeStyle='black';
  context.fillStyle = couleur;
  context.beginPath();
  context.ellipse(x, y, 7, 7, 0, 0, Math.PI * 2);
  context.fill();
  context.stroke();
}

function add_electeur(canvas,event){
  if(nb_electeurs>0){
    const canvas2 = document.getElementById("myCanvas");
    const ctx = canvas2.getContext("2d");

    let rect = canvas.getBoundingClientRect();
    let x = event.clientX - rect.left;
    let y = event.clientY - rect.top;
    tracerpoint(ctx, x, y, "white");

    axe_x.push(x);
    axe_y.push(y);

    nb_electeurs=nb_electeurs-1;
    document.getElementById("afficheNbElect").innerHTML="Nombre d'électeurs restants à placer : "+nb_electeurs;
  }
  if(nb_electeurs==0) document.getElementById("fini").style.display = "block";
}

function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

function add_candidate(canvas, event){
  if(document.getElementById("InfoCandidats").style.display=="none"){
    if(nb_candidate>0){
      const canvas2 = document.getElementById("myCanvas");
      const ctx = canvas2.getContext("2d");
  
      let rect = canvas.getBoundingClientRect();
      let x = event.clientX - rect.left;
      let y = event.clientY - rect.top;
      tracerpoint(ctx, x, y, "blue");
  
      axe_x.push(x);
      axe_y.push(y);
  
      nb_candidate=nb_candidate-1;
      document.getElementById("afficheNbCand").innerHTML="Nombre de candidats restants à placer : "+nb_candidate;
      show_candidats_box();
    } else add_electeur(canvas,event);
  }
}

// Remplis aléatoirement les informations des candidats
function fillRandom(){
  let info_c = document.getElementById("c_infoc").checked;
  if(info_c){
    nom.value = names[getRandomInt(names.length)];
    age.value = getRandomInt(100);
    if(sexe_list[getRandomInt(2)]=="M") sexe_M.checked = true;
    popularite.value = getRandomInt(100);
  } else {
    reset_candidats_box();
    document.getElementById("InfoCandidats").style.display="block";
  }
}

// Vérifie la validité des informations entrées et ajoute la personne à la liste des candidats
function information_candidats(){
  var candidat = {
    nom:'',
    age:'',
    sexe:'',
    visibilite:'',
  }

  if(nom.checkValidity()) {
    candidat.nom = nom.value;
    document.getElementById("err_name").style.display = 'none';
  } else {
    document.getElementById("err_name").innerHTML = nom.validationMessage;
    document.getElementById("err_name").style.display = 'block';
    return
  }

  if(age.checkValidity()) {
    candidat.age = age.value;
    document.getElementById("err_age").style.display = 'none';
  } else {
    document.getElementById("err_age").innerHTML = age.validationMessage;
    document.getElementById("err_age").style.display = 'block';
    return
  }

  if(sexe_M.checked) candidat.sexe = "M";
  else candidat.sexe = "F";

  if(popularite.checkValidity()) {
    candidat.visibilite = Number(popularite.value)/100;
    document.getElementById("err_pop").style.display = 'none';
  } else {
    document.getElementById("err_pop").innerHTML = popularite.validationMessage;
    document.getElementById("err_pop").style.display = 'block';
    return
  }
  candidat_list.push(candidat);
  console.log(candidat_list);
  reset_candidats_box();
}

function reset_candidats_box(){
  document.getElementById("InfoCandidats").style.display="none";
  document.getElementById("cand_name").value="";
  document.getElementById("cand_age").value = '';
  document.getElementById("cand_pop").value = '';
  document.getElementById("cand_sexe").checked = false;
  document.getElementById("c_infoc").checked = false;
}

function show_candidats_box(){ document.getElementById("InfoCandidats").style.display="block"; }

function update_mouse(){
  if(document.getElementById("InfoCandidats").style.display=="none") canvasElem.style.cursor="pointer";
  else canvasElem.style.cursor="not-allowed";
}

canvasElem.addEventListener("mousemove", function (e) { getMousePosition(canvasElem, e); update_mouse()});
canvasElem.addEventListener("click", function (e) { add_candidate(canvasElem, e);});

// Contraintes d'âge et de popularité

age.addEventListener("input", function(){
  if(age.value<0) age.value=0;
  if(age.value>100) age.value=100;
});

popularite.addEventListener("input",function(){
  if(popularite.value<0) popularite.value = 0;
  if(popularite.value>100) popularite.value =100;
});