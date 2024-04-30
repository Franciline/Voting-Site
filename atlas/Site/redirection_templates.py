from flask import render_template
#from codecarbon import track_emissions

"""FONCTIONS RENDER TEMPLATE"""

#page site 
def template_site():
    """template site.html"""
    return render_template('site.html')

#page documentation
def template_documentation():
    return render_template('documentation.html')

#page credits
def template_credits():
    return render_template('credits.html')

#page comite [choix]
def template_comite(nb_cand): 
    """template comite.html
    input: 
        nb_cand: le nombre de candidats int"""
    return render_template('comite.html', nb_cand = nb_cand)

#page simulation [choix]
def template_simulation():
    """template simulation.html"""
    return render_template('simulation.html')

#page manuelle [placement]
def template_manuelle(nb_cand, nb_elec):
    """template placement_manu.html
    
    input:
        nb_cand: le nombre de candidats int
        nb_elec: le nombre d'electeurs int"""
    return render_template("placement_manu.html",nb_candi=nb_cand, nb_electi=nb_elec)

#page election individuel [resultats]
def template_affiche_election(liste_resultats, liste_votant_candidats_xy, liste_resultats_votes, liste_candidat, liste_satisf):
    """template affiche_election.html
    
    input:
        liste_resultats, la liste des gagnant de chaque methode de vote
        liste_votant_candidats_xy, la liste des positions x y des votants et des candidats
        liste_resultats_votes, la liste du nombre de vote pour chaque candidat pour chaque methode de vote
        liste_candidat, la liste des candidats sous leur forme attributs
        liste_satisf, liste des satisfaction de chaque candidat
    """
    return render_template('affiche_election.html', liste_resultats = liste_resultats, liste_votant_candidats_xy = liste_votant_candidats_xy,
                            liste_resultats_votes = liste_resultats_votes, liste_candidat = liste_candidat, liste_satisf=liste_satisf)

#page democratie liquide [resultats]
def template_liquide(liste_resultats, liste_votant_candidats_xy, liste_resultats_votes, liste_candidat, liste_poids, liste_deleg, liste_satisf):
    """template liquide.html
    
    input:
        liste_resultats, la liste des gagnant de chaque methode de vote
        liste_votant_candidats_xy, la liste des positions x y des votants et des candidats
        liste_resultats_votes, la liste du nombre de vote pour chaque candidat pour chaque methode de vote
        liste_candidat, la liste des candidats sous leur forme attributs
        liste_poids, la liste des poids de chaque votants
        liste_deleg, la liste de delegation de chaque votants
        liste_satisf, liste des satisfaction de chaque candidat
    """
    return render_template('liquide.html', liste_resultats = liste_resultats, liste_votant_candidats_xy = liste_votant_candidats_xy,
                            liste_resultats_votes = liste_resultats_votes, liste_candidat = liste_candidat, liste_poids = liste_poids, liste_deleg = liste_deleg, liste_satisf=liste_satisf)

#page affiche_comite [resultats]
def template_affiche_comite(listexv, listeyv, res_comites_mdte, liste_all_candi, list_cont_indiv, list_cont_glob, liste_satisf):
    """template affiche_comite.html
    
    input:
        listexv, la liste des positions x des votants 
        listeyv, la liste des positions y des votants
        res_comites_mdte, la liste de comites pour chaque methodes de vote
        liste_all_candi, la liste de tous les candidats sous leur forme attribut
        list_cont_indiv, la liste des contraintes individuelles
        list_cont_glob, la liste des contraintes globales
        liste_satisf, la liste des satisfaction pour chaque candidat
    """
    return render_template("affiche_comite.html", liste_xv = listexv, liste_yv = listeyv, res_comites_mdte = res_comites_mdte, liste_all_candi = liste_all_candi, list_cont_indiv = list_cont_indiv, list_cont_glob = list_cont_glob, liste_satisf=liste_satisf)

