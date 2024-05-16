from PySide6.QtWidgets import  QHBoxLayout,QGridLayout, QPushButton,QWidget,QLabel,QLineEdit,QVBoxLayout
from PySide6.QtCore import Qt,QSize

from utility import clearLayout, connect_database

from drag_and_drop_ele import drag_on_me_button,fencer_button_class

def create_person_button(list):
    collection = connect_database()
    button_list=[]
    for button in list:
        if button[0].isChecked():
            query = {"competition":{"$regex": "^.*"+button[2]+".*$"}}
            fencer_list_cursor=collection.find(query)
            for fencer in fencer_list_cursor:
                for add_fencer in button_list:
                    if add_fencer.fencer["id"]==fencer["id"]:
                        break
                else:
                    fencer_button=fencer_button_class(fencer=fencer,x=None,y=None)
                    button_list.append(fencer_button)
    return button_list


class group_selection_wid(QWidget):
    def __init__(self,parent):
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
        self.set_group_amount_wid = QLineEdit("None")
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

        global_horizintal_layout.addWidget(menu_wid)
        global_horizintal_layout.addWidget(self.selection_wid)
        self.setLayout(global_horizintal_layout)

        self.setMinimumWidth(890)

    def value_changed(self):
        clearLayout(self.selection_wid.layout())

        self.fencer_button_list = create_person_button(self.par.wid_first.button_list)
        list_len=len(self.fencer_button_list)
        number_of_groups=int(self.set_group_amount_wid.text())
        people_per_group=int(self.set_group_size_wid.text())
        
        
        row=0
        self.selection_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        for i in range(number_of_groups):
            wid=QLabel(f"Gruppe {i+1}:")
            self.selection_layout.addWidget(wid,
                        row,
                        0,
                        1,6)
            row +=1
            for i in range(people_per_group):
                button=drag_on_me_button(x=row+ i//6,y=i%6)
                self.selection_layout.addWidget(button,
                        row+ i//6,
                        i%6)
            row += people_per_group // 6 + bool(people_per_group % 6)
        self.selection_layout.addWidget(QLabel("Nicht zugeordnet:"),row,0,1,6)
        row+=1

        for i in range(list_len):
            xcoord= i // 6
            ycoord= i  % 6
            self.selection_layout.addWidget(self.fencer_button_list[i],
                row+xcoord,
                ycoord )
            self.fencer_button_list[i].x=row+xcoord
            self.fencer_button_list[i].y=ycoord

