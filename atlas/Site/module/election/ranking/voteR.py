from ..classe import AucunCandidat, AucunVote, VoteInvalide



#MÉTHODES POUR LES VÉRIFICATIONS



def lenEqual_ForAll (liste_vote, nb_candidat) : #Retourne un vote invalide si il y en a, None sinon
    for vote in liste_vote :
        if len(vote) != nb_candidat :
            return vote
    return None

def allInList_ForAll (liste_vote, liste_candidat) : #Retourne un vote invalide si il y en a, None sinon
    for vote in liste_vote :
        for candidat in liste_candidat :
            if candidat not in vote :
                return vote
    return None

def verif_liste_vote_Ranking (liste_vote, liste_candidat) : #Vérifie liste_vote et liste_candidat pour les méthodes de Ranking
    if not liste_candidat : #Vérification si liste_candidat vide
        raise AucunCandidat()
    if not liste_vote : #Vérification si liste_vote vide
        raise AucunVote()
    vote = allInList_ForAll(liste_vote, liste_candidat)
    if vote != None : #Vérification si tous les candidats sont dans chaque vote
        raise VoteInvalide(vote)
    vote = lenEqual_ForAll(liste_vote, len(liste_candidat))
    if vote != None : #Vérifications si chaque vote possède autant de nom que de candidat
        raise VoteInvalide(vote)



#MÉTHODES POUR LES ÉLÉCTIONS



def pluralite (liste_vote, liste_candidat) : #Méthode pour le vote pluralité
    """Départage les égalités par le 1er candidat dans l'ordre de liste_candidat"""
    verif_liste_vote_Ranking(liste_vote, liste_candidat)
    liste_1er = [0]*len(liste_candidat)
    for vote in liste_vote : #Pour chaque vote
        liste_1er[liste_candidat.index(vote[0])] += 1 #Incrémenter de 1 le nombre de 1er du candidat étant classé 1er
    elu = liste_candidat[liste_1er.index(max(liste_1er))] #Élire le candidat qui a le nombre maximal de 1er
    return [elu, liste_1er]



def veto (liste_vote, liste_candidat) : #Méthode pour le vote veto
    """Départage les égalités par le 1er candidat dans l'ordre de liste_candidat"""
    verif_liste_vote_Ranking(liste_vote, liste_candidat)
    liste_veto = [0]*len(liste_candidat)
    for vote in liste_vote : #Pour chaque vote
        liste_veto[liste_candidat.index(vote[-1])] += 1 #Incrémenter de 1 le nombre de veto du candidat ayant reçu un veto
    elu = liste_candidat[liste_veto.index(min(liste_veto))] #Élire le candidat qui a le nombre minimal de veto
    return [elu, liste_veto]



def borda (liste_vote, liste_candidat) :
    """Départage les égalités par le 1er candidat dans l'ordre de liste_candidat"""
    verif_liste_vote_Ranking(liste_vote, liste_candidat)
    nb_candidat = len(liste_candidat)
    liste_score = [0]*nb_candidat
    for vote in liste_vote : #Pour chaque vote
        for nom in vote : #Pour chaque nom
            liste_score[liste_candidat.index(nom)] += nb_candidat-1-vote.index(nom) #Augmenter son score selon son classement
    elu = liste_candidat[liste_score.index(max(liste_score))] #Élire le candidat avec le score maximal
    return [elu, liste_score]



#Méthodes servant le vote stv

def delForAllList (liste_liste, candidat) : #Supprime un candidat de toutes les listes d'une liste
    return [[obj for obj in liste if obj!=candidat] for liste in liste_liste]

def ordreElim_into_listeScore (liste_candidat, ordreElim) :
    return [ordreElim.index(candidat) for candidat in liste_candidat]

def stv (liste_vote, liste_candidat, en_lice=[], ordreElim=[]) : #Méthode pour le vote Élimination Successive
    """Élimine le 1er candidat dans liste_candidat si il y a égalité entre 2 candidat"""
    if not en_lice : #Si la fonction est appelée pour la 1ère fois
        en_lice = liste_candidat #Tous les candidats de liste_candidat sont encore en lice
    verif_liste_vote_Ranking(liste_vote, en_lice) #Vérifivation le liste_vote avec en_lice
    if len(en_lice) == 1 : #Si il n'y a qu'un seul candidat en lice
        liste_score = ordreElim_into_listeScore(liste_candidat, ordreElim+en_lice) #Déterminer le score
        return [en_lice[0], liste_score, ordreElim] #L'élire et renvoyer la liste des scores et des éléminés
    else :
        liste_1er = [0]*len(en_lice)
        for vote in liste_vote : #Pour chaque vote
            liste_1er[en_lice.index(vote[0])] += 1 #Incrémenter de 1 le nombre de 1er pour le candidat classé en 1er
        dernier = en_lice[liste_1er.index(min(liste_1er))] #Sélectionner le candidat avec le moins 1er
        liste_vote = delForAllList(liste_vote, dernier) #L'enlever de tous les votes
        en_lice = [candidat for candidat in en_lice if candidat!=dernier] #L'enlever des candidats en lice
        ordreElim.append(dernier) #Le rajouter dans la liste des éliminés
        return stv(liste_vote, liste_candidat, en_lice, ordreElim) #Itérer avec les listes nouvelles listes



#Méthodes servant le vote condorcet/copeland/simpson

def scoreSup_inVote (vote, candidat, liste_candidat) : #Retourne le score du candidat pour le vote en paramètre
    return [0 if nom==candidat else 1 if vote.index(candidat)<vote.index(nom) else -1 for nom in liste_candidat]

def scoreSup_ForAllVote (liste_vote, candidat, liste_candidat) : #Retourne le score total du candidat pour tous les votes
    liste_scoreSup = [scoreSup_inVote(vote, candidat, liste_candidat) for vote in liste_vote] #Créer une liste de score pour le candidat
    totalScore = [sum(scoreSup) for scoreSup in zip(*liste_scoreSup)] #Additionne le score de tous les votes du candidat
    return totalScore

def scoreSup_ForAll (liste_vote, liste_candidat) : #Retourne les scores totaux de tous les candidats
    liste_totalScore = [scoreSup_ForAllVote(liste_vote, candidat, liste_candidat) for candidat in liste_candidat]
    return liste_totalScore

def scoreCopeland (totalScore) : #Régularise le score d'un candidat selon la règle de Copeland
    totalScore.remove(0)
    return [1 if score>0 else 0 if score<0 else 0.5 for score in totalScore]

def scoreCopeland_ForAll (liste_totalScore) : #Régularise les scores totaux de tous les candidats selon la règle de Copeland
    return [scoreCopeland(totalScore) for totalScore in liste_totalScore]



def condorcet (liste_vote, liste_candidat) : #Méthode pour le vote Condorcet sans règle supplémentaire
    """Pas d'égalité possible"""
    verif_liste_vote_Ranking(liste_vote, liste_candidat)
    liste_scoreTotal = scoreSup_ForAll(liste_vote, liste_candidat) #Prendre la liste des scores totaux des candidats
    liste_scoreCopeland = scoreCopeland_ForAll(liste_scoreTotal) #Régularise la liste de score selon la règle de Copeland
    liste_scoreCopeland = [sum(scoreCopeland) for scoreCopeland in liste_scoreCopeland] #Additionne tous les scores de chaque candidat
    scoreMax = len(liste_candidat)-1 
    if scoreMax in liste_scoreCopeland : #Si il existe un candidat qui gagne tous les duels
        elu = liste_candidat[liste_scoreCopeland.index(scoreMax)] # L'élire
    else : #Sinon
        elu = None #Aucun gagnant
    return [elu, liste_scoreCopeland]

def copeland (liste_vote, liste_candidat) : #Méthode pour le vote Condorcet selon la règle de Copeland
    """Départage les égalités par le 1er candidat dans l'ordre de liste_candidat"""
    verif_liste_vote_Ranking(liste_vote, liste_candidat) 
    liste_scoreTotal = scoreSup_ForAll(liste_vote, liste_candidat) #Prendre la liste des scores totaux des candidats
    liste_scoreCopeland = scoreCopeland_ForAll(liste_scoreTotal) #Régularise la liste de score selon la règle de Copeland
    liste_scoreCopeland = [sum(scoreCopeland) for scoreCopeland in liste_scoreCopeland] #Additionne tous les scores de chaque candidat
    elu = liste_candidat[liste_scoreCopeland.index(max(liste_scoreCopeland))] #Élire le candidat qui gagne le plus de duel
    return [elu, liste_scoreCopeland]



def scoreDef_ForAllVote (liste_vote, candidat, liste_candidat) : #Renvoie la liste du nombre de defaites par duel pour un candidat
    liste_scoreSup = [scoreSup_inVote(vote, candidat, liste_candidat) for vote in liste_vote] #Créer une liste de score pour le candidat
    liste_scoreDef = [[1 if duel==-1 else 0 for duel in scoreSup] for scoreSup in liste_scoreSup]
    liste_scoreDef = [sum(scoreDef) for scoreDef in zip(*liste_scoreDef)]
    return liste_scoreDef

def scoreDef_ForAll (liste_vote, liste_candidat) : #Renvoie la liste du nombre de defaites par duel pour chaque candidat
    return [scoreDef_ForAllVote(liste_vote, candidat, liste_candidat) for candidat in liste_candidat]

def scoreDef_loose (totalScore, scoreDef) : #Renvoie une liste du nombre de défaites par duel perdu
    defaites = []
    for i in range (len(totalScore)) : #Pour chaque score
        if totalScore[i] <= 0 : #Si le duel est perdu
            defaites.append(scoreDef[i]) #Garder ce score de défaite
    return defaites 

def scoreDef_loose_ForAll (liste_totalScore, liste_scoreDef) : #Renvoie une liste du nombre de défaites par duel perdu pour chaque candidat
    return [scoreDef_loose(totalScore, scoreDef) for totalScore, scoreDef in zip(liste_totalScore, liste_scoreDef)]

def simpson (liste_vote, liste_candidat) : #Méthode pour le vote Condorcet selon la règle de Simpson
    """Départage les égalités par le 1er candidat dans l'ordre de liste_candidat"""
    verif_liste_vote_Ranking(liste_vote, liste_candidat) 
    liste_scoreTotal = scoreSup_ForAll(liste_vote, liste_candidat) #Prendre la liste des scores totaux des candidats    
    liste_scoreDef = scoreDef_ForAll(liste_vote, liste_candidat) #Prendre la liste du nombre de défaites par duel pour chaque cnadidat
    liste_defaites = scoreDef_loose_ForAll (liste_scoreTotal, liste_scoreDef) #Garder seulement le nombre de défaites par duel perdu
    liste_maxDefaites = [max(defaites) for defaites in liste_defaites] #Créer la liste des défaites maximales par candidat
    elu = liste_candidat[liste_maxDefaites.index(min(liste_maxDefaites))] #Élire le candidat avec la défaite maximale la moins élevée
    return [elu, liste_maxDefaites]


