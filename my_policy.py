from policy import CribbagePolicy
from deck import Deck
from collections import defaultdict
import scoring, random

class MyPolicy(CribbagePolicy):
    def __init__(self, game):
        super().__init__(game)

        
    def keep(self, hand, scores, am_dealer):
        remaining_deck = Deck(range(1,14), ['S', 'H', 'D', 'C'], 1)
        for card in hand:
            remaining_deck._cards.remove(card)
        crib = 1 if am_dealer else -1
        
        def score_split(indices):
            keep = []
            throw = []
            score = 0
            for i in range(len(hand)):
                if i in indices:
                    throw.append(hand[i])
                else:
                    keep.append(hand[i])
            for turn in remaining_deck._cards:
                score += scoring.score(self._game, keep, turn, False)[0] + crib * scoring.score(self._game, throw, turn, True)[0]
            score /= len(remaining_deck._cards)
            return keep, throw, score

        throw_indices = self._game.throw_indices()
        
        random.shuffle(throw_indices)

        keep, throw, best_score = max(map(lambda i: score_split(i), throw_indices), key=lambda t: t[2])
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
        best_card = None
        if history.has_legal_play(self._game, cards, 0 if am_dealer else 1):
            curr_count = history.total_points()
            best_score = None

            rank_count = defaultdict(int)
            for card in cards:
                rank_count[card.rank()] += 1

            if history.is_start_round():
                for card in cards:
                    card_rank = card.rank()
                    if card_rank == 4:
                        return card
                    # elif card_rank == 3:
                    #     return card
                    elif card_rank < 5 and rank_count[card_rank] > 1:
                        return card
                    elif card_rank < 5:
                        return card
                    elif rank_count[card_rank] > 1:
                        return card
                    elif card_rank != 10 and card_rank != 5:
                        best_card = card 
                    else:
                        best_card = card   
                return best_card

            for card in cards:
                card_rank = card.rank()
                new_count = curr_count + (card_rank if card_rank < 10 else 10)
                if new_count <= 31:                
                    if new_count == 15:
                        best_card = card
                        break
                    else:
                        score = history.score(self._game, card, 0 if am_dealer else 1)
                        if score is not None and (best_score is None or score > best_score):
                            best_score = score
                            best_card = card
                        if best_score == 0 and curr_count < 15 and new_count > 15:
                            best_card = card
                    
        return best_card

