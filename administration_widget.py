from PySide6.QtWidgets import QGridLayout ,QHBoxLayout ,QVBoxLayout ,QPushButton, QComboBox, QWidget, QLabel,QLineEdit ,QHBoxLayout,QVBoxLayout
from administration_buttons import paid_box,recipe_box,attest_box,attandance_box


import pymongo

from utility import clearLayout, calculate_age


def read_collection(key,value):
    client = pymongo.MongoClient("localhost:27017")
    database = client.get_database("Tournament")
    collection = database.get_collection("Fencer")
    
    
    reg_ex_str=""
    for letter in value:
        reg_ex_str += "("+letter.upper()+"|"+letter.lower()+ ")"
    db_ret=collection.find({key:{"$regex": "^.*"+reg_ex_str+".*$"}})
    return db_ret

class administation_layout(QVBoxLayout):
    def __init__(self):
        super().__init__()

        self.selected_keys= ["lastname","firstname","club","attandence","paid","competition"]

        search_bar = QWidget()
        
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
        
        search_bar.setLayout(search_layout)

        self.addWidget(search_bar)
        self.work_widget = QWidget()

        self.widgets_in_worklayout =[]
        self.work_layout=QGridLayout()
        self.work_layout.addWidget(QLabel("Nachname, Vorname"),0,1)
        self.work_layout.addWidget(QLabel("Verein"),0,2)
        self.work_layout.addWidget(QLabel("Wettbewerb"),0,3)
        self.work_layout.addWidget(QLabel("Anwesend"),0,4)
        self.work_layout.addWidget(QLabel("Bezahlt"),0,5)
        self.work_layout.addWidget(QLabel("Quittung"),0,6)
        self.work_layout.addWidget(QLabel("Attest"),0,7)
        self.work_widget.setLayout(self.work_layout)
        self.addWidget(self.work_widget)
        self.addStretch()

    def button_submit_clicked(self):
        
        clearLayout(self.work_layout)
        self.work_layout.addWidget(QLabel("Nachname, Vorname"),0,1)
        self.work_layout.addWidget(QLabel("Verein"),0,2)
        self.work_layout.addWidget(QLabel("Wettbewerb"),0,3)
        self.work_layout.addWidget(QLabel("Anwesend"),0,4)
        self.work_layout.addWidget(QLabel("Bezahlt"),0,5)
        self.work_layout.addWidget(QLabel("Quittung"),0,6)
        self.work_layout.addWidget(QLabel("Attest"),0,7)
        db_ret=read_collection(
            key=self.search_key.currentText(),
            value = self.search_input.text())
        
        db_ret=sorted(db_ret,key=lambda x : x ["lastname"])
        counter=1
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
            self.widgets_in_worklayout.extend([person_name,club_name,comp_name,attan_box,pay_box,recei_box])
            
            
            self.work_layout.addWidget(person_name,counter,1)
            self.work_layout.addWidget(club_name,counter,2)
            self.work_layout.addWidget(comp_name,counter,3)
            self.work_layout.addWidget(attan_box,counter,4)
            self.work_layout.addWidget(pay_box,counter,5)
            self.work_layout.addWidget(recei_box,counter,6)
            self.work_layout.addWidget(attes_wid,counter,7)

            counter+=1
        self.work_widget.setLayout(self.work_layout)

    