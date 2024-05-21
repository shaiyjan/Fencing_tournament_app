from PySide6.QtWidgets import (
    QPushButton, 
    QWidget, 
    QCheckBox, 
    QLineEdit,
    QComboBox,
    QHBoxLayout,
    QDateEdit
    )

from dbmongo import db

m = "männlich", "M"
w= "weiblich", "F"

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

        list_of_comp:list[str]= db.get_distinct_values("Fencer","competition")
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

        


        add_dict={
            "firstname":self.first_name_input.text(),
            "lastname":self.last_name_input.text(),
            "dateofbirth":self.dateofbirth_input.text() ,
            "gender":self.gender_input.currentText(),
            "competition":self.tournament_input.currentText(),
            "paid": "yes" if self.paid_input.isChecked() else "no",
            "attendance": "yes" if self.attandence_input.isChecked() else "no",
            "nation":self.nation_input.text(),
            "club":self.club_input.text(),
            "recipe": "yes" if self.recipe_input.isChecked() else "no",
        }
        copy_check=db.find_one("Fencer",query={"firstname":self.first_name_input.text(),
            "lastname":self.last_name_input.text(),})
        if copy_check:
            add_dict["id"]=copy_check["id"]
        else:
            id_str =max(db.get_distinct_values("Fencer","id"))
            add_dict["id"]=str(int(id_str)+1)

        db.insert("Fencer",add_dict)
        self.cancel_button_clicked()

        