from datetime import date


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
    mat.append([None]*col)
  return(mat)
