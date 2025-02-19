import random
from montecarlo import monte_carlo_simulation


def simulate_hand(iterations=1000):
    """
    Simulate a Texas Hold'em hand progression with random card dealing.
    At each stage, the Monte Carlo simulation is called to estimate win odds.
    """
    # Define deck parameters using proper card symbols
    ranks = '23456789TJQKA'
    suits = {'h': '♥', 'd': '♦', 'c': '♣', 's': '♠'}
    deck = [r + suits[s] for r in ranks for s in suits]
    random.shuffle(deck)

    # Draw hero's hand (2 cards) and full set of community cards (5 cards)
    hero_hand = [deck.pop(), deck.pop()]
    community_cards_full = [deck.pop() for _ in range(5)]

    stages = [("Pre-flop", 0), ("Flop", 3), ("Turn", 4), ("River", 5)]

    print(f"Hero's hand: {hero_hand}\n")
    for stage, num_cards in stages:
        known_community = community_cards_full[:num_cards]
        print(f"Stage: {stage}")
        if known_community:
            print(f"Community cards: {known_community}")
        else:
            print("No community cards dealt yet.")

        # Get win odds from the Monte Carlo simulation
        win_pct = monte_carlo_simulation(
            hero_hand, known_community, num_opponents=1, iterations=iterations)
        print(f"Estimated Win Percentage: {win_pct:.2f}%\n")


if __name__ == "__main__":
    simulate_hand(iterations=2000)
