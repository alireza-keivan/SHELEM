import random
class ShuffleDeal:
    players = ["x1", "x2", "y1", "y2"]
    suits = ["diamonds", "hearts", "clubs", "spades"]
    ranks = [2,3,4,5,6,7,8,9,10,11,12,13,14]
    Jokers = ["BJ", "RJ"]

    @classmethod
    def build_deck(cls, with_jokers = True):
        deck = [(r,s) for s in cls.suits for r in cls.ranks]
        cls.with_jokers = with_jokers
        if with_jokers:
            deck+= [("Red","Joker"), ("Black","Joker")]
        return deck

    @classmethod
    def shuffle(cls):
        cards = cls.build_deck()
        random.shuffle(cards)
        return cards

    @classmethod
    def deal(cls):
        cls.deck = cls.shuffle()
        dealt = {player: cls.deck[i*12:(i+1) *12]
            for i, player in enumerate(cls.players)}
        suit_order= {'clubs':0,
                     'hearts':1,
                     'spades':2,
                     'diamonds':3,
                     'Joker':4
                     }
        for player in dealt:
            dealt[player] = sorted(
                dealt[player],
                key=lambda card: (
                    suit_order[card[1]],
                    card[0] if isinstance(card[0], int) else 99
            ), reverse=True
        )
        sorted_players = sorted(dealt.items(), key = lambda item: item[0])
        return sorted_players

    @classmethod
    def remainings(cls):
        if cls.with_jokers:
            remainings = cls.deck[-6:]
            return remainings
        else:
            remainings = cls.deck[-4:]
            return remainings

class Bidding:
    def __init__(self):
        self.deal = ShuffleDeal.deal()
        self.remainings = ShuffleDeal.remainings()

    def computation(self):
        pass

    



"""obj1= ShuffleDeal()
p1 = obj1.deal()
p2 = obj1.remainings()
print(p1,p2)
"""
