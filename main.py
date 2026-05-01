import random
import numpy as np
from collections import defaultdict
class ShuffleDeal:
    players = ["x1", "x2", "y1", "y2"]
    suits = ["diamonds", "hearts", "clubs", "spades"]
    ranks = ['2','3','4','5','6','7','8','9','10','11','12','13','14']

    @classmethod
    def build_deck(cls, with_jokers = True):
        deck = [(r,s) for s in cls.suits for r in cls.ranks]
        cls.with_jokers = with_jokers
        if with_jokers:
            deck+= [("20","Red"), ("15","Black")]
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
                     'Black':4,
                     'Red':5
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
        return sorted_players, dealt

    @classmethod
    def remainings(cls):
        if cls.with_jokers:
            remainings = cls.deck[-6:]
            return remainings
        else:
            remainings = cls.deck[-4:]
            return remainings

class Bidding:
    
    @classmethod
    def computation(cls):
        from collections import defaultdict
        cls.deal = ShuffleDeal.deal()
        """ranks_dict = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'11':11,'12':12,'13':13,'14':14, "joker_black":15, "joker_red":16}
        points_dict = {'5':5,'10':10,'14':10,'16':15,'17':20}
        joker_dict={'Joker_black':15, "Joker_Red":20}"""

        dict_keys = cls.deal[1].keys()
        val = []
        [val.append(cls.deal[1][i][0:12]) for i in dict_keys]
        cls.group_x1, cls.group_x2, cls.group_y1, cls.group_y2 = {},{},{},{}
        cls.groups =[cls.group_x1, cls.group_x2, cls.group_y1, cls.group_y2]

        for group, cards in zip(cls.groups,val):
            for r,s in cards:
                group.setdefault(s,[]).append(r)
        @classmethod
        def f_rank(cls, group):
            total = 0
            for suit, rank in group:
                if rank == "Red":
                    total+= 20
                if rank == 'Black':
                    total+= 15
                else: 
                    total+= int(suit)
            return(total)
        
        
        return f_rank(cls.group_x1.keys())
        def f_count(cards):
            suits = defaultdict(list)
            for rank, suit in cards:
                suits[suit.lower()].append((rank,suit))

        """"
        #mu_r = np.mean(f_rank)
        sigma_r = np.std(f_rank)
        z = (x - np.mean(x)) / np.std(x)
        z_rank = (f_rank - mu_r) / sigma_r
        score = alpha*z_rank + beta*z_count + gamma*z_points
        features = np.vstack([z_rank, z_count, z_points])
        weights = np.array([alpha, beta, gamma])
        score = weights @ features
        """ 
        return x




"""obj1= ShuffleDeal()
p1 = obj1.deal()
p2 = obj1.remainings()
print(p1,p2)
"""
bid = Bidding()
bid_1 = bid.computation()
print(bid_1)
#l1 = [1,2,3]
