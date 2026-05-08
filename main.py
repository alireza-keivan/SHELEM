import random
import numpy as np
from collections import defaultdict
class ShuffleDeal:
    players = ["x1", "x2", "y1", "y2"]
    suits = ["diamonds", "hearts", "clubs", "spades"]
    ranks = ['2','3','4','5','6','7','8','9','10','11','12','13','14']

    @classmethod
    def build_deck(cls, with_jokers = True):
        """
            This method buils a deck of cards based on the previous variables we defined in the class.
            Xs and Ys are allies. 
            There is also an option for playing this game with Jokers(set as default) and if so,
            the jokers are added to the deck
            ** 11,12,13, and 14 are interpreted as J,Q,K, and A
        """
        deck = [(r,s) for s in cls.suits for r in cls.ranks]
        cls.with_jokers = with_jokers
        if with_jokers:
            deck+= [("20","Red"), ("15","Black")]
        return deck

    @classmethod
    def shuffle(cls):
        """This merely shuffles the deck using the random library"""
        cards = cls.build_deck()
        random.shuffle(cards)
        return cards

    @classmethod
    def deal(cls):
        """This methods deals the deck between players. Each player receives exctly 12 cards, 
           and the remaining 6 cards are put on the ground.
           The for loop, sorts cards from high to low, where each suits is placed next to
           the oppposite color to avoid visual mistakes by players. 
           Jokers are placed at the end, as the trump is not known yet"""
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
        # sorting_players' hands: (x1,x2,y1,y2). "sorting_players" its a list, but "dealt" is a dictionary!
        sorted_players = sorted(dealt.items(), key = lambda item: item[0])

        return sorted_players, dealt

    @classmethod
    
    def remainings(cls):
        """if jokers are played, we have 6 cards on the ground, else there are 4!"""
        if cls.with_jokers:
            remainings = cls.deck[-6:]
            return remainings
        else:
            remainings = cls.deck[-4:]
            return remainings

class Bidding:
    
    @classmethod
    def computation(cls):
        cls.deal = ShuffleDeal.deal()
        dict_keys = cls.deal[1].keys()
        val = []
        [val.append(cls.deal[1][i][0:12]) for i in dict_keys]
        group_x1, group_x2, group_y1, group_y2 = {},{},{},{}
        cls.groups =[group_x1, group_x2, group_y1, group_y2]

        for group, cards in zip(cls.groups,val):
            for r,s in cards:
                group.setdefault(s,[]).append(r)
        
        return cls.groups
    
    @classmethod
    def f_rank(cls):
        """
        Ranking suits for every player to estimate their potential for each strategy:
        1) Going negative: the rank is estimate raw as the trump is not defined yet.
        2) Bidding: suits must be prioritized based on points for bidding, 
           with a score calculation for each suit.
        """
        hands = cls.computation()
        all_dicts = [{k:sum(map(int, v)) for k, v in g.items()} for g in hands]
        sorted_dicts = [dict(sorted(i.items(), key=lambda item: item[1], reverse=True)) for i in all_dicts]
        a = [sum(map(int, i.values()))for i in sorted_dicts]
        
        return sorted_dicts
        
    @classmethod
    def f_count(cls):
        groups = cls.computation()
        count = [{k: len(v) for k, v in g.items()} for g in groups]

        return count
    @classmethod
    def f_point(cls):
        points_dict = {'5':5,'10':10,'14':10,'15':15,'20':20}
        groups = cls.computation()
        points = [{k: sum(points_dict.get(card, 0) for card in cards) for k, cards in g.items()} for g in groups]

        return points

    @classmethod
    def score_points(cls,a=1,b=2,c=3):
        f_rank = cls.f_rank()
        print(f_rank[0].get("diamonds"))
        """mu_f_rank = np.mean(f_rank)
        sigma_f_rank = np.std(f_rank)
        z_rank = (f_rank-mu_f_rank) / sigma_f_rank

        f_count = cls.f_count()
        mu_count = np.mean(f_count)
        sigma_f_count = np.std(f_count)
        z_count = (f_count-mu_count) / sigma_f_count

        f_points = cls.f_point()
        mu_points = np.mean(f_points)
        sigma_f_points = np.std(f_points)
        z_points = (f_points-mu_points)/sigma_f_points
        
        cls.score = (a* z_rank) + (b* z_count) + (c* z_points)
        """
          
        
        
        """
        #mu_r = np.mean(f_rank)
        sigma_r = np.std(f_rank)
        z = (x - np.mean(x)) / np.std(x)
        z_rank = (f_rank - mu_r) / sigma_r
        score = alpha*z_rank + beta*z_count + gamma*z_points
        features = np.vstack([z_rank, z_count, z_points])
        weights = np.array([alpha, beta, gamma])
        score = weights @ features
        """ 
        

"""obj1= ShuffleDeal()
p1 = obj1.deal()
p2 = obj1.remainings()
print(p1,p2)
"""
bid = Bidding()
bid_1 = bid.score_points()
print(bid_1)
#print(bid_1)
#l1 = [1,2,3]
