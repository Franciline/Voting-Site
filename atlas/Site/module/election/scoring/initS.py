from ..classe import Candidat, Votant
from ..var import COORD_MIN, COORD_MAX, DIST_MAX, SCORE_MIN, SCORE_MAX
from math import dist
from random import random, randint, choice



def posAlea () : #Retourne un 2-uplet contenant des coordonnées aléatoire dans [COORD_MIN ; COORD_MAX]
    return (randint(COORD_MIN, COORD_MAX), randint(COORD_MIN, COORD_MAX))

def distanceAssoc (entite, cible) : #Retourne la distance associé entre une entite et une cible (association)  
    return (dist((entite.coord[0], entite.coord[1]), (cible.coord[0], cible.coord[1])), cible)

def scoreDist (distance) : #Renvoie un score dans [SCORE_MIN ; SCORE_MAX] proportionnel à DIST_MAX
    return round((SCORE_MIN-SCORE_MAX)*distance/DIST_MAX +SCORE_MAX)

def creer_voteS (votant, liste_candidat) : #Crée un vote pour les méthodes de Scoring
    vote_assoc = [distanceAssoc(votant, candidat) for candidat in liste_candidat] #Crée une liste de distance (association)
    vote = [scoreDist(distance[0]) for distance in vote_assoc] #Transforme la liste de distance (association) en liste de score
    return vote



def creer_liste_candidat (nb_candidat) : #Génère liste_candidat de nb_candidat candidat
    return [Candidat("Candidat"+"0"*(len(str(nb_candidat))-len(str(i)))+str(i), posAlea(), round(random(), 2), choice(['H', 'F']), randint(0, 70)) for i in range(1, nb_candidat+1)]

def creer_liste_votant (nb_vote) : #Génère une liste de nb_vote votant
    return [Votant(posAlea()) for i in range(nb_vote)]

def creer_liste_voteS (liste_votant, liste_candidat) : #Crée liste_vote à partir de liste_votant et liste_candidat
    return [creer_voteS(votant, liste_candidat) for votant in liste_votant]


