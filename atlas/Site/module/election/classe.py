#CLASSES

class Candidat () :
    def __init__ (self, nom, coord, visibilite=None, sexe=None, age=None) :
        """
        nom : String
        coord : (int * int) ([COORD_MIN, COORD_MAX], [COORD_MIN, COORD_MAX])
        visibilité : float [0, 1]
        sexe : String {'H', 'F'}
        age : int [0, +inf[
        """
        self.nom = nom 
        self.coord = coord
        self.visibilite = visibilite 
        self.sexe = sexe 
        self.age = age 
    
    def aff (self, *attributes) : #Renvoie un affichage selon les attributs sélectionés
        dico = vars(self)
        if not attributes : #Si aucun attribut sélectionné
            return str(list(dico.values())) #Renvoyer l'affichage de tous les attributs
        return str([dico[attribute] for attribute in attributes if attribute in dico]) #Renvoyer l'affichage des attributs sélectionnés

    def setNom (self, nom) : #Setter du nom du candidat
        self.nom = nom 

    def setCoord (self, coord) : #Setter des coordonées du candidat
        self.coord = coord

    def setVisibilite (self, visibilite) : #Setter du taux de visibilité du candidat
        self.visibilite = visibilite

    def setSexe (self, sexe) : #Setter du sexe du candidat
        self.visibilite = sexe

    def setAge (self, age) : #Setter de l'âge du candidat
        self.age = age



class Votant () :
    def __init__ (self, coord) :
        """
        coord : (int * int) ([COORD_MIN, COORD_MAX], [COORD_MIN, COORD_MAX])
        """
        self.coord = coord
    
    def aff (self) : #Affiche les coordonées du votant
        return str(list(vars(self).values()))

    def setCoord (self, coord) : #Setter des coordonées du votant
        self.coord = coord



class VotantPoids (Votant) :
    def __init__ (self, coord, competence, delegue=False, poids=1) :
        """
        coord : (int * int) ([COORD_MIN, COORD_MAX], [COORD_MIN, COORD_MAX])
        competence : float [0, 1]
        delegue : bool
        poids : int
        """
        super().__init__(coord)
        self.competence = competence
        self.delegue = delegue 
        self.poids = poids

    def setCompetence (self, competence) : #Setter du taux de compétence du votantPoids
        self.competence = competence

    def setDelegue (self) : #Setter de la délégation du votantPoids
        self.delegue = not self.delegue 

    def setPoids (self, poids) : #Setter du poids du votantPoids
        self.poids += poids

    def delegation (self, votantPoids) : #Méthode de déléguation avec un autre votantPoids
        if self != votantPoids and not self.delegue : #Un votantPoids ne peut pas déléguer son vote à lui même et ne peut pas déléguer son vote s'il a déjà été délégué
            self.setDelegue() #Le votantPoids délègue son vote
            votantPoids.setPoids(self.poids) #Addition le poids du votantPoids délégué au poids du votantPoids qui délègue
            self.setPoids(-self.poids) #Le votant poids qui délègue à désormais un poids nul



#EXCEPTIONS



class AucunVote (Exception) :
    def __init__ (self) :
        pass
    def __str__ (self) :
        return "Il n'y a aucun vote."

class VoteInvalide (Exception) :
    def __init__ (self, liste) :
        self.liste = liste
    def __str__ (self) : 
        return "Le vote {0} est invalide.".format(self.liste)

class AucunCandidat (Exception) :
    def __init__ (self) :
        pass
    def __str__ (self) :
        return "Il n'y a aucun candidat."


