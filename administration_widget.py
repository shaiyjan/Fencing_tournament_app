from PySide6.QtWidgets import (
    QLayout,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QComboBox,
    QWidget,
    QLabel,
    QLineEdit,
    QStackedWidget,
    QSizePolicy,
    QTextEdit)
from PySide6.QtCore import Qt

from administration_buttons import (
    paid_box,
    recipe_box,
    attest_box,
    attendance_box,
    referee_box)

from dbmongo import db

from utility import calculate_age


def read_collection(key,value):
    
    if value ==".+":
        reg_ex_str=".+"
    else:
        reg_ex_str=""
        for letter in value:
            reg_ex_str += "("+letter.upper()+"|"+letter.lower()+ ")"


    db_ret=db.find_all("Fencer",query={key:{"$regex": "^.*"+reg_ex_str+".*$"}})
    
    return db_ret

class administation_layout(QGridLayout):
    def __init__(self):
        super().__init__()

        key_names=["Nachname","Vorname","Verein","Anwesend","Bezahlt","Wettbewerb","Kampfrichter ","Notiz"]
        self.selected_keys= ["lastname","firstname","club","attendance","paid","competition","referee","note"]
        self.setSizeConstraint(QLayout.SetMinimumSize) #type: ignore
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)  
        
        search_label = QLabel("Suche")

        self.search_input= QStackedWidget()
        self.search_input.setSizePolicy(QSizePolicy.Policy.Minimum,QSizePolicy.Policy.Fixed)
        self.search_input.addWidget(QLineEdit())

        self.search_key = QComboBox()
        self.search_key.currentIndexChanged.connect(self.select_search_widget)
        self.search_key.addItems(key_names)
        search_submit_button = QPushButton("Suche")
        
        self.yes_no_box=QComboBox()
        self.yes_no_box.addItems(["Ja","Nein"])
        self.tournament_box=QComboBox()
        self.search_input.addWidget(self.yes_no_box)
        self.search_input.addWidget(self.tournament_box)

        search_layout=QHBoxLayout()
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_key)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_submit_button)

        search_submit_button.clicked.connect(self.button_submit_clicked)
        
        self.addLayout(search_layout,0,0,1,7)
        
        self.addWidget(QLabel("Nachname, Vorname"),1,0)
        self.addWidget(QLabel("Verein"),1,1)
        self.addWidget(QLabel("Wettbewerb"),1,2)
        self.addWidget(QLabel("Anwesend"),1,3)
        self.addWidget(QLabel("Bezahlt"),1,4)
        self.addWidget(QLabel("Quittung"),1,5)
        self.addWidget(QLabel("Attest"),1,6)
        self.addWidget(QLabel("Kampfrichter"),1,7)
        self.addWidget(QLabel("Notiz"),1,8)

    def select_search_widget(self):
        if self.search_key.currentIndex() in [0,1,2,77]:
            self.search_input.setCurrentIndex(0) #
        elif self.search_key.currentIndex() in [3,4,6]:
            self.search_input.setCurrentIndex(1)
        elif self.search_key.currentIndex()==5:
            comp_list=db.get_distinct_values("Fencer","competition")
            self.search_input.setCurrentIndex(2)
            self.tournament_box.clear()
            self.tournament_box.addItems(comp_list)


    def button_submit_clicked(self):
        for row in range(2,self.rowCount()):
            for col in range(self.columnCount()):
                if self.itemAtPosition(row,col) and self.itemAtPosition(row,col).widget():
                    self.itemAtPosition(row,col).widget().deleteLater()

        key=self.selected_keys[self.search_key.currentIndex()]

        if self.search_key.currentIndex()==7:
            if self.search_input.currentWidget().text():
                value=self.search_input.currentWidget().text()
            else:
                value=".+"
        
        elif type(self.search_input.currentWidget()) == QLineEdit: #type: ignore
            value= self.search_input.currentWidget().text()
        elif type(self.search_input.currentWidget()) == QComboBox: #type:ignore 
            value=self.search_input.currentWidget().currentText()
            if value=="Ja":
                value="yes"
            elif value=="Nein":
                value="no"

        db_ret=read_collection(key=key,value = value) #type: ignore
        
        db_ret=sorted(db_ret,key=lambda x : x ["lastname"])
        counter=2
        for it in db_ret:
            id=it["_id"]
            
            age=calculate_age(*it["dateofbirth"].strip().split("."))
            if age <18:
                attes_wid=attest_box(id,True if it["attest"]=="yes" else False)
            else:
                attes_wid=QWidget()
            
            self.addWidget(
                QLabel(f"{it['lastname'].capitalize()}, {it['firstname']}"),
                counter,0)
            self.addWidget(
                QLabel(f"{it['club']}"),
                counter,1)
            self.addWidget(
                QLabel(f"{it['competition']}"),
                counter,2)
            self.addWidget(
                attendance_box(id,True if it["attendance"]=="yes" else False),
                counter,3)
            self.addWidget(
                paid_box(id,True if it["paid"]=="yes" else False)
                ,counter,4)
            self.addWidget(
                recipe_box(id,True if it["recipe"]=="yes" else False),
                counter,5)
            self.addWidget(
                attes_wid,
                counter,6)
            self.addWidget(
                referee_box(id,True if it["referee"]=="yes" else False),
                counter,7)
            self.addWidget(
                note_button(id),
                counter,8)

            counter+=1

        for row in range(counter):
            try:
                self.setRowStretch(row,0)
            except:
                ...

        for col in range(self.columnCount()):
            try:
                self.setColumnStretch(col,0)
            except:
                ...
        
class note_button(QPushButton):
    def __init__(self,id):
        super().__init__()
        self.id=id
        self.setText("Notiz")
        self.clicked.connect(self.note_button_clicked)

    def note_button_clicked(self):
        global x
        x=note_widget(id=self.id)
        x.show()
        
class note_widget(QWidget):
    def __init__(self,id):
        super().__init__()

        self.id=id
        fencer= db.find_one(
            collection="Fencer",
            query={"_id":id})

        self.setLayout(QGridLayout())
        text_widget= QTextEdit()
        text_widget.setText(fencer["note"])
        submit_button = QPushButton("Submit")#
        submit_button.clicked.connect(lambda: self.submit_clicked(text_widget.toPlainText()))
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)

        self.layout().addWidget(submit_button,0,0) #type: ignore
        self.layout().addWidget(cancel_button,1,0)  #type: ignore
        self.layout().addWidget(text_widget,0,1,1,3) #type: ignore


    def submit_clicked(self,string):
        db.update_one(collection="Fencer",
            query={"_id":self.id},
            update_dict={"note":string})
        self.close()