from PySide6.QtWidgets import (
    QLayout,
    QGridLayout,
    QHBoxLayout,
    QPushButton,
    QComboBox,
    QWidget,
    QLabel,
    QLineEdit)
from PySide6.QtCore import Qt

from administration_buttons import paid_box,recipe_box,attest_box,attandance_box

from utility import calculate_age, connect_database


def read_collection(key,value):
    
    collection = connect_database()
    reg_ex_str=""
    for letter in value:
        reg_ex_str += "("+letter.upper()+"|"+letter.lower()+ ")"
    db_ret=collection.find({key:{"$regex": "^.*"+reg_ex_str+".*$"}})

    return db_ret

class administation_layout(QGridLayout):
    def __init__(self):
        super().__init__()

        self.selected_keys= ["lastname","firstname","club","attandence","paid","competition"]
        self.setSizeConstraint(QLayout.SetMinimumSize) #type: ignore
        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        
        search_label = QLabel("Suche")
        self.search_key = QComboBox()
        self.search_key.addItems(self.selected_keys)
        search_submit_button = QPushButton("Suche")
        self.search_input= QLineEdit()
        search_layout=QHBoxLayout()
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_key)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_submit_button)

        search_submit_button.clicked.connect(self.button_submit_clicked)
        
        self.addLayout(search_layout,0,0,1,6)
        
        self.addWidget(QLabel("Nachname, Vorname"),1,0)
        self.addWidget(QLabel("Verein"),1,1)
        self.addWidget(QLabel("Wettbewerb"),1,2)
        self.addWidget(QLabel("Anwesend"),1,3)
        self.addWidget(QLabel("Bezahlt"),1,4)
        self.addWidget(QLabel("Quittung"),1,5)
        self.addWidget(QLabel("Attest"),1,6)
        

    def button_submit_clicked(self):

        for row in range(2,self.rowCount()):
            for col in range(6):
                if self.itemAtPosition(row,col) and self.itemAtPosition(row,col).widget():
                    self.itemAtPosition(row,col).widget().deleteLater()

        db_ret=read_collection(
            key=self.search_key.currentText(),
            value = self.search_input.text())
        
        db_ret=sorted(db_ret,key=lambda x : x ["lastname"])
        counter=2
        for it in db_ret:
            id=it["_id"]
            person_name = QLabel(f"{it['lastname'].capitalize()}, {it['firstname']}")
            club_name =  QLabel(f"{it['club']}")
            comp_name = QLabel(f"{it['competition']}")
            attan_box=attandance_box(id,True if it["attandence"]=="yes" else False)
            pay_box=paid_box(id,True if it["paid"]=="yes" else False)
            age=calculate_age(*it["dateofbirth"].strip().split("."))
            recei_box = recipe_box(id,True if it["recipe"]=="yes" else False)
            if age <18:
                attes_wid=attest_box(id,True if it["attest"]=="yes" else False)
            else:
                attes_wid=QWidget()
            
            self.addWidget(person_name,counter,0)
            self.addWidget(club_name,counter,1)
            self.addWidget(comp_name,counter,2)
            self.addWidget(attan_box,counter,3)
            self.addWidget(pay_box,counter,4)
            self.addWidget(recei_box,counter,5)
            self.addWidget(attes_wid,counter,6)

            counter+=1

                

    