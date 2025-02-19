import random
import itertools

# Mapping for card ranks to numeric values
RANK_VALUES = {r: i for i, r in enumerate("23456789TJQKA", start=2)}


def evaluate_five_card_hand(cards):
    """
    Evaluate a 5-card hand and return a tuple representing its rank.
    Higher tuples indicate stronger hands.
    """
    ranks = [card[0] for card in cards]
    suits = [card[1] for card in cards]
    rank_nums = sorted([RANK_VALUES[r] for r in ranks], reverse=True)

    # Count frequencies
    freqs = {r: ranks.count(r) for r in set(ranks)}
    counts = sorted(freqs.values(), reverse=True)

    # Check for flush
    flush = len(set(suits)) == 1

    # Check for straight (including wheel: A-2-3-4-5)
    unique_nums = sorted(set(rank_nums))
    straight = False
    high_straight = None
    for combo in itertools.combinations(unique_nums, 5):
        if max(combo) - min(combo) == 4 and len(combo) == 5:
            straight = True
            high_straight = max(combo)
    if set([14, 2, 3, 4, 5]).issubset(set(rank_nums)):
        straight = True
        high_straight = 5

    if flush and straight:
        return (9, high_straight)
    if 4 in counts:
        quad_rank = max(r for r, count in freqs.items() if count == 4)
        kicker = max(RANK_VALUES[r] for r in freqs if freqs[r] != 4)
        return (8, RANK_VALUES[quad_rank], kicker)
    if 3 in counts and 2 in counts:
        trip_rank = max(r for r, count in freqs.items() if count == 3)
        pair_rank = max(r for r, count in freqs.items() if count == 2)
        return (7, RANK_VALUES[trip_rank], RANK_VALUES[pair_rank])
    if flush:
        return (6, rank_nums)
    if straight:
        return (5, high_straight)
    if 3 in counts:
        trip_rank = max(r for r, count in freqs.items() if count == 3)
        kickers = sorted(
            (RANK_VALUES[r] for r in freqs if freqs[r] != 3), reverse=True)
        return (4, RANK_VALUES[trip_rank], kickers)
    if counts.count(2) >= 2:
        pair_ranks = sorted(
            (RANK_VALUES[r] for r, count in freqs.items() if count == 2), reverse=True)
        kicker = max(RANK_VALUES[r] for r in freqs if freqs[r] == 1)
        return (3, pair_ranks, kicker)
    if 2 in counts:
        pair_rank = max(r for r, count in freqs.items() if count == 2)
        kickers = sorted(
            (RANK_VALUES[r] for r in freqs if freqs[r] == 1), reverse=True)
        return (2, RANK_VALUES[pair_rank], kickers)
    return (1, rank_nums)


def evaluate_hand(cards):
    """
    From 7 cards, determine the best possible 5-card hand.
    """
    best = (0,)
    for five in itertools.combinations(cards, 5):
        score = evaluate_five_card_hand(list(five))
        if score > best:
            best = score
    return best


def monte_carlo_simulation(hero_hand, community_cards, num_opponents=1, iterations=1000):
    """
    Run a Monte Carlo simulation to estimate winning odds.

    Args:
        hero_hand (list): Hero's cards.
        community_cards (list): Known community cards (0 to 5 cards).
        num_opponents (int): Number of opponents.
        iterations (int): Number of simulation iterations.

    Returns:
        float: Estimated win percentage for hero.
    """
    wins = ties = losses = 0

    # Build full deck with proper suit symbols
    ranks = '23456789TJQKA'
    suits = {'h': '♥', 'd': '♦', 'c': '♣', 's': '♠'}
    full_deck = [r + suits[s] for r in ranks for s in suits]

    # Remove known cards (hero and community)
    known_cards = hero_hand + community_cards
    for card in known_cards:
        full_deck.remove(card)

    for _ in range(iterations):
        deck = full_deck[:]  # copy deck
        random.shuffle(deck)

        # Complete community cards if fewer than 5 are known
        complete_community = community_cards.copy()
        while len(complete_community) < 5:
            complete_community.append(deck.pop())

        # Deal opponent hands (each 2 cards)
        opponents = []
        for _ in range(num_opponents):
            opponents.append([deck.pop(), deck.pop()])

        # Evaluate hero's best hand
        hero_best = evaluate_hand(hero_hand + complete_community)

        # Evaluate opponents' best hands
        opponent_bests = [evaluate_hand(opponent + complete_community) for opponent in opponents]
        best_opponent = max(opponent_bests)

        if hero_best > best_opponent:
            wins += 1
        elif hero_best == best_opponent:
            ties += 1
        else:
            losses += 1

    return wins / iterations * 100
