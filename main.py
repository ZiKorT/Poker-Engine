from poker_engine import *

J = 3

def get_card(texte, cartes_exclues):
    """
    Demande à l'utilisateur de saisir une carte, valide le format et s'assure
    qu'elle n'a pas déjà été distribuée.
    """
    while True:
        card_str = input(texte)

        if len(card_str) != 2:
            print("Erreur : La carte doit être composée de 2 caractères (ex: 'Kh' pour Roi de Coeur).")
            continue
        rank, suit = card_str[0], card_str[1]

        if rank not in "23456789TJQKA" or suit not in "shdc":
            print("Erreur : Valeur ou couleur invalide. Valeurs: 2-9,T,J,Q,K,A. Couleurs: s,h,d,c.")
            continue

        if card_str in cartes_exclues:
            print("Erreur : Cette carte a déjà été distribuée.")
            continue

        return card_str

def cote():
    P = int(input('Quel est le pot?'))
    B = int(input('Combien devez vous miser?'))
    return (B / (P + (J-1) * B))

def main():
    """Fonction principale qui gère le programme"""
    print("--- Calculateur d'Équité pour Poker Spin & Rush (3 joueurs) ---")
    print("Instructions : Entrez les cartes au format 'VALEURcouleur'.")
    print("Valeurs : 2, 3, 4, 5, 6, 7, 8, 9, T(10), J(Valet), Q(Dame), K(Roi), A(As)")
    print("Couleurs : s(Pique), h(Coeur), d(Carreau), c(Trèfle)")
    print("Exemple : Pour le Roi de Pique, entrez 'Ks'\n")

    cartes_connues = set()

    C1 = get_card("Entrez votre première carte : ", cartes_connues)
    cartes_connues.add(C1)
    C2 = get_card("Entrez votre deuxième carte : ", cartes_connues)
    cartes_connues.add(C2)

    hand = [C1, C2]
    board = []

    print("\nCalcul de l'équité pré-flop...")
    chance = equity(hand,board,nb_sim)
    print(f"Votre équité avec {hand} est de {chance:.2%}")
    """c = cote()
    if chance > c :
        print(f"Vous devriez misez. Cote : {c:.2%}")
    else :
        print(f"vous devriez fold. Cote : {c:.2%}")"""

    print("\n--- FLOP ---")
    f1 = get_card("Entrez la première carte du flop : ", cartes_connues)
    cartes_connues.add(f1)
    f2 = get_card("Entrez la deuxième carte du flop : ", cartes_connues)
    cartes_connues.add(f2)
    f3 = get_card("Entrez la troisième carte du flop : ", cartes_connues)
    cartes_connues.add(f3)

    board = [f1, f2, f3]

    print("\nCalcul de l'équité post-flop...")
    chance = equity(hand, board, nb_sim)
    print(f"Votre équité avec le board {board} est de {chance:.2%}")

    print("\n--- TURN ---")
    t1 = get_card("Entrez la carte du turn : ", cartes_connues)
    cartes_connues.add(t1)

    board.append(t1)

    print("\nCalcul de l'équité post-turn...")
    chance = equity(hand, board, nb_sim)
    print(f"Votre équité avec le board {board} est de {chance:.2%}")

    # --- Étape 4 : La River ---
    print("\n--- RIVER ---")
    r1 = get_card("Entrez la carte de la river : ", cartes_connues)
    cartes_connues.add(r1)

    board.append(r1)

    print("\nCalcul de l'équité finale...")
    chance = equity(hand, board, nb_sim)
    print(f"Votre équité finale avec le board complet {board} est de {chance:.2%}")


nb_sim = 10000
main()