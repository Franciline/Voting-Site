from ..classe import Candidat, Votant, VotantPoids
from ..var import COORD_MIN, COORD_MAX
from math import dist
from random import random, randint, choice



def posAlea () : #Retourne un 2-uplet contenant des coordonnées aléatoire dans [COORD_MIN ; COORD_MAX]
    return (randint(COORD_MIN, COORD_MAX), randint(COORD_MIN, COORD_MAX))

def distanceAssoc (entite, cible) : #Retourne la distance associé entre une entite et une cible (association)  
    return (dist((entite.coord[0], entite.coord[1]), (cible.coord[0], cible.coord[1])), cible)

def creer_voteR (votant, liste_candidat) : #Crée un vote pour les méthodes de Ranking
    vote_assoc = [(distanceAssoc(votant, candidat)) for candidat in liste_candidat] #Créer une liste de distance (association)
    vote_assoc.sort(key=lambda x: x[0]) #Trier la liste par distance croissante
    vote = [candidat[1] for candidat in vote_assoc] #Conserver seulement les candidats
    return vote



def creer_liste_candidat (nb_candidat) : #Génère liste_candidat de nb_candidat candidat
    return [Candidat("Candidat"+"0"*(len(str(nb_candidat))-len(str(i)))+str(i), posAlea(), round(random(), 2), choice(['H', 'F']), randint(0, 70)) for i in range(1, nb_candidat+1)]

def creer_liste_votant (nb_vote) : #Génère une liste de nb_vote votant
    return [Votant(posAlea()) for i in range(nb_vote)]

def creer_liste_voteR (liste_votant, liste_candidat) : #Crée liste_vote à partir de liste_votant et liste_candidat
    return [creer_voteR(votant, liste_candidat) for votant in liste_votant]



#LIQUIDE



def proximite (votantPoids, liste_votantPoids, rayon) : #Renvoie une liste des votantPoids à proximité du votantPoids selon un rayon
    return [votant 
            for votant in liste_votantPoids
            if votantPoids != votant and distanceAssoc(votantPoids, votant)[0] <= rayon]

def proximite_not_delegue (proximite) : #Filtre les votants poids qui n'ont pas délégué leur vote 
    return [votantPoids for votantPoids in proximite if not votantPoids.delegue]

def proba_proximite (proximite) : #Calcule et associe une probabilité à chaque votantPoids
    d = sum([votantPoids.competence for votantPoids in proximite]) #Calcule la somme des compétences des votantPoids
    return [[votantPoids.competence/d, votantPoids] for votantPoids in proximite] #probabilitéI = compétenceI/d

def valeur_proximite (valeur_proximite) : #Converti la probabilité asssociée à chaque votantPoids en une valeur
    valeur = valeur_proximite
    for i in range(1, len(valeur)) : #Pour chaque indice (sauf 0)
        valeur[i][0] += valeur[i-1][0] #Additionner la probabilité à la valeur précédente
    return valeur

def delegation_ForAll (liste_votantPoids, rayon) : #Procédé de délégation pour tous les votantPoids
    for votantPoids in liste_votantPoids : #Pour chaque votantPoids
        if not votantPoids.delegue and random() <= 1-votantPoids.competence : #Si le votantPoids n'a pas délégué son vote et choisi de le déléguer 
            liste_proximite = proximite(votantPoids, liste_votantPoids, rayon) #Calculer la liste des votantPoids à proximité
            liste_proximite = proximite_not_delegue(liste_proximite) #Filtrer les votantPoids qui n'ont pas délégué leur vote
            liste_proximite = proba_proximite(liste_proximite) #Associer une probabilité à chaque votantPoids
            liste_proximite = valeur_proximite(liste_proximite) #Associer une valeur à chaque votantPoids
            liste_proximite.sort(key=lambda x: x[0]) #Trier la liste obtenue par la valeur associée à chaque votantPoids
            x = random() #Choix d'une valeur pour choisir le votantPoids de la liste à déléguer
            for i in range(len(liste_proximite)) : #Pour chaque votantPoids de la liste
                if x <= liste_proximite[i][0] : #Si sa valeur est supérieure ou égale à la valeur choisie
                    votantPoids.delegation(liste_proximite[i][1]) #Déléguer le vote à ce votantPoids
                    break #Recommencer pour le votantPoids suivant

def concat_all (liste_liste) : #Concatène toutes les listes d'une liste
    concat = []
    for i in range (len(liste_liste)) :
        concat += liste_liste[i]
    return concat



def creer_liste_votantPoids (nb_vote) : #Génère une liste de nb_vote votantPoids
    return [VotantPoids(posAlea(), round(random(), 2)) for i in range(nb_vote)]

def creer_liste_votePoidsR (liste_votantPoids, liste_candidat, rayon) : #Crée liste_vote à partir de liste_votantPoids et liste_candidat et un rayon
    delegation_ForAll(liste_votantPoids, rayon) #Effectuer le procédé de délégation pour tous les votantPoids
    liste_vote = concat_all([votantPoids.poids*[creer_voteR(votantPoids, liste_candidat)] 
                                for votantPoids in liste_votantPoids]) #Crée la liste_vote selon le poids des votantPoids
    return liste_vote


