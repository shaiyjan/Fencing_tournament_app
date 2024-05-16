from PySide6.QtWidgets import QComboBox,QWidget,QLabel,QLineEdit,QPushButton,QGridLayout,QVBoxLayout,QHBoxLayout
from PySide6.QtCore import QSize

from utility import connect_database


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
    def __init__(self,parent):
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
        participant_ids=set()
        for button,comp_participants,_ in self.button_list:
            if button.isChecked():
                participant_ids.update(comp_participants)
        self.count_label.setText(str(len(participant_ids)))

def create_weapon_buttons():
    """ by pure data, not by competition """
    collection = connect_database()

    modal = []
    for fencer in collection.find():
        
        add_dict ={"competition":fencer["competition"].strip(),
                "teilnehmer":[fencer["id"]]
                }
        for dict_in in modal:
            if dict_in["competition"]== add_dict["competition"]:
                dict_in["teilnehmer"].append(fencer["id"])
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
            anzahl=str(len(mod_dict["teilnehmer"]))))
        button_list.append((weapon_button,mod_dict["teilnehmer"],mod_dict["competition"])) 

    return button_list
    

