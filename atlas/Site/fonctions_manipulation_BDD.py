import sqlite3
from module.election.ranking import *
from module.election.classe import *
from redirection_templates import *



"""FONCTIONS RECONSTITUTION OBJETS DEPUIS BDD"""

#retourne les objets Candidat à partir de la BDD
def bdd_obj_candidat():
    """Retourne les objets Candidats reconstitues depuis la BDD
    
    return: liste_candidats_obj, liste d'objets Candidat
    """
    database, cursor = open_bdd()
    candidats = cursor.execute('''SELECT * FROM CANDIDAT;''').fetchall()
    close_bdd(database, cursor)
    
    liste_candidats = []
    for c in candidats:
        #on creer les objets Candidat : nom, coordonnees, visibilite, sexe, age 
        liste_candidats.append(Candidat(c[1], (c[2], c[3]), c[4], c[5], c[6]))

    return liste_candidats

#retourne les objets Votant à partir de la BDD
def bdd_obj_votant():
    """Retourne les objets Votants reconstitués depuis la BDD 

    :return: liste_votants_obj, liste d'objets Votant
    """
    database, cursor = open_bdd()
    votants = cursor.execute('''SELECT * FROM Votant;''').fetchall()
    close_bdd(database, cursor)

    liste_votants = []
    for v in votants:
        #creation des objets Votant : coordonnees
        liste_votants.append(Votant((v[1], v[2])))

    return liste_votants

#retourne les objets VotantPoids à partir de la BDD
def bdd_obj_votantPoids():
    """Retourne les objets VotantPoids reconstitués depuis la BDD

    return: liste_votants_obj, liste d'objets VotantPoids
    """
    database, cursor = open_bdd()
    votantsP = cursor.execute('''SELECT * FROM PERSONNE;''').fetchall()
    close_bdd(database, cursor)

    liste_votantsP = []
    for v in votantsP:
        #creation des objets VotantPoids : coord, competence, delegation, poids 
        liste_votantsP.append(VotantPoids((v[1], v[2]), v[3], v[5], v[4]))

    return liste_votantsP

#reconstitue les objets avec la BDD 
def bdd_to_obj(liquide = False):
    """Retourne les objets Votants et Candidats reconstitués depuis la BDD 
    
    liquide: parametre indiquant s'il s'agit d'une democratie liquide, par defaut False
    :return: 
            :liste_candidats_obj, liste d'objets Candidat
            :liste_votants_obj, liste d'objets Votant (objets VotantPoids si liquide = True)
    """
    if liquide == False:
        return bdd_obj_candidat(), bdd_obj_votant() 
    return bdd_obj_candidat(), bdd_obj_votantPoids()


"""FONCTIONS INSERTION OBJETS"""

#fonction qui insere dans la BDD les objets Candidat et VotantPoids
def inserer_BDD_liquide(liste_votants, liste_candidats):
    """Insère dans la base de données les informations de Candidat et VotantPoids

    input:  liste_votants, une liste d'objets VotantPoids
            liste_candidats, une liste d'objets Candidat
    """

    database, cursor = open_bdd()

    #Insertion dans la BDD les objets Candidat
    cmd = "INSERT INTO CANDIDAT (X, Y, NOM, VISIBILITE, SEXE, AGE) VALUES (?, ?, ?, ?, ?, ?);"
    for c in liste_candidats:
        cursor.execute(cmd, (c.coord[0], c.coord[1], c.nom, c.visibilite, c.sexe, c.age))

    #Insertion dans la BDD les objets VotantPoids
    cmd = "INSERT INTO PERSONNE (X, Y, COMPETENCE, POIDS, DELEGATION) VALUES (?, ?, ?, ?, ?);"
    for v in liste_votants:
        cursor.execute(cmd, (v.coord[0], v.coord[1], v.competence ,v.poids, v.delegue))

    database.commit()

    close_bdd(database, cursor)

#fonction qui insere dans BDD les objets Candidat et Votant
def inserer_BDD(liste_votants, liste_candidats):
    """Insère dans la base de données les informations de Candidat et Votant

    input:  liste_votants: une liste d'objets VotantPoids
            liste_candidats: une liste d'objets Candidat
    """

    database, cursor = open_bdd()

    #Insertion dans la BDD les objets Candidat
    cmd = "INSERT INTO CANDIDAT (X, Y, NOM, VISIBILITE, SEXE, AGE) VALUES (?, ?, ?, ?, ?, ?);"
    for c in liste_candidats:
        cursor.execute(cmd, (c.coord[0], c.coord[1], c.nom, c.visibilite, c.sexe, c.age))

    #Insertion dans la BDD les objets Votant
    cmd = "INSERT INTO VOTANT (X, Y) VALUES (?, ?);"
    for v in liste_votants:
        cursor.execute(cmd, (v.coord[0], v.coord[1]))

    database.commit()

    close_bdd(database, cursor)


"""FONCTIONS MANIPULATION/INSERTION BDD"""

#ouverture BDD
def open_bdd():
    """Connecte la BDD et renvoie la database et le curseur
    
    return: database, l'objet BDD
            cursor, curseur sur la BDD permettant de manipuler la database"""
    
    database = sqlite3.connect('bdd.db')
    cursor = database.cursor()

    with open('bdd.sql', 'r') as sql_file:
        sql_script = sql_file.read()
        cursor.executescript(sql_script)
    
    return database, cursor

#fermeture BDD
def close_bdd(database, cursor):
    """Ferme la BDD
    
    input: database, l'objet BDD
            cursor, curseur sur la BDD permettant de manipuler la database"""
    
    database.close()
    cursor.close

#ajoute les candidats et les votants dans la BDD CAS MANUELLE ATTRIBUT EN PLUS (not used yet)
def ajout_dans_BDD(listex, listey, nb_c, candidats):
    """
    Ajoute les Candidats et les Votants dans la BDD dans le cas manuelle individuelle 
    
    input: 
        listex: la liste des coordonnées x des objets Candidat et Votant
        listey: la liste des coordonnées y des objets Candidat et Votant
        nb_c: nombre de candidats
        candidats: liste de dictionnaire d'attributs des candidats: nom, age, sexe, visibilite
    """
    #OUVERTURE BDD
    database, cursor = open_bdd()

    #-Insertion dans la BDD des données
    cmd = "INSERT INTO CANDIDAT (X, Y, NOM, VISIBILITE, SEXE, AGE) VALUES (?, ?, ?, ?, ?, ?);"
    for i in range(0, nb_c):
        cursor.execute(cmd, (listex[i], listey[i], candidats[i]['nom'], float(candidats[i]['visibilite']), candidats[i]['sexe'], int(candidats[i]['age'])))

    cmd = "INSERT INTO VOTANT (X, Y) VALUES (?, ?);"
    for i in range(nb_c, len(listex)):
        cursor.execute(cmd, (listex[i], listey[i]))

    database.commit()  
    close_bdd(database, cursor)


#récupère les données depuis la BDD nécessaire à HTML
def donnees_depuis_BDD(liquide = False, rayon = 0.0):
    """ Retourne une liste contenant les donnees que necessite la page HTML pour afficher les resultats des 
    elections individuelles

    input: 
        liquide: True s'il s'agit d'une democratie liquide, False par defaut
        rayon: float qui correspond a la distance de delegation pour la delegation liquide, par defaut 0.0
    return:
        liste_resultats : liste du gagnant sous forme (x, y, nom) pour chaque methode de vote (int, int, String) list
        liste_votant_candidats_xy : les positions x y des votants et des candidats [int list] * 4
        liste_resultats_votes : le nombre de vote recus pour chaque candidat (statistiques) int list list
        liste_candidat : liste du nom de tous les candidats String list
        liste_satisf : liste des satisfaction pour chaque candidats float list

    si liquide = True renvoie aussi 
        liste_poids: liste du poids de tous les votants int list
        liste_deleg: liste de booleen T/F indiquant si les votants ont délégué leur vote int list
    """

    #on récupère les objets et les votes
    liste_candidats, liste_votants = bdd_to_obj() if liquide == False else bdd_to_obj(True)
    liste_votes = creer_liste_voteR(liste_votants, liste_candidats) if liquide == False else creer_liste_votePoidsR(liste_votants, liste_candidats, rayon)
    
    liste_candidat_nom = liste_nom_candidats(liste_candidats)
    liste_satisf = satisf(liste_votants, liste_candidats)
    listexc, listeyc =  liste_coord_candidats(liste_candidats)        
    
    liste_resultats_votes, liste_resultats = resultats_vote(liste_votes, liste_candidats)

    if liquide == False:
        listexv, listeyv = liste_coord_votant(liste_votants)
        liste_votant_candidats_xy = [listexv, listeyv, listexc, listeyc]
        return [liste_votant_candidats_xy, liste_resultats, liste_resultats_votes, liste_candidat_nom, liste_satisf]
    
    # Cas delegation
    listexv, listeyv, liste_deleg, liste_poids = liste_attr_votantPoids(liste_votants)
    liste_votant_candidats_xy = [listexv, listeyv, listexc, listeyc]
    return [liste_votant_candidats_xy, liste_resultats, liste_resultats_votes, liste_candidat_nom, liste_poids, liste_deleg, liste_satisf]

#insere des candidats de base (not used yet)
def BDD_candidats_base():
    """Ajout dans la BDD des candidats prédéfinis"""

    database, cursor = open_bdd()
    cmd = "INSERT INTO CANDIDAT(NOM, X, Y, VISIBILITE, SEXE, AGE) VALUES('Emmental Macaron', 450, 250, 0.7, 'H', 35);"
    cursor.execute(cmd)
    cmd = "INSERT INTO CANDIDAT(NOM, X, Y, VISIBILITE, SEXE, AGE) VALUES('Marine Lapin', 250, 550, 0.65, 'F', 42);"
    cursor.execute(cmd)
    cmd = "INSERT INTO CANDIDAT(NOM, X, Y, VISIBILITE, SEXE, AGE) VALUES('Jean Peuplu', 450, 50, 0.1, 'H', 44);"
    cursor.execute(cmd)
    cmd = "INSERT INTO CANDIDAT(NOM, X, Y, VISIBILITE, SEXE, AGE) VALUES('Marinette Dupaincheng', 10, 590, 0.99, 'F', 14);"
    cursor.execute(cmd)
    cmd = "INSERT INTO CANDIDAT(NOM, X, Y, VISIBILITE, SEXE, AGE) VALUES('Harry Ko', 590, 500, 0.7, 'H', 70);"
    cursor.execute(cmd)
    cmd = "INSERT INTO CANDIDAT(NOM, X, Y, VISIBILITE, SEXE, AGE) VALUES('Taylor Shift', 300, 300, 0.7, 'F', 20);"
    cursor.execute(cmd)
    cmd = "INSERT INTO CANDIDAT(NOM, X, Y, VISIBILITE, SEXE, AGE) VALUES('Da Heil', 599, 1, 0.7, 'H', 0);"
    cursor.execute(cmd)
    #modifier autres values
    cmd = "INSERT INTO CANDIDAT(NOM, X, Y, VISIBILITE, SEXE, AGE) VALUES('Sasuke', 599, 1, 0.7, 'H', 0);"
    cursor.execute(cmd)
    cmd = "INSERT INTO CANDIDAT(NOM, X, Y, VISIBILITE, SEXE, AGE) VALUES('Amelia', 599, 1, 0.7, 'H', 0);"
    cursor.execute(cmd)
    cmd = "INSERT INTO CANDIDAT(NOM, X, Y, VISIBILITE, SEXE, AGE) VALUES('Chucky', 599, 1, 0.7, 'H', 0);"
    cursor.execute(cmd)
    cmd = "INSERT INTO CANDIDAT(NOM, X, Y, VISIBILITE, SEXE, AGE) VALUES('Mickey Mouse', 599, 1, 0.7, 'H', 0);"
    cursor.execute(cmd)
    cmd = "INSERT INTO CANDIDAT(NOM, X, Y, VISIBILITE, SEXE, AGE) VALUES('Tiri Giglio', 599, 1, 0.7, 'H', 0);"
    cursor.execute(cmd)
    database.commit()
    close_bdd(database, cursor)

#insere les candidats choisi par l'user (not used yet)
def insere_candidat_manuelle(nom, x, y, visibilite, sexe, age):
    """Permet d'insérer dans la BDD un candidat voulu

    input:
        nom: nom du candidat String
        x: coordonnee x du candidat int
        y: coordonnee y du candidat int
        visibilite: visibilite du candidat float
        sexe: sexe du candidat 'H' homme 'F' femme
        age: age du candidat int
    """

    database, cursor = open_bdd()
    cursor.execute(
        "INSERT INTO CANDIDATS (NOM, X, Y, VISIBILITE, SEXE, AGE) VALUES(:nom, :x, :y, :visibilite, :sexe, :age);",
        nom = nom,
        x = x,
        y = y,
        visibilite = visibilite,
        sexe = sexe,
        age = age 
    )
    close_bdd(database, cursor)

#fonction qui recupere les contraintes globales et individuelles depuis la BDD
def get_cont_BDD():
    """Renvoie les contraintes depuis la BDD
    return: liste_contr_indiv, la liste des contraintes individuelles
            liste_cont_glob, la liste des contraintes globales
    """

    database, cursor = open_bdd()
    liste_cont_indiv = cursor.execute("SELECT * FROM CONTRAINTES_INVIDIVIDUELLES").fetchall()
    liste_cont_glob = cursor.execute("SELECT * FROM CONTRAINTES_GLOBALES").fetchall()
    
    close_bdd(database, cursor)

    #on modifie les contraintes de la BDD sous forme voulue
    liste_cont_indiv, liste_cont_glob = cont_bdd_lst(liste_cont_indiv, liste_cont_glob)

    return liste_cont_indiv, liste_cont_glob

#Verifie si la BDD est vide
def estVideBDD():
    """Renvoie si BDD est vide 
    return: boolean, True si la BDD est vide sinon False"""

    database, cursor = open_bdd()
    est_vide = True if cursor.execute('''SELECT COUNT(*) FROM CANDIDAT;''').fetchall()[0][0] == 0 else False
    close_bdd(database, cursor)
    return est_vide

#fonction qui insere dans la bdd les contraintes individuelles
def save_cont_BDD(liste_cont_indiv, liste_cont_glob):
    """ sauvegarde dans la BDD les contraintes
    Input:  liste_cont_indiv: une liste de contraintes individuelles
            liste_cont_glob: une liste de contraintes globales"""

    database, cursor = open_bdd()
    
    #Insertion des contraintes individuelles
    cmd = "INSERT INTO CONTRAINTES_INVIDIVIDUELLES (NOM_MIN, NOM_MAX, X_MIN, X_MAX, Y_MIN, Y_MAX, VISIBILITE_MIN, VISIBILITE_MAX, SEXE, AGE_MIN, AGE_MAX) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
    for contr_i in liste_cont_indiv:
        #si aucune contrainte sur le sexe
        if contr_i[4] == []:
            contr_i[4] = ['N'] #pour None
        cursor.execute(cmd, (contr_i[0][0], contr_i[0][1],contr_i[1][0], contr_i[1][1], contr_i[2][0], contr_i[2][1], contr_i[3][0], contr_i[3][1], contr_i[4][0], contr_i[5][0], contr_i[5][1] ))

    #S'il n'y a aucune contrainte globale, on en cree une
    if cursor.execute("SELECT COUNT(*) FROM CONTRAINTES_GLOBALES").fetchall()[0][0] == 0:
        cursor.execute("INSERT INTO CONTRAINTES_GLOBALES(ID, PARITE_F, PARITE_H, DISTANCE_MIN, DISTANCE_MIN) VALUES (1, NULL, NULL, NULL, NULL);")

    #Si il y a une contrainte globale on la modifie 
    if liste_cont_glob[0] != []:
        #On ajoute la contrainte de la parite H/F
        cmd = "UPDATE CONTRAINTES_GLOBALES SET (PARITE_F, PARITE_H) = (?, ?) WHERE ID = 1;"
        cursor.execute(cmd, (liste_cont_glob[0][0], liste_cont_glob[0][1]))

    if liste_cont_glob[1] != []:
        #On ajoute les contraintes de la distance entre les candidats
        cmd = "UPDATE CONTRAINTES_GLOBALES SET (DISTANCE_MIN, DISTANCE_MAX) = (?, ?) WHERE ID = 1;"
        cursor.execute(cmd, (liste_cont_glob[1][0], liste_cont_glob[1][1]))
        
    database.commit()

    close_bdd(database, cursor)

#Supprime toutes les donnees de la BDD
def empty_bdd():
    """Vide tous les tables de la BDD"""

    database, cursor = open_bdd()
    cursor.execute('DROP TABLE CANDIDAT;')
    cursor.execute(' DROP TABLE PERSONNE;')
    cursor.execute('DROP TABLE CONTRAINTES_INVIDIVIDUELLES;')
    cursor.execute('DROP TABLE CONTRAINTES_GLOBALES;')
    cursor.execute('DROP TABLE VOTANT;')
    database.commit()
    close_bdd(database, cursor)

#Supprime les contraintes globales et individuelles de la BDD
def empty_bdd_cont():
    """Vide les tables de contraintes de la BDD (CONTRAINTES_INVIDIVIDUELLES et CONTRAINTES_GLOBALES)"""

    database, cursor = open_bdd()
    cursor.execute('DROP TABLE CONTRAINTES_INVIDIVIDUELLES;')
    cursor.execute('DROP TABLE CONTRAINTES_GLOBALES;')
    database.commit()
    close_bdd(database, cursor)

"""FONCTIONS CREATION DE LISTES"""

# creer liste votants et candidats version liquide
def creer_liste_vc_liq(nb_elec, nb_cand):
   """Retourne la liste aléatoire de Candidat et de VotantPoids pour la delegation 
   
   input:
    nb_elec: int, le nombre d'electeurs
    nb_cand: int, le nombre de candidats
   return: obj VotantPoids list, obj Canditat list"""

   return creer_liste_votantPoids(nb_elec), creer_liste_candidat(nb_cand)
    
#creer liste votants et candidats version normal
def creer_liste_vc(nb_elec, nb_cand):
    """Retourne la liste aléatoire de Candidat et de Votant 
    
    input:
        nb_elec: int, le nombre d'electeurs
        nb_cand: int, le nombre de candidats
    return: obj Votant list, obj Canditat list"""
    return creer_liste_votant(nb_elec), creer_liste_candidat(nb_cand)


"""FONCTIONS INTERMEDIAIRES (RETRIEVE LISTS)"""

#recupere tous les attributs des objets Candidat
def liste_att_candidats(liste_candidats):
    """Renvoie les attributs de tous les candidats [nom, x, y, visibilite, sexe, age]
    
    input:
        liste_candidats: la liste des objets Candidat
    return: [nom, x, y, visibilite, sexe, age] list"""
    return [[e.nom, e.coord[0], e.coord[1], e.visibilite, e.sexe, e.age] for e in liste_candidats]
    
#recupere le nom de tous les objets Candidat
def liste_nom_candidats(liste_candidats):
    """Renvoie le nom de tous les candidats

    input: 
        liste_candidats: la liste des objets Candidat
    return: String list"""

    liste_candidat_nom = []
    for e in liste_candidats: #passage object à string
        liste_candidat_nom.append(e.nom)
    return liste_candidat_nom

#recupere les coordonnees de tous les objets Candidat
def liste_coord_candidats(liste_candidats):
    """Renvoie les coordonnées x y des candidats: x, y

    input: 
        liste_candidats: la liste des objets Candidat
    return: int list, int list"""
    listexc, listeyc = [], []
    for c in liste_candidats:
        listexc.append(c.coord[0])
        listeyc.append(c.coord[1])
    return listexc, listeyc

#recupere les attributs de tous les objets VotantPoids
def liste_attr_votantPoids(liste_votants):
    """Renvoie la liste des attributs des votantPoids: x, y, delegation, poids

    input: 
        liste_votants: la liste des objets Votant
    return: int list * 4 """

    listexv, listeyv = [], []
    liste_deleg = []
    liste_poids = []
    liste_competence = []

    for v in liste_votants:
        listexv.append(v.coord[0])
        listeyv.append(v.coord[1])
        liste_deleg.append(v.delegue) 
        liste_poids.append(v.poids)
        liste_competence.append(v.competence)

    return listexv, listeyv, liste_deleg, liste_poids

#recupere les coord de tous les objets Votants
def liste_coord_votant(liste_votants):
    """Recupere les coordonees x y des votants: x, y

    input: 
        liste_votants: la liste des objets Votant
    return: int list, int list
    """
    listexv, listeyv = [], []
    for v in liste_votants:
        listexv.append(v.coord[0])
        listeyv.append(v.coord[1])
    return listexv, listeyv

#prend une liste d'objet Candidat et la renvoie sous la forme d'une liste d'attributs pour comite
def lst_obj_to_lst_str(liste_comite):
    """Liste comite: contient des listes de comites, un comite etant un ensemble d'objets Candidat
    
    input:  
        liste_comite: une liste de comite (un comite etant une ensemble d'objets Candidat)
    return: Renvoie la meme liste de comites avec les objets Candidats remplaces par une liste d'attributs"""

    return [[ [e.nom, e.coord[0], e.coord[1], e.visibilite, e.sexe, e.age] for e in comit ] if comit != None else [] for comit in liste_comite]

#modifie la forme des contraintes globales et individuelles
def ordre_contraintes(liste_contraints_indiv, liste_contraints_glob):
    """Ordonne la liste des contraintes individuelles de forme [nom, age, x, y, visibilite, sexe] 
    sous forme [nom, x, y, visibilite, sexe, age], cast les nombres str en float/int et modifie les
    cntraintes globales pour qu'elles soient utilisables par les fonctions python

    input: 
        liste_contraints_indiv: liste des contraintes individuelles
        liste_contraints_glob: liste des contraintes globales
    return: [nom, x, y, visibilite, sexe, age] list, [[pariteF, pariteH], [distMin, distMax]] """

    #On convertie les str en float pour les contraintes globales
    liste_contraints_glob = [[float(el) for el in cont] for cont in liste_contraints_glob]
    
    #On ordonne les attributs individuelles dans un ordre
    [candidat_i.append(candidat_i.pop(1)) for candidat_i in liste_contraints_indiv]

    #Transformation pour la contrainte individuelle sur le sexe ['both'] -> []
    liste_contraints_indiv = [[[] if att == ['both'] else att for att in candidat_i] for candidat_i in liste_contraints_indiv] 

    #On convertie les attributs des contraintes individuells
    liste_contraints_indiv = [ [candidat_i[0],[int(x) for x in candidat_i[1]], [int(x) for x in candidat_i[2]], [float(x) for x in candidat_i[3]],  candidat_i[4], [int(x) for x in candidat_i[5]]] for candidat_i in liste_contraints_indiv]

    return liste_contraints_indiv, liste_contraints_glob

#transforme les donnees tuple de BDD en listes
def cont_bdd_lst(liste_contrainte_indiv, liste_contrainte_glob):
    """Transforme liste_contrainte_indiv et liste_contrainte_glob qui contient des tuples (contraintes depuis BDD) en liste de contraintes
    
    input: 
        liste_contraints_indiv: liste des contraintes individuelles
        liste_contraints_glob: liste des contraintes globales
    return:
        liste_contraints_indiv: liste des contraintes individuelles
        liste_contraints_glob: liste des contraintes globales
    """

    #On transforme les contraintes individuelles
    liste_contrainte_indiv = [[[cont[1], cont[2]], [cont[3], cont[4]], [cont[5], cont[6]], [cont[7], cont[8]], cont[9], [cont[10], cont[11]] ] for cont in liste_contrainte_indiv]

    #On transforme les contraintes globales    
    liste_contrainte_glob = [ [[e[1], e[2]], [e[3], e[4]]] for e in liste_contrainte_glob]
    liste_contrainte_glob = [[e if e!= [None, None] else [] for e in cont] for cont in liste_contrainte_glob][0] #car dans une liste

    return liste_contrainte_indiv,liste_contrainte_glob

"""FONCTION RESULTATS DE METHODES DE VOTE"""

#renvoie les résultats des votes et positions des candidats gagnants pour individuel
def resultats_vote(liste_votes, liste_candidats):
    """Retourne 2 listes, le nombre de votes pour chaque candidat en fonction de la méthode de vote, et le gagnant pour chaque méthode de vote
    Ordre des methodes de votes: [veto, stv, condorcet, pluralité, borda, copeland, simpson]

    input:
        liste_votes: la liste de vote obtenue avec les votants, un vote etant une liste d'objets Candidat
        liste_candidats: la liste d'objets Candidat

    return:
        int list list, la liste du nombre de vote par candidat pour chaque methode de vote
        liste_resultats, la liste des gagnants pour chaque methodes de vote (int, int, String) list """

    fonction_veto = veto(liste_votes, liste_candidats)
    fonction_stv = stv(liste_votes, liste_candidats) 
    fonction_condorcet = condorcet(liste_votes, liste_candidats)
    fonction_pluralite = pluralite(liste_votes, liste_candidats)
    fonction_borda = borda(liste_votes, liste_candidats)
    fonction_copeland = copeland(liste_votes, liste_candidats)
    fonction_simpson = simpson(liste_votes, liste_candidats)
    
    #on recupere le nom des candidats pour la liste des eliminations successives 
    tmp_stv = []
    for e in fonction_stv[2]:
        tmp_stv.append(e.nom) 
    
    liste_resultats = []

    #liste_resultats = [veto, stv, condorcet, pluralité, borda, copeland, simpson] sous forme (X, Y, NOM)
    liste_resultats.append((fonction_veto[0].coord[0], fonction_veto[0].coord[1], fonction_veto[0].nom))
    liste_resultats.append((fonction_stv[0].coord[0], fonction_stv[0].coord[1], fonction_stv[0].nom))
    #Cas condorcet renvoie None car aucun gagnant
    if (fonction_condorcet[0]) == None:
        liste_resultats.append('None')
    else:
        liste_resultats.append((fonction_condorcet[0].coord[0], fonction_condorcet[0].coord[1], fonction_condorcet[0].nom))
    liste_resultats.append((fonction_pluralite[0].coord[0], fonction_pluralite[0].coord[1], fonction_pluralite[0].nom))  
    liste_resultats.append((fonction_borda[0].coord[0], fonction_borda[0].coord[1], fonction_borda[0].nom))  
    liste_resultats.append((fonction_copeland[0].coord[0], fonction_copeland[0].coord[1], fonction_copeland[0].nom))  
    liste_resultats.append((fonction_simpson[0].coord[0], fonction_simpson[0].coord[1], fonction_simpson[0].nom))  

    #liste_resultats_votes = [veto, stv, condorcet, pluralité, borda, copeland, simpson] sous forme [n1, n2 ... ] nb de vote pour chaque candidat
    return [fonction_veto[1], tmp_stv, fonction_condorcet[1], fonction_pluralite[1],fonction_borda[1],fonction_copeland[1], fonction_simpson[1]], liste_resultats

#renvoie comites gagnants pour chaque methode de votes
def resultats_vote_comite(liste_votants, liste_candidats):
    """Retourne la liste des 3 premiers comités gagnant pour chaque methodes de votes 
    dans l'ordre [veto, stv, condorcet, pluralité, borda, copeland, simpson]

    input:
        liste_votants, la liste des objets Votant
        liste_candidats, la liste de sobjets Candidats
    return:
        Candidats_att list list list, l'ensemble de comite avec un comite un ensemble de candidat sous leur forme d'attributs"""

    #On recupere les variables
    mes_contr_indiv, mes_contr_glob = get_cont_BDD()    
    liste_votes = creer_liste_voteR(liste_votants, liste_candidats)    
    
    #On recupere la liste des comites gagnants pour chaque methodes de vote de la bonne forme
    liste_comite_veto = lst_obj_to_lst_str(election_comite(3, len(mes_contr_indiv), liste_candidats, veto(liste_votes, liste_candidats)[1], mes_contr_glob, mes_contr_indiv))
    liste_comite_stv = lst_obj_to_lst_str(election_comite(3, len(mes_contr_indiv), liste_candidats, stv(liste_votes, liste_candidats)[1], mes_contr_glob, mes_contr_indiv))
    liste_comite_condorcet = lst_obj_to_lst_str(election_comite(3, len(mes_contr_indiv), liste_candidats, condorcet(liste_votes, liste_candidats)[1], mes_contr_glob, mes_contr_indiv))
    liste_comite_plura = lst_obj_to_lst_str(election_comite(3, len(mes_contr_indiv), liste_candidats, pluralite(liste_votes, liste_candidats)[1], mes_contr_glob, mes_contr_indiv))
    liste_comite_borda = lst_obj_to_lst_str(election_comite(3, len(mes_contr_indiv), liste_candidats, borda(liste_votes, liste_candidats)[1], mes_contr_glob, mes_contr_indiv))
    liste_comite_copeland = lst_obj_to_lst_str(election_comite(3, len(mes_contr_indiv), liste_candidats, copeland(liste_votes, liste_candidats)[1], mes_contr_glob, mes_contr_indiv))
    liste_comite_simpson = lst_obj_to_lst_str(election_comite(3, len(mes_contr_indiv), liste_candidats, simpson(liste_votes, liste_candidats)[1], mes_contr_glob, mes_contr_indiv))

    #[veto, stv, condorcet, pluralité, borda, copeland, simpson] sous forme ensemble de comites
    return [liste_comite_veto,liste_comite_stv,liste_comite_condorcet, liste_comite_plura, liste_comite_borda, liste_comite_copeland, liste_comite_simpson]

"""FONCTION AFFICHE RESULTATS"""

#fonction pour manuelle
def placement_manuelle(nb_cand, nb_elec):
    """template placement_manu.html
    
    input:
        nb_cand: le nombre de candidats int
        nb_elec: le nombre d'electeurs int
    """
    return template_manuelle(nb_cand, nb_elec)

#fonction pour election comite [resultats]
def affiche_comite_res(nb_cand, nb_elec):
    """Affiche le resultat de l'election comite : redirige vers affiche_comite.html
    input:
        nb_cand: le nombre de candidats int
        nb_elec: le nombre d'electeurs int"""
    
    #On verifie si la page a ete rechargee
    refresh = not(estVideBDD()) #Si la BDD n'est pas vide, alors la page a ete rechargee

    #Cas non refresh
    if refresh == False:
        #Creation aléatoire et sauvegarde des votants et des candidats
        liste_votants, liste_candidats = creer_liste_vc(nb_elec, nb_cand)
        inserer_BDD(liste_votants, liste_candidats)
    else:
        liste_candidats, liste_votants = bdd_to_obj()   #on recupere nos candidats et nos votants dans la BDD

    #On recupere les resultats et les donnees pour la page HTML
    res_comites_mdte = resultats_vote_comite(liste_votants, liste_candidats) 
    listexv, listeyv = liste_coord_votant(liste_votants)
    liste_all_candi = liste_att_candidats(liste_candidats)
    list_cont_indiv, list_cont_glob = get_cont_BDD()
    liste_satisf = satisf(liste_votants, liste_candidats)
    
    return template_affiche_comite(listexv, listeyv, res_comites_mdte, liste_all_candi, list_cont_indiv, list_cont_glob, liste_satisf)


#fonction pour délégation liquide (auto) [resultats]
def liquide(nb_cand, nb_elec, rayon_range):
    """Affiche le resultat de l'election individuel liquide : redirige vers liquide.html
    
    input:
        nb_cand: le nombre de candidats int
        nb_elec: le nombre d'electeurs int
        rayon_range: le rayon de delegation, float"""
    
    #On verifie si la page a ete rechargee
    refresh = not(estVideBDD()) #Si la BDD n'est pas vide, alors la page a ete rechargee

    #Cas non refresh
    if refresh == False:
        #Création aléatoire et sauvegarde des votants et des candidats (pas de manuelle pour la délégation liquide)
        liste_votants, liste_candidats = creer_liste_vc_liq(nb_elec, nb_cand)
        inserer_BDD_liquide(liste_votants, liste_candidats)

    #On recupere les resultats et les donnees pour la page HTML
    liste_votant_candidats_xy, liste_resultats, liste_resultats_votes, liste_candidat, liste_poids, liste_deleg, liste_satisf = donnees_depuis_BDD(True, rayon_range)   
    return template_liquide(liste_resultats, liste_votant_candidats_xy, liste_resultats_votes, liste_candidat, liste_poids, liste_deleg, liste_satisf = liste_satisf)

#fonction pour résultats individuel automatique
def individuel_auto(nb_cand, nb_elec):
    """Affiche le resultat de l'election individuel : redirige vers affiche_election.html
    
    input:
        nb_cand: le nombre de candidats int
        nb_elec: le nombre d'electeurs int"""         
    
    #On verifie si la page a ete rechargee
    refresh = not(estVideBDD()) #Si la BDD n'est pas vide, alors la page a ete rechargee

    #Cas non refresh
    if refresh == False:
        #Création aléatoire et sauvegarde des votants et des candidats
        liste_votants, liste_candidats = creer_liste_vc(nb_elec, nb_cand)
        inserer_BDD(liste_votants, liste_candidats)

    #On recupere les resultats et les donnees pour la page HTML
    liste_votant_candidats_xy, liste_resultats, liste_resultats_votes, liste_candidat, liste_satisf = donnees_depuis_BDD()
    return template_affiche_election(liste_resultats, liste_votant_candidats_xy, liste_resultats_votes, liste_candidat, liste_satisf=liste_satisf)

