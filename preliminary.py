
from utility import new_matrix

from collections import namedtuple
from dbmongo import db

id_rank=namedtuple("id_rank","id rank")

def create_elimination_round(tournament_name,elim_type,part_by_rank):
    ...

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
    preliminary_id = 0
    def __init__(self,name,groups : list[dict],rounds:list[int],elim_type):
        self.elimination_type=elim_type
        self.tournament_name=name
        self.id=preliminary.preliminary_id
        preliminary.preliminary_id +=1
        self.group_counter=0
        self.rounds=rounds
        self.groups=[]
        self.finished=False
        round=self.rounds.pop()
        for group in groups:
            self.groups.append(prelimary_group(name,self,group,round=round))

    def check_finished(self):
        for group in self.groups:
            if group.finished == False:
                return
        else:
            part_by_rank=self.generate_ranking()
            if not self.rounds:
                new_groups=groups_by_ranking_func(part_by_rank,len(self.groups))
                preliminary(self.tournament_name,new_groups,self.rounds,self.elimination_type)
            else:
                create_elimination_round(
                    self.tournament_name,
                    self.elimination_type,
                    part_by_rank)
            
    def generate_ranking(self) -> list[int]:
        score =[]
        for group in self.groups:
            score.append(group[1]+group[-6:])
        score.sort(key = lambda  x: (x[-4],x[-1]))
        
        return [el[0] for el in score]

class prelimary_group:
    def __init__(self,name,parent : preliminary,group,round : int):
        self.group_id= parent.group_counter
        self.parent=parent
        parent.group_counter+=1

        self.group_dict={"id":[el["_id"] for el in group],
                "type":"preliminary" + str(round),
                "group":group,
                "table":[],
                "finished":False}
        db.insert(name,self.group_dict)

    def __dict__(self):
        return self.group_dict

    def insert_table(self,input_table: list[list[int]]):
        for index,_ in enumerate(input_table):
            if len(input_table[index])==len(self.table[index]):
                continue
        else:
            self.table=input_table
            self.finished,self.table=check_group_finished(self.table)

        if self.finished:
            db.update_one("Preliminary",
                query={"id": self.group_id},
                update_dict={"table": []})
            self.parent.check_finished()
        
def check_group_finished( table : list[list]):
    size=len(table)
    bool_val=True
    for i in range(size):
        for j in range(size):
            try:
                table[i][j]=int(table[i][j])
            except TypeError | ValueError:
                return False,table
            
            

    if bool_val:
        for i in range(size):
            hit_set=0
            hit_get=0
            wins = 0
            for j in range(size):
                hit_set += table[i][j]
                hit_get += table[j][i]
                if table[i][j]>table[j][i]:
                    wins+=1
            table[i].extend([wins,size,wins/size,hit_set,hit_get,hit_set-hit_get])
    
    row = [i for i in range(4)]
    row.sort(key = lambda ind: (table[ind][-4],table[ind][-1]))
    for pos,i in enumerate(row):
        table[i].append(pos+1)
    return True,table