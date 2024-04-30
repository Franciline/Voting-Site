from .initR import distanceAssoc



def candidat_maxSatisf (liste_votant, liste_candidat) : #Calcule et associe maxSatisf avec le candidat associé et les autres satisf 
    liste_sumDist = [0]*len(liste_candidat) #Créer une liste de distance
    for votant in liste_votant : #Pour chaque votant
        for i in range(len(liste_candidat)) : #Pour tous les candidats
            liste_sumDist[i] += distanceAssoc(votant, liste_candidat[i])[0] #Additionner la distance à l'indice correspondant
    liste_satisf = [1/sumDist for sumDist in liste_sumDist] #Calculer la satisf de chaque candidat
    maxSatisf = max(liste_satisf)
    maxSatisf = [maxSatisf, liste_candidat[liste_satisf.index(maxSatisf)]] #Associer maxSatisf au candidat correspondant
    return [maxSatisf, liste_satisf]

def candidat_satisfPercent (maxSatisf, liste_satisf, candidat, liste_candidat) : #Calcule la satisf (%) du candidat par rapport à maxSatisf
    return round((liste_satisf[liste_candidat.index(candidat)]/maxSatisf[0])*100, 3)

def satisf (liste_votant, liste_candidat) :
    maxSatisf, liste_satisf = candidat_maxSatisf(liste_votant, liste_candidat)
    return [candidat_satisfPercent(maxSatisf, liste_satisf, candidat, liste_candidat) for candidat in liste_candidat]


