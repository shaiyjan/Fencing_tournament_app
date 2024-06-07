
from preliminary import generate_ranking

from dbmongo import db


def create_elimination_round(tournament):
    participants_by_rank=generate_ranking(tournament=tournament,round=1)
    elimination_round(tournament=tournament,
        particpants_by_rank=participants_by_rank)

def next_match(name,prev_match_1,prev_match_2):
    winner_match_1 = prev_match_1["fencer1"] if (
        not prev_match_1["score2"] or int(prev_match_1["score1"])>int(prev_match_1["score2"])
                                    ) else prev_match_1["fencer2"]
    winner_match_2 = prev_match_2["fencer1"] if (
        not prev_match_2["score2"] or int(prev_match_2["score1"])>int(prev_match_2["score2"])
                                    ) else prev_match_2["fencer2"]

    match_round=prev_match_1["round"]>>1
    placing=min(prev_match_1["placing"],prev_match_2["placing"])

    next_match = db.find_one(collection=name,query={"placing":placing,"round":match_round})

    if next_match:
        if next_match["fencer1"] not in [winner_match_1,winner_match_2] or next_match["fencer2"] not in  [winner_match_1,winner_match_2]:
            db.del_one(collection=name,
                query={"_id":next_match["_id"]})
        else:
            return None
    
    match(tournament=name,
        fencer_A=winner_match_1,
        fencer_B=winner_match_2,
        match_round=match_round,
        placing=placing,
        elim_type=prev_match_1["type"])



def next_round(tournament,match_id):
    ...
    match_data= db.find_one(collection=tournament,query={"_id":match_id})
    match_round= match_data["round"]
    other_match = db.find_one(collection=tournament,
            query={"round":match_round, "placing": match_round-match_data["placing"]})
    

    if other_match["finished"]==True :
        winner_match = match_data["fencer1"] if match_data["score1"]>match_data["score2"] else   match_data["fencer2"]
        winner_other = other_match["fencer1"] if other_match["score1"]>other_match["score2"] else   other_match["fencer2"]

        if (match_round :=match_round<<1)>1:
            match(fencer_A=winner_match,
                fencer_B=winner_other,
                tournament=tournament,
                match_round=match_round<<1,
                placing=min(match_data["placing"],other_match["placing"]),
                elim_type=match_data["elimination_type"])
        else:
            ... # finish tournament?

class elimination_round:
    def __init__(self,tournament,particpants_by_rank):
        
        tournament_data=db.find_one(collection="Organisation",
                query={"name":tournament})
        elim_type=tournament_data["elimination_type"]

        
        match_round=1
        while match_round < len(particpants_by_rank):
            match_round = match_round << 1 #round*=2

        insertion={"wettbewerbsname":tournament,
            "type":"elimination"}

        db.insert(collection="Organisation",insertion=insertion)

        while len(particpants_by_rank) != match_round:
            particpants_by_rank.append(None)



        for i in range(match_round>>1): #round >>2 = round //2
            match(
                tournament=tournament,
                fencer_A=particpants_by_rank[i],
                fencer_B=particpants_by_rank[match_round-1-i],
                match_round=match_round,
                placing=i,
                elim_type=elim_type)

class match:
    def __init__(self,tournament,fencer_A,fencer_B,match_round,placing,elim_type):
        
        insertion ={"fencer1":fencer_A,
                "fencer2":fencer_B,
                "score1": None,
                "score2":None,
                "round":match_round ,
                "placing":placing,
                "type":"elimination",# + elim_type,
                "finished":False}

        if fencer_B==None:
            insertion["finished"]=True
            insertion["score1"]=15

        db.insert(collection=tournament,insertion=insertion)


