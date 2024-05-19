from datetime import date

class part_counter:
    def __init__(self,attendant,total):
        self.nom=attendant
        self.denom=total

    def __str__(self):
        return f"{len(self.nom)}/{len(self.denom)}"

    def __add__(self,other):
        if type(other)==type(self):
            nom_ids=self.nom
            denom_ids=self.denom
            for id in other.nom:
                if id not in nom_ids:
                    nom_ids.append(id)
            for id in other.denom:
                if id not in denom_ids:
                    denom_ids.append(id)
            return part_counter(
                nom_ids,denom_ids)


def calculate_age(day,month,year):
    today = date.today()
    return today.year - int(year) - ((today.month, today.day) < (int(month), int(day)))


def clearLayout(layout):
  """https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt"""
  while layout.count():
    child = layout.takeAt(0)
    if child.widget():
      child.widget().deleteLater()

def new_matrix(row : int,col : int):
  mat=[]
  for x in range(row):
    mat.append([]*col)
  return(mat)


def altersklasse(string_in : str, season_year : int):
    _,_,year = string_in.split(".")
    ret_val = None
    match season_year-int(year):
        case 10|11:
            ret_val="U11"
        case 12|13:
            ret_val="U13"
        case 14|15:
            ret_val="U15"
        case 16|17:
            ret_val="U17"
        case 18|19|20:
            ret_val="U20"
        case _:
            ret_val="Senioren"
    return ret_val

if __name__=="__main__":
    print(altersklasse("14.04.2014",2024))
