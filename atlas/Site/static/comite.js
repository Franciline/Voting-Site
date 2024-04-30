//AU LANCEMENT DE LA PAGE
window.onload = function() {
    ajoutCandContraints();
}

/*---------------------------------------*/
//CONTRAINTES GLOBALES

//Fonction sur la contrainte sur la parité des sexes
function parite(){
    var par=document.getElementById('parite');
    const check=par.childNodes[1].checked;
    if(check){
        var f = document.createElement('div');
        var h = document.createElement('div');
        f.append('Femme : ');
        var inp_f = creerInput('number');
        inp_f.value = 0.5;
        inp_f.step = 0.01;
        inp_f.min = 0;
        inp_f.max = 1;
        inp_f.required = 'true';
        inp_f.style.setProperty("width","50px");
        f.appendChild(inp_f);
        
        h.append('Homme : ')
        var inp_h = creerInput('number');
        inp_h.value = 0.5;
        inp_h.step = 0.01;
        inp_h.min = 0;
        inp_h.max = 1;
        inp_h.required = 'true';
        inp_h.style.setProperty("width","50px");
        h.appendChild(inp_h);


        inp_f.addEventListener('input',function(){
            if(Number(inp_f.value) > 1) inp_f.value=1;
            if(Number(inp_f.value) < 0) inp_f.value=0;
            inp_h.value = (1-Number(inp_f.value)).toFixed(2);
        });

        inp_h.addEventListener('input',function(){
            if(Number(inp_h.value) > 1) inp_h.value=1;
            if(Number(inp_h.value) < 0) inp_h.value=0;
            inp_f.value = (1-Number(inp_h.value)).toFixed(2);
        });

        par.appendChild(h);
        par.appendChild(f);
    } else if(check == false){
        par.removeChild(par.childNodes[6]);
        par.removeChild(par.childNodes[5]);
    }
}

//Fonction sur la contrainte des distances entre les candidats
function distance(){
    var dis = document.getElementById('distance');
    const check=dis.childNodes[1].checked;
    if(check){
        var min = document.createElement('div');
        var max = document.createElement('div');

        min.append('Minimum : ');
        var inp_min = creerInput('number');
        inp_min.value = 0;
        inp_min.step = 0.01;
        inp_min.min = 0;
        inp_min.style.setProperty("width","50px");
        inp_min.required = 'true';
        min.appendChild(inp_min);
        
        max.append('Maximum : ')
        var inp_max = creerInput('number');
        inp_max.value = 0;
        inp_max.step = 0.01;
        inp_max.min = 0;
        inp_max.style.setProperty("width","50px");
        inp_max.required = 'true';
        max.appendChild(inp_max);

        
        inp_min.addEventListener('input',function(){
            if(Number(inp_min.value) < 0) inp_min.value=0;
            if(Number(inp_max.value) < Number(inp_min.value)) inp_max.value=inp_min.value;
        });

        inp_max.addEventListener('input',function(){
            if(Number(inp_max.value) < Number(inp_min.value)) inp_min.value=inp_max.value;
        });

        dis.appendChild(min);
        dis.appendChild(max);
    } else if(check == false){
        dis.removeChild(dis.childNodes[6]);
        dis.removeChild(dis.childNodes[5]);
    }
}


/*---------------------------------------------------------*/
//CONTRAINTES CANDIDATS

//Ajout d'une contrainte individuelle dans les données
function ajoutCandContraints(){
    const donnees=document.getElementById('donnees');
    for(var i=0;i<nbCand;i++) donnees.appendChild(creerCandContraints(i+1));
}

//Créer et renvoi d'une contrainte individuelle
function creerCandContraints(i){
    // i : int -> numero de la contrainte
    var candi = document.createElement("fieldset");
    candi.append("Candidat "+i+") ");
    candi.append(document.createElement("br"));
    candi.id = "cand"+i+"_cont"+i;
    candi.style.float="left";
    candi.style.width="20%";

    ajoutContraintes(candi);
    return candi;
}


//Ajouts des inputs dans la contrainte candi
function ajoutContraintes(candi){
    //candi : fieldset -> element de la page contenant les contraintes

    //pour le nom
    var nom = document.createElement('div');
    nom.append(document.createElement('br'));
    nom.append("Nom");
    att_nom(nom);
    candi.appendChild(nom);
    
    //pour l'age
    var age = document.createElement('div');
    age.append(document.createElement('br'));
    age.append("Age");
    att_age(age);
    candi.appendChild(age);

    //pour la coordonnée x
    var x = document.createElement('div');
    x.append(document.createElement('br'));
    x.append("Coordonnée x");
    att_coord(x);
    candi.appendChild(x);

    //pour la coordonnée y
    var y = document.createElement('div');
    y.append(document.createElement('br'));
    y.append("Coordonnée y");
    att_coord(y);
    candi.appendChild(y);

    //Pour la visibilité
    var visibilite = document.createElement('div');
    visibilite.append(document.createElement('br'));
    visibilite.append("Visibilité");
    att_visibilite(visibilite);
    candi.appendChild(visibilite);

    //POur le sexe
    var sexe = document.createElement('div');
    sexe.append(document.createElement('br'));
    sexe.append("Sexe");
    att_sexe(sexe);
    candi.appendChild(sexe);

}

//Création d'un input
function creerInput(para){
    // para : str -> 'number' ou 'text', parametre de type de l'input
    var inp = document.createElement('input');
    inp.type = para;
    inp.required = true;
    inp.style.setProperty("width","20%");
    return inp;
}

//Contrainte sur le nom
function att_nom(conti_div){
    conti_div.append(" : [ ");
    var inp_inf = creerInput('text');
    inp_inf.value="A";
    inp_inf.required = 'true';
    conti_div.appendChild(inp_inf);
    conti_div.append(" , ");
    var inp_sup = creerInput('text');
    inp_sup.value="z";
    inp_sup.required = 'true';
    conti_div.appendChild(inp_sup);
    conti_div.append(" ]");
}

//Contrainte sur l'age
function att_age(conti_div){
    conti_div.append(" : [ ");
    var inp_inf = creerInput('number');
    inp_inf.value=0;
    inp_inf.required = 'true';
    conti_div.appendChild(inp_inf);
    conti_div.append(" , ");
    var inp_sup = creerInput('number');
    inp_sup.value=100;
    inp_sup.required = 'true';
    conti_div.appendChild(inp_sup);
    conti_div.append(" ]");
}

//Contrainte sur les coordonnées (x et y)
function att_coord(conti_div){
    conti_div.append(" : [ ");
    var inp_inf = creerInput('number');
    inp_inf.value=0;
    conti_div.appendChild(inp_inf);
    conti_div.append(" , ");
    var inp_sup = creerInput('number');
    inp_sup.value=600;
    inp_sup.required = 'true';
    conti_div.appendChild(inp_sup);
    conti_div.append(" ]");
}

//contrainte sur la visibilité
function att_visibilite(conti_div){
    conti_div.append(" : [ ");
    var inp_inf = creerInput('number');
    inp_inf.step = 0.01;
    inp_inf.value=0;
    inp_inf.required = 'true';
    inp_inf.addEventListener('input',function(){
        if(Number(inp_inf.value) > 1) inp_inf.value=1;
        if(Number(inp_inf.value) < 0) inp_inf.value=0;
    });
    conti_div.appendChild(inp_inf);
    conti_div.append(" , ");

    var inp_sup = creerInput('number');
    inp_sup.step = 0.01;
    inp_sup.value=1;
    inp_sup.required = 'true';
    inp_sup.addEventListener('input',function(){
        if(Number(inp_sup.value) > 1) inp_sup.value=1;
        if(Number(inp_sup.value) < 0) inp_sup.value=0;
    });
    conti_div.appendChild(inp_sup);
    conti_div.append(" ]");
}

//Contrainte sur le sexe
function att_sexe(conti_div){
    conti_div.append(" = ");

    var sel = document.createElement('select');

    var both = document.createElement('option');
    both.value="both";
    both.selected = true;
    both.innerHTML="Les deux";
    both.selected = true;
    sel.appendChild(both);

    var optF = document.createElement('option');
    optF.value="F";
    optF.innerHTML="Femme";
    sel.appendChild(optF);

    var optH = document.createElement('option');
    optH.value="H";
    optH.innerHTML="Homme";
    sel.appendChild(optH);

    conti_div.appendChild(sel);
}

/*-------------------------------------------------------------------*/
//Récuperation contraintes globales et individuelles

//Récupération des contraintes individuelles
function recupDonnees(){
    const donnees = document.getElementById("donnees");
    var all=[];
    for(var i=0; i<nbCand;i++){
        var candi=donnees.childNodes[i];
        var cand = [];
        for(var j=0; j<5; j++){
            var conti = candi.childNodes[2+j];
            var cont = [];
            cont.push(conti.querySelectorAll('input')[0].value);
            cont.push(conti.querySelectorAll('input')[1].value);
            cand.push(cont);
        }
        var contSexe = [];
        contSexe.push(candi.childNodes[7].querySelectorAll('select')[0].value);
        cand.push(contSexe);
        all.push(cand);

    }

    return all;
}

//Récupération des contraintes globales
function recupGlobales(){
    const par = document.getElementById('parite');
    var parite = [];
    if(par.childNodes[1].checked){
        parite.push(par.childNodes[5].querySelectorAll('input')[0].value);
        parite.push(par.childNodes[6].querySelectorAll('input')[0].value);
    }

    const dis = document.getElementById('distance');
    var distance = [];
    if(dis.childNodes[1].checked){
        distance.push(dis.childNodes[5].querySelectorAll('input')[0].value);
        distance.push(dis.childNodes[6].querySelectorAll('input')[0].value);
    }

    return [parite,distance];
}


