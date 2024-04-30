from election import *



liste_candidat1 = creer_liste_candidat(7)
liste_candidat2 = creer_liste_candidat(10)
liste_candidat3 = creer_liste_candidat(13)
liste_candidat4 = creer_liste_candidat(16)
liste_candidat5 = creer_liste_candidat(20)

liste_votant = creer_liste_votant(150)
liste_votantPoids = creer_liste_votantPoids(150)

liste_vote1 = creer_liste_voteR(liste_votant, liste_candidat1)
liste_vote2 = creer_liste_votePoidsR(liste_votantPoids, liste_candidat2, 50)
liste_vote3 = creer_liste_votePoidsR(liste_votantPoids, liste_candidat3, 100)
liste_vote4 = creer_liste_votePoidsR(liste_votantPoids, liste_candidat4, 150)
liste_vote5 = creer_liste_votePoidsR(liste_votantPoids, liste_candidat5, 200)

satisfaction1 = satisf(liste_votant, liste_candidat1)
satisfaction2 = satisf(liste_votantPoids, liste_candidat2)
satisfaction3 = satisf(liste_votantPoids, liste_candidat3)
satisfaction4 = satisf(liste_votantPoids, liste_candidat4)
satisfaction5 = satisf(liste_votantPoids, liste_candidat5)



score_Pluralite1 = pluralite(liste_vote1, liste_candidat1)[1]
score_Pluralite2 = pluralite(liste_vote2, liste_candidat2)[1]
score_Pluralite3 = pluralite(liste_vote3, liste_candidat3)[1]
score_Pluralite4 = pluralite(liste_vote4, liste_candidat4)[1]
score_Pluralite5 = pluralite(liste_vote5, liste_candidat5)[1]

score_Veto1 = veto(liste_vote1, liste_candidat1)[1]
score_Veto2 = veto(liste_vote2, liste_candidat2)[1]
score_Veto3 = veto(liste_vote3, liste_candidat3)[1]
score_Veto4 = veto(liste_vote4, liste_candidat4)[1]
score_Veto5 = veto(liste_vote5, liste_candidat5)[1]

score_Borda1 = borda(liste_vote1, liste_candidat1)[1]
score_Borda2 = borda(liste_vote2, liste_candidat2)[1]
score_Borda3 = borda(liste_vote3, liste_candidat3)[1]
score_Borda4 = borda(liste_vote4, liste_candidat4)[1]
score_Borda5 = borda(liste_vote5, liste_candidat5)[1]

score_Stv1 = stv(liste_vote1, liste_candidat1)[1]
score_Stv2 = stv(liste_vote2, liste_candidat2)[1]
score_Stv3 = stv(liste_vote3, liste_candidat3)[1]
score_Stv4 = stv(liste_vote4, liste_candidat4)[1]
score_Stv5 = stv(liste_vote5, liste_candidat5)[1]

score_Condorcet1 = condorcet(liste_vote1, liste_candidat1)[1]
score_Condorcet2 = condorcet(liste_vote2, liste_candidat2)[1]
score_Condorcet3 = condorcet(liste_vote3, liste_candidat3)[1]
score_Condorcet4 = condorcet(liste_vote4, liste_candidat4)[1]
score_Condorcet5 = condorcet(liste_vote5, liste_candidat5)[1]

score_Copeland1 = copeland(liste_vote1, liste_candidat1)[1]
score_Copeland2 = copeland(liste_vote2, liste_candidat2)[1]
score_Copeland3 = copeland(liste_vote3, liste_candidat3)[1]
score_Copeland4 = copeland(liste_vote4, liste_candidat4)[1]
score_Copeland5 = copeland(liste_vote5, liste_candidat5)[1]

score_Simpson1 = simpson(liste_vote1, liste_candidat1)[1]
score_Simpson2 = simpson(liste_vote2, liste_candidat2)[1]
score_Simpson3 = simpson(liste_vote3, liste_candidat3)[1]
score_Simpson4 = simpson(liste_vote4, liste_candidat4)[1]
score_Simpson5 = simpson(liste_vote5, liste_candidat5)[1]



liste_global1 = [[0.25, 0.75], []]
matrice_indiv1 = [[[], [], [], [], [], []],
                  [[], [], [], [], [], []],
                  [[], [], [], [], [], []]]

liste_global2 = [[0.5, 0.5], []]
matrice_indiv2 = [[[], [None, 300], [], [], [], []],
                  [[], []         , [], [], [], []],
                  [[], []         , [], [], [], []]]

liste_global3 = [[0.25, 0.75], []]
matrice_indiv3 = [[[], [None, 300], []         , [], [], []],
                  [[], []         , [300, None], [], [], []],
                  [[], []         , []         , [], [], []]]

liste_global4 = [[], [100, None]]
matrice_indiv4 = [[[], [], [], [], [], []],
                  [[], [], [], [], [], []],
                  [[], [], [], [], [], []]]

liste_global5 = [[], [125, None]]
matrice_indiv5 = [[[], [], [], [], ['F'], [0, 30]],
                  [[], [], [], [], []   , []     ],
                  [[], [], [], [], []   , []     ]]

liste_global6 = [[], [150, None]]
matrice_indiv6 = [[[], [], [], [], ['F'], [0, 30] ],
                  [[], [], [], [], ['H'], [30, 60]],
                  [[], [], [], [], []   , []      ]]

liste_global7 = [[0.25, 0.75], [150, None]]
matrice_indiv7 = [[[], [None, 300], []         , [], ['F'], [0, 30] ],
                  [[], []         , [300, None], [], ['H'], [30, 60]],
                  [[], []         , []         , [], []   , []      ]]

e1 = election_comite(3, 3, liste_candidat1, score_Pluralite1, liste_global1, matrice_indiv1)
e2 = election_comite(3, 3, liste_candidat2, score_Veto2, liste_global2, matrice_indiv2)
e3 = election_comite(3, 3, liste_candidat3, score_Borda3, liste_global3, matrice_indiv3)
e4 = election_comite(3, 3, liste_candidat4, score_Stv4, liste_global4, matrice_indiv4)
e5 = election_comite(3, 3, liste_candidat5, score_Condorcet5, liste_global5, matrice_indiv5)
e6 = election_comite(3, 3, liste_candidat5, score_Copeland5, liste_global6, matrice_indiv6)
e7 = election_comite(3, 3, liste_candidat5, score_Simpson5, liste_global7, matrice_indiv7)



print("Liste candidat 1 :")
for candidat in ranking.comiteR.aff_CollecC(liste_candidat1) :
    print(candidat)
print()

print("Liste candidat 2 :")
for candidat in ranking.comiteR.aff_CollecC(liste_candidat2) :
    print(candidat)
print()

print("Liste candidat 3 :")
for candidat in ranking.comiteR.aff_CollecC(liste_candidat3) :
    print(candidat)
print()

print("Liste candidat 4 :")
for candidat in ranking.comiteR.aff_CollecC(liste_candidat4) :
    print(candidat)
print()

print("Liste candidat 5 :")
for candidat in ranking.comiteR.aff_CollecC(liste_candidat5) :
    print(candidat)
print()



print("Satisfaction 1 :")
print(satisfaction1)
print()

print("Satisfaction 2 :")
print(satisfaction2)
print()

print("Satisfaction 3 :")
print(satisfaction3)
print()

print("Satisfaction 4 :")
print(satisfaction4)
print()

print("Satisfaction 5 :")
print(satisfaction5)
print()



print("Score Pluralité 1 :")
print(score_Pluralite1)
print()

print("Score Pluralité 2 :")
print(score_Pluralite2)
print()

print("Score Pluralité 3 :")
print(score_Pluralite3)
print()

print("Score Pluralité 4 :")
print(score_Pluralite4)
print()

print("Score Pluralité 5 :")
print(score_Pluralite5)
print()



print("Score Veto 1 :")
print(score_Veto1)
print()

print("Score Veto 2 :")
print(score_Veto2)
print()

print("Score Veto 3 :")
print(score_Veto3)
print()

print("Score Veto 4 :")
print(score_Veto4)
print()

print("Score Veto 5 :")
print(score_Veto5)
print()



print("Score Borda 1 :")
print(score_Borda1)
print()

print("Score Borda 2 :")
print(score_Borda2)
print()

print("Score Borda 3 :")
print(score_Borda3)
print()

print("Score Borda 4 :")
print(score_Borda4)
print()

print("Score Borda 5 :")
print(score_Borda5)
print()



print("Score Stv 1 :")
print(score_Stv1)
print()

print("Score Stv 2 :")
print(score_Stv2)
print()

print("Score Stv 3 :")
print(score_Stv3)
print()

print("Score Stv 4 :")
print(score_Stv4)
print()

print("Score Stv 5 :")
print(score_Stv5)
print()



print("Score Condorcet 1 :")
print(score_Condorcet1)
print()

print("Score Condorcet 2 :")
print(score_Condorcet2)
print()

print("Score Condorcet 3 :")
print(score_Condorcet3)
print()

print("Score Condorcet 4 :")
print(score_Condorcet4)
print()

print("Score Condorcet 5 :")
print(score_Condorcet5)
print()



print("Score Copeland 1 :")
print(score_Copeland1)
print()

print("Score Copeland 2 :")
print(score_Copeland2)
print()

print("Score Copeland 3 :")
print(score_Copeland3)
print()

print("Score Copeland 4 :")
print(score_Copeland4)
print()

print("Score Copeland 5 :")
print(score_Copeland5)
print()




print("Score Simpson 1 :")
print(score_Simpson1)
print()

print("Score Simpson 2 :")
print(score_Simpson2)
print()

print("Score Simpson 3 :")
print(score_Simpson3)
print()

print("Score Simpson 4 :")
print(score_Simpson4)
print()

print("Score Simpson 5 :")
print(score_Simpson5)
print()



print("Classement 1 :")
for comite in ranking.comiteR.aff_Collec2C(e1) :
    print(comite)
print()

print("Classement 2 :")
for comite in ranking.comiteR.aff_Collec2C(e2) :
    print(comite)
print()

print("Classement 3 :")
for comite in ranking.comiteR.aff_Collec2C(e3) :
    print(comite)
print()

print("Classement 4 :")
for comite in ranking.comiteR.aff_Collec2C(e4) :
    print(comite)
print()

print("Classement 5 :")
for comite in ranking.comiteR.aff_Collec2C(e5) :
    print(comite)
print()

print("Classement 6 :")
for comite in ranking.comiteR.aff_Collec2C(e6) :
    print(comite)
print()

print("Classement 7 :")
for comite in ranking.comiteR.aff_Collec2C(e7) :
    print(comite)
print()
