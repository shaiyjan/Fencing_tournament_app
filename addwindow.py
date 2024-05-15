from PySide6.QtWidgets import QSizePolicy,QApplication ,QStackedLayout,QComboBox,QWidget,QPushButton ,QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit
from PySide6.QtCore import Qt, QSize, QMimeData

from PySide6.QtGui import QDrag #type: ignore

import pymongo
from ultility import clearLayout,new_matrix

def create_person_button(list):
    client = pymongo.MongoClient("localhost:27017")
    database = client.get_database("Tournament")
    collection = database.get_collection("Fencer")
    button_list=[]
    for button in list:
        if button[0].isChecked():
            query = {"competition":{"$regex": "^.*"+button[2]+".*$"}}
            fencer_list_cursor=collection.find(query)
            for fencer in fencer_list_cursor:
                fencer_button=fencer_button_class(fencer)
                button_list.append(fencer_button)
    return button_list

def create_query(button):
    reg_ex_1= button[2]
    query = {"competition":{"$regex": "^.*"+reg_ex_1+".*$"}}
    return query

class add_widget(QWidget):
    def __init__(self):
        super().__init__()
        self.ind=0

        self.super_layout = QStackedLayout()

        self.wid_first= general_button_group(self)
        self.wid_sec = group_selection_wid(self)

        self.super_layout.insertWidget(0,self.wid_first)
        self.super_layout.insertWidget(1,self.wid_sec)

    def next_click(self):
        self.ind +=1
        xpos = self.super_layout.currentWidget().x()
        ypos = self.super_layout.currentWidget().y()
        self.super_layout.setCurrentIndex(self.ind)
        self.super_layout.currentWidget().move(xpos,ypos)

        if self.ind == 1 :
            tz=int(self.wid_first.count_label.text())
            ga=int(self.wid_sec.set_group_size_wid.text())
            new_size = str(max(tz // ga + bool(tz%ga),1))
            self.wid_sec.set_group_amount_wid.setText(new_size)   

    def prev_clicked(self):
        self.ind -=1
        self.super_layout.setCurrentIndex(self.ind)

    def cancel_clicked(self):
        self.super_layout.currentWidget().close()    

    @property
    def ind(self):
        return self._ind

    @ind.setter
    def ind(self,num):
        self._ind = max(0,num)

class weapon_button_outer_l(QGridLayout):
    def __init__(self,competition:str, anzahl="NULL"):
        super().__init__()

        fencer_values=tuple(competition.split(" "))
        waffe = fencer_values[0]
        geschlecht = fencer_values[1]
        altersklasse = fencer_values[2]
        ein_team= fencer_values[3]

        self.addWidget(QLabel(waffe),0,0)
        self.addWidget(QLabel(geschlecht),0,1)
        self.addWidget(QLabel(altersklasse),1,0)
        self.addWidget(QLabel(anzahl),1,1)

class general_button_group(QWidget):
    def __init__(self,parent : add_widget):
        super().__init__()      
        self.setWindowTitle("Neuer Wettbewerb")

        self.par=parent
        #input tournament name - widged
        line_widget = QWidget()
        self.name_label =QLabel("Name:")
        self.set_name_label = QLineEdit("Wettbewerbsname")

        layout_upper_right=QHBoxLayout()
        layout_upper_right.addWidget(self.name_label)
        layout_upper_right.addWidget(self.set_name_label)

        line_widget.setLayout(layout_upper_right)

        #weapn/age/... buttons - widged
        group_widget = QWidget()
        self.button_list=create_weapon_buttons()
        
        layout_outer=QGridLayout()
        length=len(self.button_list)
        amount_rows = length//4 + bool(length%4)

        for row in range(amount_rows):
            for j in range(4):
                try:
                    button = self.button_list[row*4+j][0]
                    button.clicked.connect(self.weapon_button_clicked)
                except IndexError:
                    button = QWidget()
                    button.setFixedSize(QSize(100,200))
                layout_outer.addWidget(button, row , j)
        group_widget.setLayout(layout_outer)
        

        self.groupWidget=group_widget
        
        #menu - widget
        self.teilnehmerzahl="0"
        left_widget = QWidget()

        teilnehmerzahl_label = QLabel("Teilnehmerzahl:")
        self.count_label = QLabel(self.teilnehmerzahl)
        group_phase_widget = QLabel("Vorrunde:")
        self.set_group_widget = QComboBox()
        self.set_group_widget.addItems([ "Einfach", "Doppelt"] )
        
        modus_widged = QLabel("Tuniermodus:")
        self.set_modus_widget = QComboBox()
        self.set_modus_widget.addItems(
            ["K.O","K.O. + Hoffnungslauf","Vollständig","nach Vorrunde"]
        )
        
        next_button = QPushButton("Next")
        cancel_button= QPushButton("Cancel")

        next_button.clicked.connect(parent.next_click)
        cancel_button.clicked.connect(parent.cancel_clicked)

        layout_left = QVBoxLayout()
        layout_left.addWidget(next_button)
        layout_left.addWidget(teilnehmerzahl_label)
        layout_left.addWidget(self.count_label)
        layout_left.addWidget(group_phase_widget)
        layout_left.addWidget(self.set_group_widget)
        layout_left.addWidget(modus_widged)
        layout_left.addWidget(self.set_modus_widget)
        layout_left.addWidget(cancel_button)
        layout_left.addStretch()
        left_widget.setLayout(layout_left)


        left_widget.setFixedWidth(150)
 
        layout_inner =QVBoxLayout()

        layout_inner.addWidget(line_widget)
        layout_inner.addWidget(group_widget)
        layout_inner.addStretch()

        right_widget=QWidget()
        right_widget.setLayout(layout_inner)

        self.left_widget=left_widget
        
        layout_outer =QHBoxLayout()        
        layout_outer.addWidget(self.left_widget)
        layout_outer.addWidget(right_widget)
        self.setLayout(layout_outer)

    def weapon_button_clicked(self):
        part=0
        for button,weapon_counter,_ in self.button_list:
            if button.isChecked():
                part += weapon_counter
        self.count_label.setText(str(part))

def create_weapon_buttons():
    """ by pure data, not by competition """
    client = pymongo.MongoClient("localhost:27017")
    database = client.get_database("Tournament")
    collection = database.get_collection("Fencer")

    modal = []
    for fencer in collection.find():
        
        add_dict ={"competition":fencer["competition"].strip(),
                "teilnehmer":1
                }
        for dict_in in modal:
            if dict_in["competition"]== add_dict["competition"]:
                dict_in["teilnehmer"] +=1
                break
        else:
            modal.append(add_dict)

    button_list=[]
    for mod_dict in modal:
        weapon_button =QPushButton()
        weapon_button.setCheckable(True)
        weapon_button.setFixedSize(QSize(150,100))
        weapon_button.setLayout(weapon_button_outer_l(
            competition=mod_dict["competition"],
            anzahl=str(mod_dict["teilnehmer"])))
        button_list.append((weapon_button,mod_dict["teilnehmer"],mod_dict["competition"])) 

    return button_list
    
class group_selection_wid(QWidget):
    def __init__(self,parent : add_widget):
        super().__init__()
        self.par=parent

        global_horizintal_layout = QHBoxLayout()
        menu_wid = QWidget()
        

        menu_layout = QVBoxLayout()
        menu_next_button = QPushButton("Next")
        menu_prev_button = QPushButton("Previous")
        menu_cancel_button = QPushButton("Cancel")

        menu_next_button.clicked.connect(parent.next_click)
        menu_prev_button.clicked.connect(parent.prev_clicked)
        menu_cancel_button.clicked.connect(parent.cancel_clicked)

        menu_layout.addWidget(menu_next_button)

        menu_layout.addWidget(QLabel("Gruppengröße:"))

        self.group_size=6
        self.set_group_size_wid = QLineEdit(str(self.group_size))
        menu_layout.addWidget(self.set_group_size_wid)
        self.set_group_size_wid.textChanged.connect(self.value_changed)

        menu_layout.addWidget(QLabel("Gruppenanzahl:"))
        self.set_group_amount_wid = QLineEdit("1")
        self.set_group_amount_wid.textChanged.connect(self.value_changed)
        menu_layout.addWidget(self.set_group_amount_wid)
        
        menu_layout.addWidget(menu_prev_button)
        menu_layout.addWidget(menu_cancel_button)
        menu_layout.addStretch()
        menu_wid.setLayout(menu_layout)
        menu_wid.setFixedWidth(150)

        self.selection_wid = QWidget()
        self.selection_layout=QGridLayout()
        self.selection_wid.setLayout(self.selection_layout)
        #self.selection_layout=QVBoxLayout()

        global_horizintal_layout.addWidget(menu_wid)
        global_horizintal_layout.addWidget(self.selection_wid)
        self.setLayout(global_horizintal_layout)

        self.setMinimumWidth(882)
        #self.setMinimumHeight(410)

    def value_changed(self):
        clearLayout(self.selection_layout)

        self.fencer_button_list = create_person_button(self.par.wid_first.button_list)
        list_len=len(self.fencer_button_list)
        number_of_groups=int(self.set_group_amount_wid.text())
        #list_len//6+bool(list_len%int(self.set_group_amount_wid.text()))
        people_per_group=int(self.set_group_size_wid.text())
        
        layout=self.selection_layout

        row=0
        for i in range(number_of_groups):
            layout.addWidget(QLabel(f"Gruppe {i+1}:"),row,0,1,6,alignment=Qt.AlignmentFlag.AlignTop)
            row +=1
            for i in range(people_per_group):
                button=QPushButton()
                button.setFixedSize(QSize(100,60))
                layout.addWidget(button,row+ i//6, i%6,alignment=Qt.AlignmentFlag.AlignTop)
            row += people_per_group // 6 +1
        layout.addWidget(QLabel("Nicht zugeordnet:"),row,0,1,6)
        row+=1
        for i in range(list_len):
            xcoord= i // 6
            ycoord= i  % 6
            layout.addWidget(self.fencer_button_list[i],
                row+xcoord,
                ycoord,
                alignment=Qt.AlignmentFlag.AlignTop
                )
        
        self.updateGeometry()





class group_window_data:
    def __init__(self,i,group_member_label,group_member_layout):
        self.group_number = i
        self.label = group_member_label
        self.layout = group_member_layout
        self.members=[]

    def add_one(self,addition):
        self.members.append(addition)

    def add_many(self,list_in):
        self.members.extend(list_in)

    def del_on(self,removal):
        self.members.pop(removal)

class fencer_button_class(QPushButton):
    def __init__(self,fencer):
        super().__init__()
        self.setFixedSize(QSize(100,60))
        self.fencer=fencer
        self.id=fencer["_id"]
        layout=QGridLayout()
        weapon, gender, age, sing_team = fencer["competition"].strip().split()
        layout.addWidget(QLabel(fencer["lastname"]),0,0,1,2)
        layout.addWidget(QLabel(fencer["firstname"]),1,0,1,2)
        layout.addWidget(QLabel(weapon),2,0)
        layout.addWidget(QLabel(age),2,1)
        self.setLayout(layout)


