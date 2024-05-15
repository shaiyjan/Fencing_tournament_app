

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


