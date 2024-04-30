import subprocess
from flask import Flask, session, request, jsonify
from redirection_templates import *
from fonctions_manipulation_BDD import *

#CREATION DE L'APP
app = Flask(__name__, template_folder='templates', static_folder = 'static')

#Creation des sessions pour les requetes HTTP
app.secret_key = 'cle_secrete'
app.config['session_name'] = 'Projet_vote'

#------------------------- APP --------------------------------

"""REDIRECTION PAGES HTML"""

#Page d'accueil
@app.route('/', methods = ['POST', 'GET'])
def accueil():
    """Page d'accueil du site"""
    return template_site()

#Affiche la page simulation
@app.route('/simulation/', methods = ['POST', 'GET'])
def simu(): 
    """Page simulation"""
    return template_simulation()

#Affiche la page documentation
@app.route('/documentation/', methods = ['POST', 'GET'])
def docu(): 
    """Page documentation"""
    return template_documentation()

#Affiche la page credits
@app.route('/credits/', methods = ['POST', 'GET'])
def cred(): 
    """Page credits"""
    return template_credits()


#Affiche la page résultats manuelles
@app.route('/resultats_manuelle/', methods = ['POST', 'GET'])
def res_sim(): 
    #--Récupération des données pour HTML
    comite = session['type_election']
    if comite == "comit":
        nb_comit = int(session.get("nb_comit"))
        return template_comite(nb_comit)
    liste_votant_candidats_xy, liste_resultats, liste_resultats_votes, liste_candidat, liste_satisf = donnees_depuis_BDD()
    return template_affiche_election(liste_resultats, liste_votant_candidats_xy, liste_resultats_votes, liste_candidat, liste_satisf)


"""REDIRECTION AVEC DONNEES HTML"""

#Traitement manuelle/automatique/délégation/comite/individuel depuis page simulation
@app.route('/simulation_form/', methods = ['POST', 'GET']) 
def simulation_form():
    """Page simulation: l'utilisateur choisit le type et le mode d'election, ainsi que les variables,
    et la fonction renvoie a la page suivante correspondante"""
    nb_cand, nb_elec, rayon_range = -1, -1, -1

    #On récupère les données de HTML
    if request.method == 'POST':
        #Recuperation des choix de l'utilisateur  

        type_election = request.form.get("type_elec")   #ind ou comit
        nb_cand = int(request.form.get("nb_candidats"))
        nb_elec = int(request.form.get("nb_electeurs"))
        nb_comit = int(request.form.get("nb_comit"))
        mode_election = request.form.get("placement")   #manu ou auto
        rayon_range = request.form.get("range")
        rayon_range = float(rayon_range) if type(rayon_range) == str else 0 #cas choix democratie liquide
        manuelle = "type_placement" in request.form

        #Sauvegarde des donnees
        session['type_election'] = type_election
        session["nb_cand"] = nb_cand
        session["nb_elec"] = nb_elec
        session["mode_election"] = mode_election 
        session["rayon_range"] = rayon_range * 50
        session["manuelle"] = manuelle
        session['nb_comit'] = nb_comit
        empty_bdd()         #on reinitialise la BDD pour une nouvelle simulation
    
    if request.method == 'GET':
        empty_bdd_cont()    #on reinitialise les contraintes pour le comite
        session.permanent = False

        type_election = session.get("type_election")
        nb_cand = int(session.get("nb_cand"))
        nb_elec = int(session.get("nb_elec"))
        rayon_range = int(session.get("rayon_range"))
        manuelle = session.get("manuelle")
        nb_comit = int(session.get("nb_comit"))
    
    del_liquide = True if rayon_range != 0 else False
    session['del_liquide'] = del_liquide
    
    #cas democratie liquide (seulement en automatique indidividuel)
    if del_liquide == True:
        return liquide(nb_cand, nb_elec, rayon_range)

    #--- Choix placement manuelle
    if manuelle == True:                   
        return placement_manuelle(nb_cand, nb_elec) 
    
    #--- Choix placement automatique
    if type_election == "comit":
        return template_comite(nb_comit) #automatique comite
    return individuel_auto(nb_cand, nb_elec) #automatique indiv


#affiche le résultat de la page comité
@app.route('/affiche_comite', methods = ['POST', 'GET'])
def affiche_comite():
    """Renvoie les resultats du comité manuelle"""
    if request.method == 'POST':
        return affiche_comite_res(session.get('nb_cand'), session.get('nb_elec'))
    return template_simulation()


"""RECUPERATION DONNEES DEPUIS HTML JSON"""

#Sauvegarde des données candidats/votants pour la partie manuelle (comité)
#partie manuelle
@app.route('/process-data', methods=["POST"])
def index(): 
    """Recupere et sauvegarde les candidats et les votants positionnes par l'utilisateur pour la manuelle"""

    if request.method == "POST":
        #Récupération des données sur JS
        jsonData = request.get_json()
        axe_x, axe_y, nb_candidat, candidats = jsonData['x'], jsonData['y'], int(jsonData['c']), jsonData['candidats']
        #On sauvegarde dans la BDD
        ajout_dans_BDD(axe_x, axe_y, nb_candidat, candidats)
    return jsonify(status="success")

#Recupere des données contraintes pour la partie comité
@app.route('/comite_contraintes', methods=["POST"])
def comite_contraintes(): 
    """Récupere les contraintes globales et individuelles de l'utilisateur pour le comité"""

    if request.method == "POST":
        #On recupere les donnees
        jsonData = request.get_json()
        indiv, glob = jsonData['individuelles'], jsonData['globales']

        #On transforme les donnees recues en donnees utilisables puis les sauvegarde dans la BDD
        indiv, glob = ordre_contraintes(indiv, glob)
        save_cont_BDD(indiv, glob)
    return jsonify(status="success")

"""MAIN"""

#Lancement

if __name__ == '__main__':
    #réinitialise la BDD
    subprocess.run("[ -f bdd.db ] && rm bdd.db", shell = True)
    
    app.run(debug=False, use_reloader=False)
    


    #response = make_response(...)
    #response.set_cookie(app.session_cookie_name, expires=0)

    #session.clear()
    #session.close()
    
    
