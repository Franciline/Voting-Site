from ..var import COORD_MIN, COORD_MAX, DIST_MAX
from math import dist, floor, ceil
from itertools import combinations



#CONTRAINTES_INDIVIDUELLES

#Nom

def contrainte_Nom (candidat, inf, sup) : #Vérifie si le nom du candidat est dans [inf, sup]
    return inf <= candidat.nom <= sup 

def compress_Nom (liste_candidat, inf=None, sup=None) : #Filtre liste_candidat selon le nom dans l'intervalle [inf, sup]
    if inf == None :
        inf = ""
    if sup == None : #Si sup non défini
        return set(filter(lambda candidat: contrainte_Nom(candidat, inf, candidat.nom), liste_candidat))
    return set(filter(lambda candidat: contrainte_Nom(candidat, inf, sup), liste_candidat))

#CoordX

def contrainte_CoordX (candidat, inf, sup) : #Vérifie si la coordonnée X du candidat est dans [inf, sup]
    return inf <= candidat.coord[0] <= sup 

def compress_CoordX (liste_candidat, inf=None, sup=None) : #Filtre liste_candidat selon la coordonnée X dans [inf, sup]
    if inf == None:
        inf = COORD_MIN 
    if sup == None :
        sup = COORD_MAX
    return set(filter(lambda candidat: contrainte_CoordX(candidat, inf, sup), liste_candidat))

#CoordY

def contrainte_CoordY (candidat, inf, sup) : #Vérifie si la coordonnée Y du candidat est dans [inf, sup]
    return inf <= candidat.coord[1] <= sup 

def compress_CoordY (liste_candidat, inf=None, sup=None) : #Filtre liste_candidat selon la coordonnée Y dans [inf, sup]
    if inf == None : 
        inf = COORD_MIN 
    if sup == None :
        sup = COORD_MAX
    return set(filter(lambda candidat: contrainte_CoordY(candidat, inf, sup), liste_candidat))

#Visibilite

def contrainte_Visibilite (candidat, inf, sup) : #Vérifie si la visibilité du candidat est dans [inf, sup]
    return inf <= candidat.visibilite <= sup

def compress_Visibilite (liste_candidat, inf=None, sup=None) : #Filtre liste_candidat selon la visibilité dans [inf, sup]
    if inf == None :
        inf = 0
    if sup == None :
        sup = 1
    return set(filter(lambda candidat: contrainte_Visibilite(candidat, inf, sup), liste_candidat))

#Sexe

def contrainte_Sexe (candidat, sexe) : #Vérifie si le sexe du candidat
    return candidat.sexe == sexe

def compress_Sexe (liste_candidat, sexe=None) : #Filtre liste_candidat selon le sexe
    if sexe == None or sexe not in {'H', 'F'} : #Si sexe non défini ou invalide
        return set(liste_candidat)
    return set(filter(lambda candidat: contrainte_Sexe(candidat, sexe), liste_candidat))

#Age

def contrainte_Age (candidat, inf, sup) : #Vérifie si l'âge du candidat est dans [inf, sup]
    return inf <= candidat.age <= sup 

def compress_Age (liste_candidat, inf=None, sup=None) : #Filtre liste_candidat selon l'âge dans [inf, sup]
    if inf == None :
        inf = 0
    if sup == None : #Si sup non défini
        sup = max(liste_candidat, key=lambda candidat: candidat.age).age
    return set(filter(lambda candidat: contrainte_Age(candidat, inf, sup), liste_candidat))



#MANIPULATIONS DE TYPES



def ens_into_setFset (ens) : #Transforme un ensemble de tuple ou de valeur en ensemble d'ensemble
    return {frozenset(element) if isinstance(element, tuple)
            else frozenset({element}) for element in ens}

def listFset_into_listTuple (listFset) : #Transforme une liste d'ensemble ou de None en liste de tuple
    return [tuple(fSet) if fSet else None for fSet in listFset]

def union (*liste_ens) : #Renvoie l'union de tous les ensembles en arguments
    u = set() #On initialise un ensemble de départ
    for ens in liste_ens : #Pour chaque ensemble
        u |= ens #On fait l'union
    return u

def intersection (*liste_ens) : #Renvoie l'intersection de tous les ensembles en arguments
    if not liste_ens : #Si la liste d'ensemble est vide
        return set() #On renvoie l'ensemble vide
    inter = liste_ens[0] #On initialise l'ensemble de départ
    inter.intersection_update(*liste_ens[1:]) #On fait l'intersection de l'ensemble de départ à tous les autres
    return inter



#COMBINAISONS DE FUSIONS



def fusion (comite, ensC) : #Fusionne un comité à tous les candidats/comités d'un ensemble
    return {element.union(comite) if isinstance(element, frozenset) 
            else frozenset({element}).union(comite)
            for element in ensC}

def combi_fusion (ensComite, ensC) : #Renvoie toutes les combinaisons pour la fusion d'un comité et d'un candidat/comité dans deux ensembles
    return union(*[fusion(comite, ensC) for comite in ensComite])



#PROCÉDURE COMBINAISONS DES FILTRAGES DES CONTRAINTES INDIVIDUELLES



def combi_CIndiv (liste_ensCandidat, resultat=None) :  #Renvoie tous les comités pour le choix d'un candidat par ensemble (un candidat peut être choisi 2 fois)
    if not liste_ensCandidat : #Si la liste d'ensemble est vide
        return resultat #Retourner le résultat
    if resultat == None :  #Lorsque la fonction est appelée pour la 1ère fois
        ensComite = ens_into_setFset(liste_ensCandidat[0]) #On transforme le 1er ensemble de candidat en ensemble de comite
        return combi_CIndiv(liste_ensCandidat[1:], ensComite) #On appelle la fonction avec un résultat sur les ensembles suivants
    ensComite = combi_fusion(resultat, liste_ensCandidat[0]) #On fait toutes les combinaisons pour la fusion du résultat et du 1er ensemble de la liste
    return combi_CIndiv(liste_ensCandidat[1:], ensComite) #On appelle la fonction avec le nouveau résultat sur les ensembles suivants



def procede_CIndiv (matrice_procedure, liste_candidat) : #Renvoie tous les comités possibles satisfaisant les contraintes indiquées par martrice_procedure
    procedure_indiv = {'0' : compress_Nom, 
                       '1' : compress_CoordX, 
                       '2' : compress_CoordY, 
                       '3' : compress_Visibilite, 
                       '4' : compress_Sexe, 
                       '5' : compress_Age} #On crée le dictionnaire qui associe un indice (colonne de la matrice) à une procédure de filtrage
    
    liste_inter_filtre = [] #On crée une liste regroupant les ensembles de candidats filtrés pour chaque liste de procédure
    for liste_procedure in matrice_procedure : #Pour chaque liste de procédure sur un candidat (ligne de la matrice)
        liste_filtre = [] #On crée la liste des ensembles de candidat filtrés selon les procédures à effectuer

        for i in range(len(procedure_indiv)) : #Pour chaque indice (colonne de la matrice)
            if liste_procedure[i] : #Si il y a une procédure à effectuer (si la liste contenant les arguments du filtrage n'est pas vide)
                if i == 4 : #Si la procédure corespondante à l'indice requiert 1 argument
                    C_X = procedure_indiv[str(i)](liste_candidat, liste_procedure[i][0]) #Filtrer la liste des candidat avec la procédure avec 1 argument
                else : #Sinon si la procédure correspondante à l'indice requiert 2 arguments
                    C_X = procedure_indiv[str(i)](liste_candidat, liste_procedure[i][0], liste_procedure[i][1]) #Filtrer la liste des candidats avec la procédure avec 2 arguments
                liste_filtre.append(C_X) #Enregistrer l'ensemble des candidats filtrés de la procédure courante
        
        ensX = set(liste_candidat).intersection(*liste_filtre) #Faire l'intersection de la liste des candidats et des ensembles filtrés
        liste_inter_filtre.append(ensX) #Enregistrer l'ensemble des candidats qui valident la liste de procédure courante
    
    combi = combi_CIndiv(liste_inter_filtre) #Faire tous les comités possibles pour le choix d'un candidat par ensemble
    combi_valide = set(filter(lambda comite: len(comite)==len(matrice_procedure), combi)) #Supprimer les comités dont un candidat a été choisi plus d'une fois
    return combi_valide

    

#CONTRAINITES_GLOBALES 

#PariteSexe

def verif_percentHF (percent_H, percent_F) : #Vérification des pourcentages
    if percent_H and percent_F : #Si percent_H et percent_F définis
        if not (0 <= percent_H <= 1 and 0 <= percent_F <= 1 and percent_H+percent_F == 1) : #Si percent_H et percent_F invalides
            return 0.5, 0.5
        return percent_H, percent_F #Sinon percent_H et percent_F valides
    elif percent_H : #Si seulement percent_H défini
        return percent_H, 1-percent_H
    elif percent_F : #Si seulement percent_F défini
        return 1-percent_F, percent_F
    elif not percent_H and not percent_F : #Si percent_H et percent_F non définis
        return 0.5, 0.5

def partage_nbHF (nb_candidat, percent_H, percent_F) :
    if (percent_H*nb_candidat)%1 > percent_F*nb_candidat%1 : #Vérification des décimales pour le partage optimal de nb_H et nb_F
        return ceil(percent_H*nb_candidat), floor(percent_F*nb_candidat)
    else :
        return floor(percent_H*nb_candidat), ceil(percent_F*nb_candidat)

def global_PariteSexe (nb_candidat, liste_candidat, percent_H=None, percent_F=None) : #Renvoie l'ensemble des comités de nb_candidat candidats vérifiant la parité sur le sexe
    percent_H, percent_F = verif_percentHF(percent_H, percent_F) #Vérification des pourcentages
    nb_H, nb_F = partage_nbHF(nb_candidat, percent_H, percent_F) #Partage de nb_H et nb_F

    compressH = compress_Sexe(liste_candidat, sexe='H') #Sélectionner l'ensemble des candidats hommes
    compressF = compress_Sexe(liste_candidat, sexe='F') #Sélectionner l'ensemble des candidats femmes
    combiH = set(combinations(compressH, nb_H)) #Sélectionner toutes les combinaisons de nb_H candidats hommes
    combiF = set(combinations(compressF, nb_F)) #Sélectionner toutes les combinaisons de nb_F candidats femmes
    combiH = ens_into_setFset(combiH) #Transformer l'ensemble de tuple en ensemble d'ensemble
    combiF = ens_into_setFset(combiF) #Transformer l'ensemble de tuple en ensemble d'ensemble
    combi = combi_fusion(combiH, combiF) #Sélectionner l'ensemble des comités respectant la parité sur le sexe
    return combi

#DistanceCoord

def candidat_CDistCoord (candidat, cible, inf, sup) : #Vérifie si la distance entre le candidat et la cible est dans [inf, sup]
    return inf <= dist((candidat.coord[0], candidat.coord[1]), (cible.coord[0], cible.coord[1])) <= sup

def comite_CDistCoord (comite, inf, sup) :  #Vérifie si le comité vérifie la contrainte de distance entre candidats
    for (candidat1, candidat2) in set(combinations(comite, 2)) : #Pour chaque couple de candidats
        if not candidat_CDistCoord(candidat1, candidat2, inf, sup) : #Si un couple ne vérifie pas la contrainte de distance
            return False #Le comité n'est pas valide
    return True #Le comité est valide

def global_DistanceCoord (nb_candidat, liste_candidat, inf=None, sup=None) : #Renvoie l'ensemble des comités de nb_candidats candidats vérifiant la contrainte de distance
    if inf == None : #Si inf non défini
        inf = 0
    if sup == None : #Si sup non défini
        sup = DIST_MAX
    combi = set(combinations(liste_candidat, nb_candidat)) #Sélectionner toutes les combinaisons de nb_candidats candidats dans liste_candidat
    combi = ens_into_setFset(combi) #Transformer l'ensemble de tuple en ensemble d'ensemble
    combi_valide = set(filter(lambda comite: comite_CDistCoord(comite, inf, sup), combi)) #Filtrer les comités vérifiant la contrainte de distance
    return combi_valide



#PROCÉDURE INTERSECTION DES COMITÉS FILTRÉS DES CONTRAINTES GLOBALES



def procede_CGlobale (nb_candidat, liste_procedure, liste_candidat) : #Renvoie tous les comités de nb_candidat candidats satisfaisant les contraintes indiquées par liste_procedure
    procedure_globale = {'0' : global_PariteSexe, 
                         '1' : global_DistanceCoord} #On crée le dictionnaire qui associe un indice (de la liste) à une procédure globale
    
    combi = set(combinations(liste_candidat, nb_candidat))
    combi = ens_into_setFset(combi)
    liste_ensComite = [] #On crée la liste des ensembles de comité selon les procédures à effectuer

    for i in range(len(procedure_globale)) : #Pour chaque indice
        if liste_procedure[i] : #Si il y a une procédure à effectuer (si la liste contenant les arguments de la procédure n'est pas vide)
            C_X = procedure_globale[str(i)](nb_candidat, liste_candidat, liste_procedure[i][0], liste_procedure[i][1]) #Effectuer la procédure avec 2 arguments
            liste_ensComite.append(C_X) #Enregistrer l'ensemble des comités qui valide la procédure courante
    
    ens_valide = combi.intersection(*liste_ensComite) #Faire l'intersection de tous les ensembles de comité
    return ens_valide



#SÉLECTIONS DE COMITÉS



def scoreComiteAssoc (comite, liste_candidat, liste_score) : #Renvoie le score du comité en prennant en compte la visibilité (association)
    return (sum([candidat.visibilite*liste_score[liste_candidat.index(candidat)] for candidat in comite]), comite)

def scoreComiteAssoc_ForAll (ensComite, liste_candidat, liste_score) : #Associe un score à chaque comite
    return {scoreComiteAssoc(comite, liste_candidat, liste_score) for comite in ensComite}

def maxScoreComite (ensComite, liste_candidat, liste_score) : #Renvoie le comité qui maximise le score
    return max(scoreComiteAssoc_ForAll(ensComite, liste_candidat, liste_score), key=lambda assoc: assoc[0])[1]

def classement_comite (nb_comite, ensComite, liste_candidat, liste_score) : #Renvoie une liste de nb_comite comités par ordre décroissant du score
    if nb_comite == 0 : #S'il ne fait aucun comité
        return [] #Retourner la liste vide
    if not ensComite : #Si l'ensemble de comité est vide
        return [None]*nb_comite #Retourner une liste contenant nb_comite None
    comite = maxScoreComite(ensComite, liste_candidat, liste_score) #Sélectionner le comité qui maximise le score
    return [comite] + classement_comite(nb_comite-1, ensComite.difference({comite}), liste_candidat, liste_score) #Ajouter le comité au début de la liste et itérer avec nb_comite-1 comités et enlever le comité de l'ensemble



#AFFICHAGE



def aff_CollecC (collecC, *attributes) : #Retourne l'affichage d'une collection de candidat
    if not collecC :
        return None
    return [candidat.aff(*attributes) for candidat in collecC]

def aff_Collec2C (collec2C, *attributes) : #Retourne l'affichage d'une collection de collection de candidat
    return [aff_CollecC(collecC, *attributes) for collecC in collec2C]



#GLOUTON



"""
def liste_DistCoord (candidat, liste_candidat, inf, sup) : #Renvoie la liste des candidats dont la contrainte de distance est respectée par rapport à candidat
    return [cible 
            for cible in liste_candidat
            if cible != candidat and candidat_contrainte_DistCoord(candidat, cible, inf, sup)]

def liste_DistCoord_ForAll (liste_candidat, inf, sup) : #Renvoie la liste des listes des candidats dont la contrainte de distance est respectée pour chaque candidat
    return [liste_DistCoord(candidat, liste_candidat, inf, sup) for candidat in liste_candidat]

def global_DistanceCoord_Glouton (nb_candidat, liste_candidat, liste_score, *, inf=0, sup=DIST_MAX) :
    liste_distance_ForAll = liste_DistCoord_ForAll(liste_candidat, inf, sup) #On récupère tous les candidats respectant la contrainte de distance pour chaque candidat
    ens = set(liste_candidat) #L'ensemble initial est liste_candidat
    comite = [] 
    
    for i in range(nb_candidat) : #Tant que le comité n'est pas complet
        if not ens : #Si l'ensemble de choix est vide
            return None #Aucun comité
        candidat_maxScore = max(ens, key=lambda candidat: candidat.visibilite*liste_score[liste_candidat.index(candidat)])  #On sélectionne le candidat qui maximise son score en prennant en compte sa visibilité
        comite.append(candidat_maxScore) #On l'ajoute dans le comité
        liste_distance_ForAll = MA.delForAllList(liste_distance_ForAll, candidat_maxScore) #On retire ce candidat de toutes les listes pour pas qu'il soit choisi une autre fois
        ens = ens.intersection(liste_distance_ForAll[liste_candidat.index(candidat_maxScore)]) #On réitère sur l'intersection de l'ensemble précédent et de la liste des candidats respectant la contrainte de distance du candidat sélectionné
    return comite
"""



#ÉLÉCTION COMITÉ



def election_comite (nb_comite, nb_candidat, liste_candidat, liste_score, liste_global, matrice_indiv) : #Renvoie une liste des nb_comite 1ers comités de nb_candidat candidats vérifiants toutes les contraintes
    ensComite_CGlobal = procede_CGlobale(nb_candidat, liste_global, liste_candidat) #Récupérer l'ensemble des comités vérifiant les contraintes globales
    ensComite_CIndiv = procede_CIndiv(matrice_indiv, liste_candidat) #Récupérer l'ensemble des comités vérifiant les contraintes individuelles
    ensComite_valide = intersection(ensComite_CGlobal, ensComite_CIndiv) #Récupérer l'ensemble des comités vérifiant toutes les contraintes
    liste_Fset_comite = classement_comite(nb_comite, ensComite_valide, liste_candidat, liste_score) #Récupérer un classement des comités 
    liste_tuple_comite = listFset_into_listTuple(liste_Fset_comite) #Transformer le type de chaque comités (ensemble -> tuple) pour pouvoir manipuler
    return liste_tuple_comite


