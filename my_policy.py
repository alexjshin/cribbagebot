from policy import CribbagePolicy, CompositePolicy, GreedyThrower, GreedyPegger
from deck import Deck
import scoring

class MyPolicy(CribbagePolicy):
    def __init__(self, game):
        super().__init__(game)

        
    def keep(self, hand, scores, am_dealer):
        keep, throw, net_score = scoring.greedy_throw(self._game, hand, 1 if am_dealer else -1)
        return keep, throw

    def peg(self, cards, history, turn, scores, am_dealer):
        """
        general heuristic - series of 'if condition then score += constnat'
        Those adjustments are intended to capture the possibility of setting up points to be earned (or avoided) in future plays
        and include preventing the opponent from reaching a count of exactly 15, and setting up pairs on future plays.
        - possibility of setting up points to be earned later
        - preventing 15
            play fours, aces
        - setting up pairs
        """
        curr_count = history.total_points()
        best_card = None
        best_score = None
        # remaining_deck = Deck(range(1,14), ['S', 'H', 'D', 'C'], 1)
        # print(remaining_deck._cards)
        # print(history.total_points())

        for card in cards:
            new_count = curr_count + (card.rank() if card.rank() < 10 else 10)
            if new_count <= 31:                
                if history.is_start_round():
                    if card.rank() == 4:
                        best_card = card
                        break
                    elif card.rank() == 3:
                        best_card = card
                        break
                    else:
                        if card.rank() < 5:
                            best_card = card
                            break
                        elif card.rank() != 10 and card.rank() != 5:
                            best_card = card
                        else:
                            best_card = card
                else:
                    score = history.score(self._game, card, 0 if am_dealer else 1)
                    
                    if score is not None and (best_score is None or score > best_score):
                        best_score = score
                        best_card = card
        # print(history.plays())
        return best_card
