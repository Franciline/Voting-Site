import pytest
from election.classe import *
from election.ranking.initR import *
from election.ranking.voteR import *
from election.ranking.statsR import *
from election.ranking.comiteR import *
from math import sqrt



a = Candidat('A', (0,0), 0.70, 'F', 20)
b = Candidat('B', (1,0), 0.20, 'H', 30)
c = Candidat('C', (0,1), 0.80, 'F', 25)
d = Candidat('D', (1,1), 0.50, 'H', 45)



def test_verif () :
    assert lenEqual_ForAll([[a, b], 
                            [b, a]], 2) == None
    
    assert lenEqual_ForAll([[a, b, b], 
                            [b, a]], 2) == [a, b, b]

    assert allInList_ForAll([[a, b], 
                            [b, a]], [a, b]) == None
    
    assert allInList_ForAll([[a, b], 
                            [b]], [a, b]) == [b]
    
    pytest.raises(AucunCandidat, verif_liste_vote_Ranking, [a], [])

    pytest.raises(AucunVote, verif_liste_vote_Ranking, [], [a])

    with pytest.raises(VoteInvalide) as info :
        verif_liste_vote_Ranking([[b, c], 
                                  [b, a]], [a, b])
    assert info.value.args[0] == [b, c]

    with pytest.raises(VoteInvalide) as info :
        verif_liste_vote_Ranking([[a, b], 
                                  [a, a, b]], [a, b])
    assert info.value.args[0] == [a, a, b]



def test_posAlea() :
    for pos in [posAlea() for i in range(100)] :
        assert COORD_MIN <= pos[0] <= COORD_MAX and COORD_MIN <= pos[1] <= COORD_MAX
    
    i=0
    for candidat in creer_liste_candidat(3) :
        assert COORD_MIN <= candidat.coord[0] <= COORD_MAX and COORD_MIN <= candidat.coord[1] <= COORD_MAX
        assert candidat.nom == ['Candidat1', 'Candidat2', 'Candidat3'][i]
        i+=1

    for votant in creer_liste_votant(100) :
        assert COORD_MIN <= votant.coord[0] <= COORD_MAX and COORD_MIN <= votant.coord[1] <= COORD_MAX  



def test_creer_liste_vote_Ranking () :
    v0 = Votant((0, 0))
    v1 = Votant((2, 1))

    assert distanceAssoc(v0, a) == (0, a)
    assert distanceAssoc(v0, b) == (1, b)
    assert distanceAssoc(v0, c) == (1, c)
    assert distanceAssoc(v0, d) == (sqrt(2), d)

    assert creer_voteR(v0, [a, b, c, d]) == [a, b, c, d]
    assert creer_voteR(v1, [a, b, c, d]) == [d, b, c, a]
    
    liste_vote = creer_liste_voteR([v0, v1], [a, b, c, d])
    assert liste_vote == [[a, b, c, d], [d, b, c, a]]
    verif_liste_vote_Ranking(liste_vote, [a, b, c, d])



def test_pluralite () :
    assert pluralite(2*[[c, b, a, d]]+ 
                     1*[[a, b, d, c]]+
                     1*[[d, a, b, c]], [a, b, c, d]) == [c, [1, 0, 2, 1]]



def test_veto () :
    assert veto(2*[[c, b, a, d]]+ 
                1*[[a, b, d, c]]+
                1*[[d, a, b, c]], [a, b, c, d]) == [a, [0, 0, 2, 2]]



def test_borda () :
    assert borda(2*[[c, b, a, d]]+ 
                 1*[[a, b, d, c]]+
                 1*[[d, a, b, c]], [a, b, c, d]) == [a, [7, 7, 6, 4]]



def test_stv () :
    assert delForAllList([[a, b, c], 
                          [c, a, b], 
                          [b, a, c]], a) == [[b, c], 
                                             [c, b], 
                                             [b, c]]
    assert delForAllList([[a, b, c], 
                          [c, a, b], 
                          [b, a, c]], b) == [[a, c], 
                                             [c, a], 
                                             [a, c]]
    assert delForAllList([[a, b, c], 
                          [c, a, b], 
                          [b, a, c]], c) == [[a, b], 
                                             [a, b], 
                                             [b, a]]

    assert ordreElim_into_listeScore([a, b, c, d], [d, a, c, b]) == [1, 3, 2, 0]

    assert stv(3*[[a, d, b, c]]+ 
               4*[[b, d, a, c]]+ 
               3*[[c, d, a, b]]+ 
               2*[[d, c, b, a]], [a, b, c, d]) == [b, [1, 3, 2, 0], [d, a, c]]



def test_scoreSup () :
    assert scoreSup_inVote([c, d, a, b], a, [a, b, c, d]) == [0, 1, -1, -1]
    assert scoreSup_inVote([c, d, a, b], b, [a, b, c, d]) == [-1, 0, -1, -1]
    assert scoreSup_inVote([c, d, a, b], c, [a, b, c, d]) == [1, 1, 0, 1]
    assert scoreSup_inVote([c, d, a, b], d, [a, b, c, d]) == [1, 1, -1, 0]

    assert scoreSup_inVote([b, c, d, a], a, [a, b, c, d]) == [0, -1, -1, -1]
    assert scoreSup_inVote([b, c, d, a], b, [a, b, c, d]) == [1, 0, 1, 1]
    assert scoreSup_inVote([b, c, d, a], c, [a, b, c, d]) == [1, -1, 0, 1]
    assert scoreSup_inVote([b, c, d, a], d, [a, b, c, d]) == [1, -1, -1, 0]

    assert scoreSup_ForAllVote([[c, d, a, b], 
                                [b, c, d, a]], a, [a, b, c, d]) == [0, 0, -2, -2]
    
    assert scoreSup_ForAllVote([[c, d, a, b], 
                                [b, c, d, a]], b, [a, b, c, d]) == [0, 0, 0, 0]
    
    assert scoreSup_ForAllVote([[c, d, a, b], 
                                [b, c, d, a]], c, [a, b, c, d]) == [2, 0, 0, 2]
    
    assert scoreSup_ForAllVote([[c, d, a, b], 
                                [b, c, d, a]], d, [a, b, c, d]) == [2, 0, -2, 0]

    assert scoreSup_ForAll([[c, d, a, b], 
                            [b, c, d, a]], [a, b, c, d]) == [[0, 0, -2, -2], 
                                                             [0, 0, 0, 0], 
                                                             [2, 0, 0, 2], 
                                                             [2, 0, -2, 0]]



def test_scoreCopeland () :
    assert scoreCopeland([0, 0, -2, -2]) == [0.5, 0, 0]
    assert scoreCopeland([0, 0, 0, 0]) == [0.5, 0.5, 0.5]
    assert scoreCopeland([2, 0, 0, 2]) == [1, 0.5, 1]
    assert scoreCopeland([2, 0, -2, 0]) == [1, 0, 0.5]

    assert scoreCopeland_ForAll([[0, 0, -2, -2], 
                                 [0, 0, 0, 0], 
                                 [2, 0, 0, 2], 
                                 [2, 0, -2, 0]]) == [[0.5, 0, 0], 
                                                     [0.5, 0.5, 0.5], 
                                                     [1, 0.5, 1], 
                                                     [1, 0, 0.5]]



def test_condorcet_copeland () :
    assert condorcet([[a, b, d, c], 
                      [d, b, a, c], 
                      [c, a, b, d]], [a, b, c, d]) == [a, [3, 2, 0, 1]]

    assert condorcet([[a, b, d, c], 
                      [d, b, c, a], 
                      [c, a, b, d]], [a, b, c, d]) == [None, [2, 2, 1, 1]]
    
    assert copeland([[c, d, a, b], 
                     [b, c, d, a]], [a, b, c, d]) == [c, [0.5, 1.5, 2.5, 1.5]]



def test_simpson () :
    assert scoreDef_ForAllVote(2*[[a, b, d, c]]+ 
                               1*[[d, b, c, a]]+ 
                               2*[[c, a, b, d]]+ 
                               1*[[d, b, a, c]], a, [a, b, c, d]) == [0, 2, 3, 2]
    
    assert scoreDef_ForAllVote(2*[[a, b, d, c]]+ 
                               1*[[d, b, c, a]]+ 
                               2*[[c, a, b, d]]+ 
                               1*[[d, b, a, c]], b, [a, b, c, d]) == [4, 0, 2, 2]
    
    assert scoreDef_ForAllVote(2*[[a, b, d, c]]+ 
                               1*[[d, b, c, a]]+ 
                               2*[[c, a, b, d]]+ 
                               1*[[d, b, a, c]], c, [a, b, c, d]) == [3, 4, 0, 4]
    
    assert scoreDef_ForAllVote(2*[[a, b, d, c]]+ 
                               1*[[d, b, c, a]]+ 
                               2*[[c, a, b, d]]+ 
                               1*[[d, b, a, c]], d, [a, b, c, d]) == [4, 4, 2, 0]

    assert scoreDef_ForAll(2*[[a, b, d, c]]+
                           1*[[d, b, c, a]]+
                           2*[[c, a, b, d]]+
                           1*[[d, b, a, c]], [a, b, c, d]) == [[0, 2, 3, 2], 
                                                               [4, 0, 2, 2], 
                                                               [3, 4, 0, 4], 
                                                               [4, 4, 2, 0]]
    
    assert scoreDef_loose ([0, 2, 0, 2], [0, 2, 3, 2]) == [0, 3]
    assert scoreDef_loose ([-2, 0, 2, 2], [4, 0, 2, 2]) == [4, 0]
    assert scoreDef_loose ([0, -2, 0, -2], [3, 4, 0, 4]) == [3, 4, 0, 4]
    assert scoreDef_loose ([-2, -2, 2, 0], [4, 4, 2, 0]) == [4, 4, 0]

    assert scoreDef_loose_ForAll([[0, 2, 0, 2], 
                                  [-2, 0, 2, 2], 
                                  [0, -2, 0, -2], 
                                  [-2, -2, 2, 0]], [[0, 2, 3, 2], 
                                                    [4, 0, 2, 2], 
                                                    [3, 4, 0, 4], 
                                                    [4, 4, 2, 0]]) == [[0, 3], 
                                                                       [4, 0], 
                                                                       [3, 4, 0, 4], 
                                                                       [4, 4, 0]]

    assert simpson(2*[[a, b, d, c]]+
                   1*[[d, b, c, a]]+
                   2*[[c, a, b, d]]+
                   1*[[d, b, a, c]], [a, b, c, d]) == [a, [3, 4, 4, 4]]



def test_satisf () :
    cc1 = Candidat('A', (1, 1))
    cc2 = Candidat('B', (2, 3))
    cc3 = Candidat('C', (4, 1))
    vc1 = Votant((0, 0))
    vc2 = Votant((3, 2))
    vc3 = Votant((1, 4))

    maxSatisf, liste_satisf = candidat_maxSatisf([vc1, vc2, vc3], [cc1, cc2, cc3])
    assert maxSatisf == [1/(sqrt(13)+2*sqrt(2)), cc2]
    assert liste_satisf == [1/(sqrt(2)+sqrt(5)+3),         #~ 0.15037
                            1/(sqrt(13)+2*sqrt(2)),        #~ 0.15542
                            1/(sqrt(17)+sqrt(2)+sqrt(18))] #~ 0.10225
    
    assert candidat_satisfPercent(maxSatisf, liste_satisf, cc1, [cc1, cc2, cc3]) == 96.747 #round (, 3)
    assert candidat_satisfPercent(maxSatisf, liste_satisf, cc2, [cc1, cc2, cc3]) == 100.0  #round (, 3)
    assert candidat_satisfPercent(maxSatisf, liste_satisf, cc3, [cc1, cc2, cc3]) == 65.787 #round (, 3)

    assert satisf([vc1, vc2, vc3], [cc1, cc2, cc3]) == [96.747, 100.0, 65.787]



def test_delegation () : 
    d0 = VotantPoids((0, 0), random())
    d1 = VotantPoids((0, 1), random())
    d2 = VotantPoids((1, 1), random())
    assert (d0.delegue, d0.poids) == (False, 1)
    assert (d1.delegue, d1.poids) == (False, 1)
    assert (d2.delegue, d2.poids) == (False, 1)

    d0.delegation(d1) 
    assert (d0.delegue, d0.poids) == (True, 0)
    assert (d1.delegue, d1.poids) == (False, 2)
    d0.delegation(d1) 
    assert (d0.delegue, d0.poids) == (True, 0)
    assert (d1.delegue, d1.poids) == (False, 2)
    d1.delegation(d1) 
    assert (d0.delegue, d0.poids) == (True, 0)
    assert (d1.delegue, d1.poids) == (False, 2)
    d1.delegation(d2) 
    assert (d1.delegue, d1.poids) == (True, 0)
    assert (d2.delegue, d2.poids) == (False, 3)



def test_liquide () :
    c1 = Candidat("Candidat1", (50, 50))
    c2 = Candidat("Candidat2", (100, 200))
    c3 = Candidat("Candidat3", (200, 100))
    v1 = VotantPoids((100, 100), random())
    v2 = VotantPoids((150, 150), random())
    v3 = VotantPoids((200, 100), random())
    v4 = VotantPoids((200, 0), random())
    v5 = VotantPoids((150, 100), random())
    liste_candidat = [c1, c2, c3]
    liste_votantPoids = [v1, v2, v3, v4, v5]

    assert proximite(v1, liste_votantPoids, sqrt(5000)) == [v2, v5]
    assert proximite(v2, liste_votantPoids, sqrt(5000)) == [v1, v3, v5]
    assert proximite(v3, liste_votantPoids, sqrt(5000)) == [v2, v5]
    assert proximite(v4, liste_votantPoids, sqrt(5000)) == []
    assert proximite(v5, liste_votantPoids, sqrt(5000)) == [v1, v2, v3]

    v5.delegation(v1)

    assert proximite_not_delegue([v2, v5]) == [v2]
    assert proximite_not_delegue([v1, v3, v5]) == [v1, v3]
    assert proximite_not_delegue([v2, v5]) == [v2]
    assert proximite_not_delegue([]) == []
    assert proximite_not_delegue([v1, v2, v3]) == [v1, v2, v3]


    valeur = valeur_proximite( proba_proximite([v1, v2, v3]) )
    assert 0 <= valeur[0][0] <= valeur[1][0] <= valeur[2][0]
    assert abs(1-valeur[2][0]) <= 0.0000000001

    assert concat_all([[1, 2], [3, 4], [5, 6]]) == [1, 2, 3, 4, 5, 6]

    liste_vote = creer_liste_votePoidsR(liste_votantPoids, liste_candidat, sqrt(5000))

    print("Poids des votantPoids :")
    for votantPoids in liste_votantPoids :
        print(votantPoids.poids)

    print()

    print("Liste des votes selon le poids des votantPoids : ")
    for vote in liste_vote :
        print(vote[0].aff('nom'), vote[1].aff('nom'), vote[2].aff('nom'))




def test_contrainte_individuelles () :
    assert contrainte_Nom(a, "A", "Z") == True
    assert contrainte_Nom(b, "M", "Z") == False
    assert contrainte_Nom(c, "a", "z") == False
    assert contrainte_Nom(d, "", "Diamant") == True
    assert compress_Nom([a, b, c, d], inf="Améthyste" ,sup="Cristal") == {b, c}
    
    assert contrainte_CoordX(a, 1, 5) == False
    assert contrainte_CoordX(b, 1, 5) == True
    assert compress_CoordX([a, b, c, d], inf=1 ,sup=5) == {b, d}

    assert contrainte_CoordY(c, 1, 5) == True
    assert contrainte_CoordY(d, 1, 5) == True
    assert compress_CoordY([a, b, c, d], inf=1 ,sup=5) == {c, d}

    assert contrainte_Visibilite(a, inf=0.10, sup=0.60) == False
    assert contrainte_Visibilite(b, inf=0.10, sup=0.60) == True
    assert compress_Visibilite([a, b, c, d], inf=0.10 ,sup=0.60) == {b, d}

    assert contrainte_Sexe(a, sexe='F') == True
    assert contrainte_Sexe(b, sexe='F') == False
    assert compress_Sexe([a, b, c, d], sexe='F') == {a, c}

    assert contrainte_Age(a, inf=18, sup=25) == True
    assert contrainte_Age(b, inf=18, sup=25) == False
    assert compress_Age([a, b, c, d], inf=18, sup=25) == {a, c}



def test_manipulation_types () :
    assert ens_into_setFset({1, 2, 3, 
                             (1, 2), 
                             (1, 3),
                             (2, 3)}) == {frozenset({1}), 
                                          frozenset({2}), 
                                          frozenset({3}),
                                          frozenset({1, 2}), 
                                          frozenset({1, 3}), 
                                          frozenset({2, 3})}
    
    assert listFset_into_listTuple([frozenset({1}), 
                                    frozenset({2}), 
                                    frozenset({3}),
                                    frozenset({1, 2}), 
                                    frozenset({1, 3}), 
                                    frozenset({2, 3}), 
                                    None]) == [(1, ), 
                                               (2, ), 
                                               (3, ), 
                                               (1, 2), 
                                               (1, 3), 
                                               (2, 3), 
                                               None]

    assert union({1, 2, 3, frozenset({1, 2}), frozenset({1, 3})}, 
                 {2, 3, frozenset({1, 3}), frozenset({2, 3})},
                 {3, frozenset({1, 2, 3}), frozenset({1, 3, 2})}) == {1, 2, 3, 
                                                                      frozenset({1, 2}), 
                                                                      frozenset({1, 3}), 
                                                                      frozenset({2, 3}), 
                                                                      frozenset({1, 2, 3})}
    
    assert intersection({1, 2, 3, 
                          frozenset({1, 2}), 
                          frozenset({1, 3}), 
                          frozenset({2, 3})}, 
                        {2, 3, 4, 
                          frozenset({2, 3}), 
                          frozenset({2, 4}), 
                          frozenset({3, 4})}, 
                        {1, 2, 3, 4, 
                          frozenset({1, 2}), 
                          frozenset({3, 4}), 
                          frozenset({2, 3})}) == {2, 3, frozenset({2, 3})}



def test_combi_fusion () :
    assert fusion(frozenset({d}), 
                  {a, b, c,
                    frozenset({a, b}),
                    frozenset({a, c}),
                    frozenset({b, c})}) == {frozenset({a, d}), 
                                            frozenset({b, d}), 
                                            frozenset({c, d}),
                                            frozenset({a, b, d}), 
                                            frozenset({a, c, d}), 
                                            frozenset({b, c, d})}
    
    assert combi_fusion({frozenset({c}), 
                         frozenset({d}), 
                         frozenset({c, d})}, 
                        {a, b,
                         frozenset({a}),
                         frozenset({b}),
                         frozenset({a, b})}) == {frozenset({a, c}), frozenset({b, c}), frozenset({a, b, c}), 
                                                 frozenset({a, d}), frozenset({b, d}), frozenset({a, b, d}),
                                                 frozenset({a, c, d}), frozenset({b, c, d}), frozenset({a, b, c, d})}



def test_procede_CIndiv () :
    assert combi_CIndiv([{a, b, c}, 
                         {c}, 
                         {b, d}]) == {frozenset({a, c, b}), frozenset({a, c, d}), 
                                      frozenset({b, c}), frozenset({b, c, d}), 
                                      frozenset({c, d})}
    
    assert procede_CIndiv([[[], [], [], [], [], []], 
                           [[], [], [], [], [], []]], [a, b, c, d]) == {frozenset({a, b}), frozenset({a, c}), frozenset({a, d}), 
                                                                        frozenset({b, c}), frozenset({b, d}), 
                                                                        frozenset({c, d})}
    
    assert procede_CIndiv([[[], [0, 0], [],     [], [], []], 
                           [[], [],     [1, 1], [], [], []]], [a, b, c, d]) == {frozenset({a, c}), 
                                                                                frozenset({a, d}), 
                                                                                frozenset({c, d})}
    
    assert procede_CIndiv([[[], [], [], [], ['F'], []        ], 
                           [[], [], [], [], [],    [None, 30]]], [a, b, c, d]) == {frozenset({a, b}), 
                                                                                   frozenset({a, c}), 
                                                                                   frozenset({c, b})}
    
    assert procede_CIndiv([[["B", "D"], [], [], [],           [], []], 
                           [[]        , [], [], [0.60, None], [], []]], [a, b, c, d]) == {frozenset({b, a}), 
                                                                                          frozenset({b, c}), 
                                                                                          frozenset({c, a}), 
                                                                                          frozenset({d, a}), 
                                                                                          frozenset({d, c})}



def test_global_PariteSexe () :
    assert verif_percentHF(None, None) == (0.50, 0.50)
    assert verif_percentHF(0.75, None) == (0.75, 0.25)
    assert verif_percentHF(None, 0.75) == (0.25, 0.75)
    assert verif_percentHF(0.25, 0.75) == (0.25, 0.75)
    assert verif_percentHF(0.85, 0.65) == (0.50, 0.50)

    assert partage_nbHF(10, 0.5, 0.5) == (5, 5)
    assert partage_nbHF(10, 0.75, 0.25) == (7, 3)
    assert partage_nbHF(10, 0.76, 0.24) == (8, 2)

    assert global_PariteSexe(3, [a, b, c, d], percent_H=0.33, percent_F=0.67) == {frozenset({b, a, c}), 
                                                                                  frozenset({d, a, c})}

    assert global_PariteSexe(2, [a, b, c, d], percent_H=0, percent_F=1) == {frozenset({a, c})}

    assert global_PariteSexe(2, [a, b, c, d]) == {frozenset({b, a}), frozenset({b, c}), 
                                                  frozenset({d, a}), frozenset({d, c})}
    
    assert global_PariteSexe(3, [a, b, c, d], percent_H=1) == set()



def test_global_DistanceCoord () :
    assert candidat_CDistCoord(a, b, inf=1, sup=1.25) == True
    assert candidat_CDistCoord(a, d, inf=1, sup=1.25) == False

    assert comite_CDistCoord(frozenset({a, b, c}), inf=1, sup=1.5) == True
    assert comite_CDistCoord(frozenset({a, b, c}), inf=0, sup=1) == False
    assert comite_CDistCoord(frozenset({c, d}), inf=0, sup=1) == True
    assert comite_CDistCoord(frozenset({c, d}), inf=0, sup=0.5) == False

    assert global_DistanceCoord(2, [a, b, c, d], inf=1, sup=1) == {frozenset({a, b}), frozenset({a, c}), 
                                                                   frozenset({b, d}), frozenset({c, d})}

    assert global_DistanceCoord(2, [a, b, c, d], inf=1.25, sup=1.5) == {frozenset({a, d}), 
                                                                        frozenset({b, c})}

    assert global_DistanceCoord(2, [a, b, c, d]) == {frozenset({a, b}), frozenset({a, c}), frozenset({a, d}), 
                                                     frozenset({b, c}), frozenset({b, d}), 
                                                     frozenset({c, d})}

    assert global_DistanceCoord(2, [a, b, c, d], inf=2, sup=3) == set()



def test_procede_CGlobale () :
    assert procede_CGlobale(2, 
                            [[], []], 
                            [a, b, c, d]) == {frozenset({a, b}), frozenset({a, c}), frozenset({a, d}), 
                                              frozenset({b, c}), frozenset({b, d}), 
                                              frozenset({c, d})}
    
    assert procede_CGlobale(2, 
                            [[None, None], [1, 1]], 
                            [a, b, c, d]) == {frozenset({a, b}), frozenset({c, d})}



def test_select_comite () :
    assert scoreComiteAssoc(frozenset({a, b}), [a, b, c, d], [65, 50, 90, 75]) == (45.5 + 10, frozenset({a, b})) #(45.5 + 10, _)
    assert scoreComiteAssoc(frozenset({c, d}), [a, b, c, d], [65, 50, 90, 75]) == (72 + 37.5, frozenset({c, d})) #(72 + 37.5, _)

    assert scoreComiteAssoc_ForAll({frozenset({a, b, c}), 
                                    frozenset({a, b, d}), 
                                    frozenset({a, c, d}), 
                                    frozenset({b, c, d})}, 
                                   [a, b, c, d], 
                                   [65, 50, 90, 75]) == {(45.5 + 10 + 72, frozenset({a, b, c})),   #(127.5, _)
                                                         (45.5 + 10 + 37.5, frozenset({a, b, d})), #(93, _)
                                                         (45.5 + 72 + 37.5, frozenset({a, c, d})), #(155, _)
                                                         (10 + 72 + 37.5, frozenset({b, c, d}))}   #(119.5, _)
    
    assert maxScoreComite({frozenset({a, b, c}), 
                           frozenset({a, b, d}), 
                           frozenset({a, c, d}), 
                           frozenset({b, c, d})},
                          [a, b, c, d], 
                          [65, 50, 90, 75]) == frozenset({a, c, d})
    
    assert classement_comite(5, 
                             {frozenset({a, b, c}), 
                              frozenset({a, b, d}), 
                              frozenset({a, c, d}), 
                              frozenset({b, c, d})}, 
                             [a, b, c, d], 
                             [65, 50, 90, 75]) == [frozenset({a, c, d}), 
                                                   frozenset({a, b, c}), 
                                                   frozenset({b, c, d}), 
                                                   frozenset({a, b, d}), 
                                                   None]
    
    listTuple1 = election_comite(7, 
                                 2, 
                                 [a, b, c, d], 
                                 [65, 50, 90, 75], 
                                 [[], []], 
                                 [[[], [], [], [], [], []], 
                                  [[], [], [], [], [], []]])
    listTuple2 = [(a, c), (c, d), (a, d), (b, c), (a, b), (b, d), None]
    assert [e in listTuple1 if e==None else (e[0], e[1]) in listTuple1 or (e[1], e[0]) in listTuple1 for e in listTuple2] == [True]*len(listTuple1)
    
    listTuple1 = election_comite(3, 
                                 2, 
                                 [a, b, c, d], 
                                 [65, 50, 90, 75], 
                                 [[None, None], []], 
                                 [[[], [], [], [], ['F'], []        ], 
                                  [[], [], [], [], [],    [None, 30]]])
    listTuple2 = [(b, c), (a, b), None]
    assert [e in listTuple1 if e==None else (e[0], e[1]) in listTuple1 or (e[1], e[0]) in listTuple1 for e in listTuple2] == [True]*len(listTuple1)

    listTuple1 = election_comite(3, 
                                 2, 
                                 [a, b, c, d], 
                                 [65, 50, 90, 75], 
                                 [[], [1, 1]], 
                                 [[["B", "D"], [], [], [],           [], []], 
                                  [[],         [], [], [0.60, None], [], []]])
    listTuple2 = [(a, c), (c, d), (a, b)]
    assert [e in listTuple1 if e==None else (e[0], e[1]) in listTuple1 or (e[1], e[0]) in listTuple1 for e in listTuple2] == [True]*len(listTuple1)

    listTuple1 = election_comite(3, 
                                 2, 
                                 [a, b, c, d], 
                                 [65, 50, 90, 75], 
                                 [[None, None], [1, 1]], 
                                 [[["B", "D"], [], [], [],           ['H'], []        ], 
                                  [[],         [], [], [0.60, None], [],    [None, 30]]])
    listTuple2 = [(c, d), (a, b), None]
    assert [e in listTuple1 if e==None else (e[0], e[1]) in listTuple1 or (e[1], e[0]) in listTuple1 for e in listTuple2] == [True]*len(listTuple1)

    listTuple1 = election_comite(3, 
                                 2, 
                                 [a, b, c, d], 
                                 [65, 50, 90, 75], 
                                 [[None, None], [1, 1]], 
                                 [[["B", "D"], [], [], [],           ['F'], []        ], 
                                  [[],         [], [], [0.60, None], [],    [None, 30]]])
    listTuple2 = [None, None,  None]
    assert [e in listTuple1 if e==None else (e[0], e[1]) in listTuple1 or (e[1], e[0]) in listTuple1 for e in listTuple2] == [True]*len(listTuple1)



