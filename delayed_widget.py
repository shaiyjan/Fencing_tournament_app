from PySide6.QtWidgets import (
    QPushButton, 
    QWidget, 
    QCheckBox, 
    QGridLayout,
    QLineEdit,
    QLabel,
    QComboBox,
    QHBoxLayout,
    QDateEdit
    )

import pymongo

from utility import connect_database

m = "männlich", "M"
w= "weiblich", "F"

""" rewrite with form widget"""

from PySide6.QtWidgets import QFormLayout

class delayed_widget(QWidget):
    def __init__(self):
        super().__init__()
        self.first_name_input = QLineEdit()
        self.last_name_input =QLineEdit()
        self.dateofbirth_input=QDateEdit()
        self.gender_input= QComboBox()
        self.tournament_input = QComboBox()
        self.paid_input = QCheckBox()
        self.attandence_input = QCheckBox()
        self.attandence_input.setChecked(True)
        self.nation_input=QLineEdit()
        self.club_input=QLineEdit()
        self.recipe_input =QCheckBox()
        self.gender_input.addItems([m[0],w[0]])

        collection = connect_database()
        list_of_comp=collection.distinct("competition")
        self.tournament_input.addItems(list_of_comp)


        self.setLayout(QFormLayout())
        layout : QFormLayout = self.layout() #type: ignore
        layout.addRow("Nachname*:", self.last_name_input) 
        layout.addRow("Vorname*:",self.first_name_input) 
        layout.addRow("Geburtsdatum",self.dateofbirth_input) 
        layout.addRow("Geschlecht",self.gender_input) 
        layout.addRow("Wettbewerb",self.tournament_input) 
        layout.addRow("Bezahlt:",self.paid_input)  
        layout.addRow("Anwesend:",self.attandence_input) 
        layout.addRow("Quittung",self.recipe_input) 

        submit_button =QPushButton("Hinzufügen")
        cancel_button =QPushButton("Abbrechen")
        
        button_row=QHBoxLayout()
        button_row.addWidget(submit_button)
        button_row.addWidget(cancel_button)
        layout.addRow(button_row)

        
        submit_button.clicked.connect(self.submit_button_clicked)
        cancel_button.clicked.connect(self.cancel_button_clicked)

        
    def cancel_button_clicked (self):
        self.close()

    def submit_button_clicked(self):
        collection = connect_database()

        add_dict={
            "firstname":self.first_name_input.text(),
            "lastname":self.last_name_input.text(),
            "dateofbirth":self.dateofbirth_input.text() ,
            "gender":self.gender_input.currentText(),
            "competition":self.tournament_input.currentText(),
            "paid": "yes" if self.paid_input.isChecked() else "no",
            "attandance": "yes" if self.attandence_input.isChecked() else "no",
            "nation":self.nation_input.text(),
            "club":self.club_input.text(),
            "recipe": "yes" if self.recipe_input.isChecked() else "no",
        }
        
        collection.insert_one(add_dict)
        self.cancel_button_clicked()

class delayed_widget_old(QWidget):

    def __init__(self):
        super().__init__()
        layout = QGridLayout()

        self.setWindowTitle("Nachtrag")

        first_name_label = QLabel("Vorname*:")
        last_name_label  = QLabel("Nachname*:")
        dateofbirth_label = QLabel("Geburtsdatum:")
        gender_label =QLabel("Geschlecht:")
        nation_label = QLabel("Land:")
        club_label = QLabel("Verein:")
        tournament_label = QLabel("Wettbewerb:")
        paid_label =QLabel("Bezahlt:")
        attandence_label =QLabel("Anwesend:")
        recipe_label =QLabel("Quittung:")


        self.first_name_input = QLineEdit()
        self.last_name_input =QLineEdit()
        self.dateofbirth_input=QLineEdit() #date Widget?
        self.gender_input= QComboBox()
        self.tournament_input = QComboBox()
        self.paid_input = QCheckBox()
        self.attandence_input = QCheckBox()
        self.attandence_input.setChecked(True)
        self.nation_input=QLineEdit()
        self.club_input=QLineEdit()
        self.recipe_input =QCheckBox()


        self.gender_input.addItems([m[0],w[0]])

        collection = connect_database()
        list_of_comp=collection.distinct("competition")
        self.tournament_input.addItems(list_of_comp)
        
        layout.addWidget(first_name_label,0,0)
        layout.addWidget(last_name_label, 1,0)
        layout.addWidget(dateofbirth_label,2,0)
        layout.addWidget(gender_label,3,0)
        layout.addWidget(nation_label,4,0)
        layout.addWidget(club_label,5,0)
        layout.addWidget(tournament_label,6,0)
        layout.addWidget(paid_label,7,0)
        layout.addWidget(attandence_label,8,0)
        layout.addWidget(recipe_label,9,0)
        layout.addWidget(self.first_name_input,0,1)
        layout.addWidget(self.last_name_input, 1,1)
        layout.addWidget(self.dateofbirth_input,2,1)
        layout.addWidget(self.gender_input,3,1)
        layout.addWidget(self.nation_input,4,1)
        layout.addWidget(self.club_input,5,1)
        layout.addWidget(self.tournament_input,6,1)
        layout.addWidget(self.paid_input,7,1)
        layout.addWidget(self.attandence_input,8,1)
        layout.addWidget(self.recipe_input,9,1)

        submit_button =QPushButton("Hinzufügen")
        cancel_button =QPushButton("Abbrechen")
        submit_button.clicked.connect(self.submit_button_clicked)
        cancel_button.clicked.connect(self.cancel_button_clicked)

        layout.addWidget(submit_button,10,0)
        layout.addWidget(cancel_button,10,1)

        self.setLayout(layout)

    def cancel_button_clicked (self):
        self.close()

    def submit_button_clicked(self):
        collection = connect_database()

        add_dict={
            "firstname":self.first_name_input.text(),
            "lastname":self.last_name_input.text(),
            "dateofbirth":self.dateofbirth_input.text() ,#date Widget?
            "gender":self.gender_input.currentText(),
            "competition":self.tournament_input.currentText(),
            "paid": "yes" if self.paid_input.isChecked() else "no",
            "attandance": "yes" if self.attandence_input.isChecked() else "no",
            "nation":self.nation_input.text(),
            "club":self.club_input.text(),
            "recipe": "yes" if self.recipe_input.isChecked() else "no",
        }
        
        collection.insert_one(add_dict)
        self.cancel_button_clicked()
        