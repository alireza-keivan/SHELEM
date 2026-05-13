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
            deck+= [("16","red"), ("15","black")]
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
        suit_order= {'black':0,
                     'red':1,
                     'clubs':2,
                     'hearts':3,
                     'spades':4,
                     'diamonds':5,
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

class Bidding():
    deal = ShuffleDeal.deal()

    @classmethod
    def computation(cls):
        dict_keys = cls.deal[1].keys()
        val = []
        [val.append(cls.deal[1][i][0:12]) for i in dict_keys]
        group_x1, group_x2, group_y1, group_y2 = {},{},{},{}
        cls.groups =[group_x1, group_x2, group_y1, group_y2]

        for group, cards in zip(cls.groups,val):
            for r,s in cards:
                group.setdefault(s,[]).append(r)
        
        return cls.groups
    
    @staticmethod
    def formula(hand):
        suits = ['diamonds', 'spades', 'hearts', 'clubs']
        stds = [float(np.std([i.get(j,0) for i in hand])) for j in suits] # standard deviation calculation for z-score
        means = [float(np.mean([i.get(j, 0) for i in hand])) for j in suits]
        z_score = [
            {
                suit: round((i.get(suit, 0) - mu) / sigma, 3)
                if sigma != 0 else 0
                for suit, mu, sigma in zip(suits, means, stds)
            }
            for i in hand
        ]
        return z_score

    @classmethod
    def f_rank(cls):
        """
        Ranking suits for every player to estimate their potential for each strategy:
        1) Going negative: the rank is estimate raw as the trump is not defined yet.
        2) Bidding: suits must be prioritized based on points for bidding, 
           with a scrore calculation for each suit.
        """

        groups = cls.computation()
        suits = ['diamonds', 'spades', 'hearts', 'clubs']
        rank_map = {'red': 20, 'black':15}
        rank = []
        for g in groups:
            player = {
                suit:sum(int(card) for card in g.get(suit, []))
                for suit in suits
                }
            player['joker'] = sum(
                rank_map.get(joker,0)
                  for joker in ['red','black']
                    if joker in g
                    )
            rank.append(player) 
        # created a dict for each hand consisted of every suit + Jokers
        z_score = cls.formula(rank)

        return z_score, rank
        
    @classmethod   
    def f_count(cls):
        """counting every suit:
            we get the length of each suit for every player and save them in a dictionary! 
            e.g. {'diamonds': 4} showing player x1 has 4 diamonds in their hand 
        """
        groups = cls.computation()
        suits = ['diamonds', 'spades', 'hearts', 'clubs']
        count = [{i:len((n.get(i,[]))) for i in suits} for n in groups]
        
        z_score = cls.formula(count)
        return z_score, count

    @classmethod
    def f_point(cls):
        """special points are the special parts of Shelem! 
            we calculate each suit's value based on this criterion to have a better understanding of the hand's strength,
            both for bidding and going negative!  
        """
        points_dict = {'5':5,'10':10,'14':10,'15':15,'16':20}
        groups = cls.computation()
        points = [{k: sum(points_dict.get(card, 0) for card in cards) for k, cards in g.items()} for g in groups]
        z_score = cls.formula(points)
        return z_score, points

    @classmethod
    def score_points(cls,a=1,b=2,c=3):
        f_rank = cls.f_rank()
        f_count = cls.f_count()
        f_points = cls.f_point()
        #z-final = [a*f_rank+ b*f_count+ c*f_points]
        suits = ['diamonds', 'spades', 'hearts', 'clubs']
        final = [{s: round(rank.get(s,0) + count.get(s,0)+ point.get(s,0),3) for s in suits} for rank, count, point in zip(f_rank[0], f_count[0], f_points[0])]
        #print("rank:",f_rank[1], "\n"*2,'count:', f_count[1], "\n"*2, "point:", f_points[1], "\n"*2, "final:", final)
        print(f_rank[0], "\n"*2, f_rank[1], f_count, f_points)


bid = Bidding()
bid_1 = bid.score_points()

