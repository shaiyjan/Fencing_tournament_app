
from utility import new_matrix

from collections import namedtuple
from dbmongo import db

id_rank=namedtuple("id_rank","id rank")


def preliminary_by_preliminary(tournament : str, round: int):

    org_data=db.find_one(collection="Organisation",query={"name":tournament})
    group_dict = [*db.find_all(collection=tournament,query={"type":"preliminary","round":round})]
    person_score_list=[]
    for group in group_dict:
        persons=group["group"]
        table=group["table"]
        for i in range(len(persons)):
            person_score_list.append([persons[i],*table[i][-7:None]])

    person_score_list.sort(key= lambda el: (float(el[3].strip("%")),int(el[-2])),reverse=True)

    group_am=len(group_dict)
    new_groups=[]
    for i in range(group_am):
        new_groups.append([])
    for i in range(len(person_score_list)):
        new_groups[i % group_am].append(person_score_list[i][0])
    preliminary(name=tournament,groups=new_groups,rounds=round-1,elim_type=org_data["elimination_type"])



def groups_by_ranking_func(fencer_ids : list[int],number_of_groups :int):
    rank_list=[]
    for id in fencer_ids:
        rank=db.find_one("Fencer",query={"_id": id})["ranking"]
        idr = id_rank(id,rank)
        rank_list.append(idr)
    rank_list.sort(key= lambda x: x.rank,reverse=True)

    groups=new_matrix(1,number_of_groups)

    group_number=0
    while rank_list:
        groups[group_number].append(rank_list.pop()[0])
        group_number +=1
        group_number =group_number % number_of_groups
    return  groups

class preliminary:
    def __init__(self,name,groups : list[list[dict]],rounds,elim_type):
        self.elimination_type=elim_type
        self.tournament_name=name
        self.group_counter=0
        self.finished=False
        for group in groups:
            prelimary_group(parent=self,name=name,group=group,round=rounds)

        db.insert("Organisation", {
                "name":name,
                "preliminary_rounds":rounds,
                "elimination_type":elim_type
        })

class prelimary_group:
    def __init__(self,name,parent : preliminary,group,round : int):
        parent.group_counter+=1

        self.group_dict={"id":[el["_id"] for el in group],
                "type":"preliminary",
                "round": round,
                "group":group,
                "group_number": parent.group_counter,
                "table":[],
                "finished":False}
        
        db.insert(name,self.group_dict)


