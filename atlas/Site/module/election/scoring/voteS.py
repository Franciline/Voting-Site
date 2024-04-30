from ..classe import AucunCandidat, AucunVote, VoteInvalide
from ..var import SCORE_MIN, SCORE_MAX



#MÉTHODES POUR LES VÉRIFICATIONS



def lenEqual_ForAll (liste_vote, nb_candidat) : #Retourne un vote invalide si il y en a, None sinon
    for vote in liste_vote :
        if len(vote) != nb_candidat :
            return vote
    return None

def InIntervalle_ForAll (liste_vote) : #Retourne un vote invalide si il y en a, None sinon
    for vote in liste_vote :
        for score in vote :
            if not SCORE_MIN <= score <= SCORE_MAX :
                return vote
    return None

def verif_liste_vote_Scoring (liste_vote, liste_candidat) : #Vérifie liste_vote et liste_candidat pour les méthodes de Scoring
    if not liste_candidat : #Vérification si liste_candidat vide
        raise AucunCandidat()
    if not liste_vote : #Vérification si liste_vote vide
        raise AucunVote()
    vote = InIntervalle_ForAll(liste_vote)
    if vote != None : #Vérification si tous les scores de chaque vote sont dans l'intervalle [0 ; SCORE_MAX]
        raise VoteInvalide(vote)
    vote = lenEqual_ForAll(liste_vote, len(liste_candidat))
    if vote != None : #Vérifications si chaque vote possède autant de score que de candidat
        raise VoteInvalide(vote)



#MÉTHODES POUR LES ÉLÉCTIONS



def maxSum (liste_vote, liste_candidat) : #Méthode pour le vote maxSum
    """Départage les égalités par le 1er candidat dans l'ordre de liste_candidat"""
    verif_liste_vote_Scoring(liste_vote, liste_candidat)
    liste_score = [sum(all_score_index) for all_score_index in (zip(*liste_vote))] #Additionne les scores de chaque vote par indice
    elu = liste_candidat[liste_score.index(max(liste_score))] #Élire le candidat qui a le score le plus élevé
    return [elu, liste_score]



#Méthodes servant le vote maxProd

def normalise2_vote (vote) : #Normalise un vote par des scores entre 1 et 2
    return [(score-1)/99 +1 for score in vote]

def normalise2_ForAll(liste_vote) : #Normalise tous les votes par des scores entre 1 et 2
    return [normalise2_vote(vote) for vote in liste_vote]

def produit (liste) : #Fait le produit de chaque élément d'une liste
    p = 1
    for element in liste :
        p *= element
    return p

def maxProd (liste_vote, liste_candidat) : #Méthode pour le vote maxProd
    """Départage les égalités par le 1er candidat dans l'ordre de liste_candidat"""
    verif_liste_vote_Scoring(liste_vote, liste_candidat)
    liste_vote_norm2 = normalise2_ForAll(liste_vote) #Normalise tous les votes par des scores entre 1 et 2
    liste_score = [produit(all_score_index) for all_score_index in zip(*liste_vote_norm2)] #Multiplie les scores de chaque vote par indice
    elu = liste_candidat[liste_score.index(max(liste_score))] #Élire le candidat qui a le score le plus élevé
    return [elu, liste_score]


