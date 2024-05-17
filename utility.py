from datetime import date
import pymongo

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



def connect_database() :
  client = pymongo.MongoClient("localhost:27017")
  database = client.get_database("Tournament")
  collection = database.get_collection("Fencer")

  return collection

def connect_prelimnary():
  client = pymongo.MongoClient("localhost:27017")
  database = client.get_database("Tournament")
  collection = database.get_collection("Preliminary")

  return collection


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
