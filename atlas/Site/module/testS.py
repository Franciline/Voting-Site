import pytest
from election.classe import *
from election.scoring.initS import *
from election.scoring.voteS import *
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
    
    assert InIntervalle_ForAll([[SCORE_MIN, 42], 
                                [SCORE_MAX, 14]]) == None
    
    assert InIntervalle_ForAll([[SCORE_MIN-1, 50], 
                                [25, 75]]) == [SCORE_MIN-1, 50]
    
    assert InIntervalle_ForAll([[85, 30], 
                                [SCORE_MAX+1, 40]]) == [SCORE_MAX+1, 40]
    
    pytest.raises(AucunCandidat, verif_liste_vote_Scoring, [50], [])

    pytest.raises(AucunVote, verif_liste_vote_Scoring, [], [a])
    
    with pytest.raises(VoteInvalide) as info :
        verif_liste_vote_Scoring([[-5, 55], 
                                  [40, 65]], [a, b])
    assert info.value.args[0] == [-5, 55]

    with pytest.raises(VoteInvalide) as info :
        verif_liste_vote_Scoring([[10, 70], 
                                  [95]], [a, b])
    assert info.value.args[0] == [95]



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



def test_creer_liste_vote_Scoring () :
    assert distanceAssoc(a, a) == (0, a)
    assert distanceAssoc(a, b) == (1, b)
    assert distanceAssoc(a, c) == (1, c)
    assert distanceAssoc(a, d) == (sqrt(2), d)

    cc1 = Candidat('B', (COORD_MIN, COORD_MIN))
    cc2 = Candidat('A', (COORD_MAX*0.5, COORD_MAX*0.5))
    cc3 = Candidat('C', (COORD_MAX, COORD_MAX))
    vc1 = Votant((COORD_MIN, COORD_MIN))
    vc2 = Votant((COORD_MAX*0.5, COORD_MAX*0.5))

    s1, s2, s3, s4, s5 = [scoreDist(DIST_MAX), 
                          scoreDist(DIST_MAX*0.75), 
                          scoreDist(DIST_MAX*0.5), 
                          scoreDist(DIST_MAX*0.25), 
                          scoreDist(0)]
    assert 1 == s1 < s2 < s3 < s4 < s5 == 100

    assert creer_voteS(vc1, [cc1, cc2, cc3]) == [100, 51, 1]
    assert creer_voteS(vc2, [cc1, cc2, cc3]) == [51, 100, 51]
    
    assert creer_liste_voteS([vc1, vc2], [cc1, cc2, cc3]) == [[100, 51, 1], 
                                                                     [51, 100, 51]]
    


def test_maxSum () :
    assert maxSum([[100, 75, 50, 25],
                   [25, 100, 50, 75],
                   [50, 25, 100, 75]], [a, b, c, d]) == [b, [175, 200, 200, 175]]



def test_maxProd () :
    s1, s2, s3, s4, s5 = normalise2_vote([1, 25, 50, 75, 100])
    assert 1 == s1 < s2 < s3 < s4 < s5 == 2 

    ((s1, s2, s3, s4, s5), 
     (s6, s7, s8, s9, s10)) = normalise2_ForAll([[1, 12, 23, 34, 45], 
                                                 [56, 67, 78, 89, 100]])
    assert 1 == s1 < s2 < s3 < s4 < s5 < s6 < s7 < s8 < s9 < s10 == 2 

    assert produit([1, 2, 3, 4, 5]) == 120
    assert produit([1, 1.25, 1.50, 1.75, 2]) == 1*1.25*1.50*1.75*2

    result = maxProd([[100, 75, 50, 25],
                      [25, 100, 50, 75],
                      [50, 25, 100, 75]], [a, b, c, d])
    assert result[0] == c
    assert result[1][0] == ((100-1)/99 +1) * ((25-1)/99 +1) * ((50-1)/99 +1) #~ 3.71472
    assert result[1][1] == ((75-1)/99 +1) * ((100-1)/99 +1) * ((25-1)/99 +1) #~ 4.34221
    assert result[1][2] == ((50-1)/99 +1) * ((50-1)/99 +1) * ((100-1)/99 +1) #~ 4.46975
    assert result[1][3] == ((25-1)/99 +1) * ((75-1)/99 +1) * ((75-1)/99 +1)  #~ 3.79395


