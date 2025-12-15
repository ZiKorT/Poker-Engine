# poker_engine.py

import csv
import random
import itertools
import time  # Pour tester la vitesse

# --- CONSTANTES ET INITIALISATION ---
RANKS = "23456789TJQKA"
SUITS = "shdc"
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

Flushes = {}
Unique5 = {}
PrimeProduct = {}


def generate_deck():
    """Crée un dictionnaire de 52 cartes (str: int)."""
    deck = {}
    for i, rank_char in enumerate(RANKS):
        for j, suit_char in enumerate(SUITS):
            prime_val = PRIMES[i]
            rank_val = i << 8
            suit_val = (1 << j) << 12
            rank_mask = (1 << i) << 16
            card_int = prime_val | rank_val | suit_val | rank_mask
            deck[rank_char + suit_char] = card_int
    return deck


DECK_INT = generate_deck()


def generate_lookup():
    """Charge les tables de consultation depuis le CSV."""
    # Cette fonction peut être lente au démarrage, mais n'est exécutée qu'une fois.
    with open("Flushes.csv", mode='r', newline='', encoding='utf-8') as fichier_csv:
        lecteur_csv = csv.reader(fichier_csv, delimiter=';')
        next(lecteur_csv)  # Ignorer l'en-tête
        for l in lecteur_csv:
            rank, c1, c2, c3, c4, c5, hand_type = l[0].strip(), l[1].strip(), l[2].strip(), l[3].strip(), l[4].strip(), \
            l[5].strip(), l[6].strip()

            # Utilise une couleur fixe (pique 's') pour générer les clés, car la couleur n'importe pas pour le rang
            cards_int = [
                DECK_INT[c1 + 's'], DECK_INT[c2 + 's'], DECK_INT[c3 + 's'],
                DECK_INT[c4 + 's'], DECK_INT[c5 + 's']
            ]

            if hand_type == "F" or hand_type == "SF":
                key = (cards_int[0] | cards_int[1] | cards_int[2] | cards_int[3] | cards_int[4]) >> 16
                Flushes[str(key)] = rank
            elif hand_type == "HC" or hand_type == "S":
                key = (cards_int[0] | cards_int[1] | cards_int[2] | cards_int[3] | cards_int[4]) >> 16
                Unique5[str(key)] = rank
            else:
                product_key = (cards_int[0] & 0xFF) * (cards_int[1] & 0xFF) * (cards_int[2] & 0xFF) * \
                              (cards_int[3] & 0xFF) * (cards_int[4] & 0xFF)
                PrimeProduct[str(product_key)] = rank



def get_hand_rank(hand_int):
    """Prend 5 cartes (entiers) et retourne leur rang."""
    if hand_int[0] & hand_int[1] & hand_int[2] & hand_int[3] & hand_int[4] & 0xF000:
        key = (hand_int[0] | hand_int[1] | hand_int[2] | hand_int[3] | hand_int[4]) >> 16
        return int(Flushes[str(key)])

    key = (hand_int[0] | hand_int[1] | hand_int[2] | hand_int[3] | hand_int[4]) >> 16
    # Utiliser .get() est plus sûr si une clé pouvait manquer, mais ici on sait qu'elle existera.
    rank = Unique5.get(str(key))
    if rank:
        return int(rank)

    product_key = (hand_int[0] & 0xFF) * (hand_int[1] & 0xFF) * (hand_int[2] & 0xFF) * \
                  (hand_int[3] & 0xFF) * (hand_int[4] & 0xFF)
    return int(PrimeProduct[str(product_key)])


def evaluate7(seven_cards_int):
    """Évalue le meilleur score pour 5 cartes parmi 7 (version rapide)."""
    best_score = 7462
    for hand_combination in itertools.combinations(seven_cards_int, 5):
        score = get_hand_rank(list(hand_combination))
        if score < best_score:
            best_score = score
    return best_score



def equity(hand, board, nb_simulation):
    """Calcule l'équité de manière optimisée."""
    hand_int = [DECK_INT[c] for c in hand]
    board_int = [DECK_INT[c] for c in board]

    known_cards_int = set(hand_int + board_int)
    deck_int = [c for c in DECK_INT.values() if c not in known_cards_int]

    wins, ties = 0, 0
    cards_to_draw = 4 + (5 - len(board))

    for _ in range(nb_simulation):
        draw = random.sample(deck_int, cards_to_draw)

        opponent1_hand = draw[0:2]
        opponent2_hand = draw[2:4]
        drawn_board = draw[4:]

        current_board = board_int + drawn_board

        my_score = evaluate7(hand_int + current_board)
        score_opp1 = evaluate7(opponent1_hand + current_board)
        score_opp2 = evaluate7(opponent2_hand + current_board)

        if my_score < score_opp1 and my_score < score_opp2:
            wins += 1
        elif my_score == score_opp1 and my_score == score_opp2:
            ties += 1  # Égalité à 3
        elif my_score == score_opp1 or my_score == score_opp2:
            ties += 1  # Égalité à 2

    return (wins + (ties / 3)) / nb_simulation


# --- CHARGEMENT AU DÉMARRAGE ---
print("Génération des tables de consultation, veuillez patienter...")
start_time = time.time()
generate_lookup()
end_time = time.time()
print(f"Tables générées en {end_time - start_time:.2f} secondes.")