#!/usr/bin/env python3

from random import shuffle as shuffle
class Carte:
    def __init__(self, valeur, couleur, is_atout=False, proprietaire = None):
        self.valeur = valeur
        self.couleur = couleur
        self.proprietaire = proprietaire
        self.is_atout = is_atout
    def __lt__(self, other):
        """supposée de la meme couleur"""
        if self.is_atout:
            if self.valeur == 11:
                return False
            elif self.valeur == 9:
                return other.valeur==11
            else:
                if other.valeur==9 or other.valeur==11:
                    return True
                else:
                    return self.valeur < other.valeur
        else:
            return (self.valeur < other.valeur)

    def __str__(self):
        if self.valeur in [7, 8, 9, 10]:
            nom = str(self.valeur)
        elif self.valeur == 11:
            nom = "valet"
        elif self.valeur == 12:
            nom ="dame"
        elif self.valeur == 13:
            nom="roi"
        elif self.valeur == 14:
            nom="as"
        return "{} de {}".format(nom, self.couleur)

def creer_deck():
    couleurs = ["carreau", "coeur", "pique", "trefle"]
    deck = []
    for couleur in couleurs:
        for k in range(7,15):
            deck.append(Carte(k, couleur))
    shuffle(deck)
    return deck
def valeur_pli(cartes, der = False):
    """
    cartes dans l'ordres ou posées
    """
    couleur_jouee = cartes[0].couleur
    valeurpli = 0
    if der:
        valeurpli += 10
    for carte in cartes:
        if carte.valeur == 10:
            valeurpli += 10
        elif carte.valeur == 14:
            valeurpli += 11
        elif carte.valeur == 12:
            valeurpli += 3
        elif carte.valeur == 13:
            valeurpli += 4
        elif carte.valeur == 11:
            if carte.is_atout:
                valeurpli += 20
            else:
                valeurpli += 2
        elif carte.valeur == 9:
            if carte.is_atout:
                valeurpli += 14
    return valeurpli
def vainqueur_pli(cartes, der = False):
    """
    cartes dans l'ordre où elles ont été posées
    """
    pt_pli = [0, 0]
    couleur_jouee = cartes[0].couleur
    atout_dans_le_pli = cartes[0].is_atout or cartes[1].is_atout or cartes[2].is_atout or cartes[3].is_atout
    if atout_dans_le_pli:
        cartevainqueur = max([carte for carte in cartes if carte.is_atout])
    else:
        cartevainqueur = max([carte for carte in cartes if carte.couleur==couleur_jouee])
    vainqueurpli = cartevainqueur.proprietaire
    if vainqueurpli in [0, 2]:
        pt_pli[0] = valeur_pli(cartes, der)
    else:
        pt_pli[1] = valeur_pli(cartes, der)
    return (vainqueurpli, pt_pli)

def debut_distrib(tas, mains, distributeur):
    given = (distributeur+1)%4
    for k in range(4):
        for i in range(3):
            carte = tas.pop()
            carte.proprietaire = given
            mains[given].append(carte)
        given = (given+1)%4
    for k in range(4):
        for i in range(2):
            carte = tas.pop()
            carte.proprietaire = given
            mains[given].append(carte)
        given = (given+1)%4
    return tas.pop()

def fin_distrib(tas, mains, preneur, tourne, distributeur, colortaken=None):
    given = (distributeur+1)%4
    if colortaken is None:
        colortaken = tourne.couleur
    for k in range(4):
        if k == preneur:
            tourne.proprietaire = preneur
            mains[k].append(tourne)
            for i in range(2):
                carte = tas.pop()
                carte.proprietaire = given
                mains[given].append(carte)
        else:
            for i in range(3):
                carte = tas.pop()
                carte.proprietaire = given
                mains[given].append(carte)
        given = (given+1)%4
    for hand in mains:
        for carte in hand:
            carte.is_atout= carte.couleur == colortaken

def jouer_donne(tas, mains, distributeur, points):
    joueur = (distributeur+1)%4
    point_tour = [0, 0]
    while len(tas)<32:
        pli = []
        for k in range(4):
            print("main du joueur ", joueur)
            for carte in mains[joueur]:
                print(carte)
            toplay= int(input("choisissez indice carte a jouer : "))
            cartetp = mains[joueur].pop(toplay)
            print("carte choisie  :", cartetp)
            pli.append(cartetp)
            tas.append(cartetp)
            joueur = (joueur + 1)%4
        print("le pli venant detre joue")
        for carte in pli:
            print(carte)
        (joueur, ptpli) = vainqueur_pli(pli, len(tas)==32)
        point_tour = [point_tour[0]+ptpli[0], point_tour[1]+ptpli[1]]
        print("vainqueur du pli et prochian joueur:", joueur, "pt du tour : ", point_tour)
    points[0]+=point_tour[0]
    points[1]+=point_tour[1]
    tas.reverse()

def jouer_12_donnes(tas):
    points = [0, 0]#equipe 0 et 2 avec 1 et 3
    distributeur = 3 #comme ca j0 commence a jouer
    for k in range(12):
        print("equipe 0 a ", points[0],"points")
        print("equipe 1 a ", points[1],"points")
        mains = [[] for _ in range(4)]
        to_be_taken = debut_distrib(tas, mains, distributeur)
        print("carte qui tourne ", to_be_taken)
        pris_1er_tour = False
        speak = (distributeur+1)%4
        for k in range(4):
            for carte in mains[speak]:
                print(carte)
            print("joueur ", speak, " tu prends ? (entre oui ou non)")
            rep = input()
            if rep == "oui":
                preneur = speak
                speak = (speak+1)%4
                pris_1er_tour = True
                colortaken = to_be_taken.couleur
                break
            speak = (speak+1)%4
        if not(pris_1er_tour):
            for k in range(4):
                for carte in mains[speak]:
                    print(carte)
                print("joueur ", speak, " tu prends ? (entre ta couleur ou non)")
                rep = input()
                if rep!="non":
                    preneur = speak
                    colortaken = rep
                    speak = (speak+1)%4
                    break
                speak = (speak+1)%4
        fin_distrib(tas, mains, preneur, to_be_taken, distributeur, colortaken)
        jouer_donne(tas, mains, distributeur, points)
        distributeur = (distributeur+1)%4


def main():
    tas = creer_deck()
    jouer_12_donnes(tas)

if __name__  == '__main__':
    main()
