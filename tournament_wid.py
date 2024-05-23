from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QComboBox,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
    QLayout,
    QTableWidgetItem)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from dbmongo import db

from preliminary import preliminary_by_preliminary
from elimination import create_elimination_round


class tournament_wid(QWidget):
    def __init__(self,name):
        super().__init__()
        self.name=name
        self.setLayout(QGridLayout())
        self.layout().setSizeConstraint(QLayout.SetMinimumSize) #type: ignore
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)  

        name_label=QLabel("Wettbewerbsname: "+name)
        phase_label=QLabel("Phase:")
        self.phase_box=QComboBox()

        status_label =QLabel("Status:")
        status_box =QComboBox()
        status_box.addItems(["Ongoing","Alle"])

        self.layout().addWidget(name_label,0,0,1,6) #type: ignore
        header = QHBoxLayout()
        header.addWidget(phase_label)
        header.addWidget(self.phase_box)
        header.addWidget(status_label)
        header.addWidget(status_box)
        header.addStretch()
        self.layout().addLayout(header,1,0,1,6) #type: ignore

        status_box.currentIndexChanged.connect(self.create_buttons)
        self.phase_box.currentIndexChanged.connect(self.create_buttons)

    def create_buttons(self):

        name_list=db.get_distinct_values(self.name,"type")
        name_labels=[]
        for name in name_list:
            label=QLabel(name)
            name_labels.append(label)

        phase_box_str=self.phase_box.currentText()
        if phase_box_str=="Alle":
            query={}
        else:
            if phase_box_str.startswith("Vorrunde"):
                query={"type":"preliminary","round": int(phase_box_str[9:])}
            elif phase_box_str.startswith("K.O."):
                query={"type":"eliminarion","round": int(phase_box_str[4:])}

        matches=db.find_all(collection=self.name,query=query) #type: ignore
        
        for row in range(2,self.layout().rowCount()): #type: ignore
            for col in range(self.layout().columnCount()): #type: ignore
                try:
                    self.layout().itemAtPosition(row,col).widget().deleteLater() # type: ignore
                except:
                    ...

        for ind,match in enumerate(matches):
            if match["type"]=="preliminary":
                participants = [el for el in match['group']]
                button = group_button(name=self.name,
                    parent=self,
                    group_number=match["group_number"], #not right!
                    group_id_bson=match["_id"],
                    participants=participants,
                    round=match["round"])
                button.setFixedHeight(150)
                button.setFixedWidth(200)
                self.layout().addWidget(button,2+ind // 4,ind % 4) #type: ignore


    def refresh(self):
        self.phase_box.clear()

        prel_list = [*db.find_all(collection=self.name,query={"type":"preliminary"})]
        elim_list = [*db.find_all(collection=self.name,query={"type":"elimination"})]       

        self.phase_box.addItems(
            set(["Vorrunde "+str(el["round"]) for el in prel_list])) #type: ignore
        self.phase_box.addItems(
            set(["K.O. - "+str(el["round"]) for el in elim_list])) #type: ignore
        self.phase_box.addItem("Alle")

        for row in range(2,self.layout().rowCount()): #type: ignore
            for col in range(self.layout().columnCount()): #type: ignore 
                try:
                    self.layout().itemAtPosition(row,col).deleteLater() #type: ignore
                except:
                    ...

class group_button(QPushButton):
    def __init__(self,name,parent,group_number,group_id_bson,participants:list,round):
        super().__init__(parent=parent)
        self.round=round
        self.name=name 
        self.round_name="Vorrunde "+ str(round)
        self.bson_id=group_id_bson
        self.participants=participants
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel(self.round_name))
        self.layout().addWidget(QLabel("Gruppe: " + str(group_number)))
        
        for el in participants:
            self.layout().addWidget(QLabel(el["lastname"].capitalize() +","+el["firstname"].capitalize()))
        self.clicked.connect(self.click)
        
    def click(self):
        wid=group_insertion_widget(
            parent=self,
            participants=self.participants,
            name=self.name,
            id=self.bson_id,
            round=self.round)
        wid.show()

class group_insertion_widget(QWidget):
    def __init__(self,parent,participants,name,id,round):
        super().__init__()
        self.par=parent
        self.round=round
        self.id=id
        self.name=name
        self.participants = participants

        group_size=len(participants)

        self.table= QTableWidget()

        self.table.setRowCount(group_size+1)
        self.table.setColumnCount(group_size+8)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)

        self.table.setItem(0,0,QTableWidgetItem())
        self.table.item(0,0).setFlags(Qt.ItemFlag.ItemIsSelectable)
        self.table.item(0,0).setText("Name")

        field_list=["Siege",
            "Gefechte",
            "Quote",
            "Treffer",
            "Getroffen",
            "Differenz",
            "Platzierung"]
        for i in range(7):
            self.table.setItem(0,group_size+i+1,QTableWidgetItem())
            self.table.item(0,group_size+i+1).setText(field_list[i])
            self.table.item(0,group_size+i+1).setFlags(Qt.ItemFlag.ItemIsSelectable)
            self.table.setColumnWidth(group_size+i+1,30)
            
            for j in range(1,group_size+1):
                self.table.setItem(j,group_size+i+1,QTableWidgetItem())
                self.table.item(j,group_size+i+1).setFlags(
                                Qt.ItemFlag.ItemIsSelectable)

        for i in range(group_size):
            self.table.setItem(i+1,0,QTableWidgetItem())
            self.table.setItem(i+1,i+1,QTableWidgetItem())
            self.table.setItem(0,i+1,QTableWidgetItem())
            self.table.item(i+1,0).setText(
                    participants[i]["lastname"]+","+participants[i]["firstname"])
            self.table.item(i+1,0).setFlags(Qt.ItemFlag.ItemIsSelectable)
            self.table.item(i+1,i+1).setText("0")
            self.table.item(i+1,i+1).setFlags(Qt.ItemFlag.ItemIsSelectable)
            self.table.item(i+1,i+1).setBackground(QColor("grey"))
            self.table.item(0,i+1).setText(str(i+1))
            self.table.item(0,i+1).setFlags(Qt.ItemFlag.ItemIsSelectable)
            self.table.setColumnWidth(i+1,10)


        self.table.cellChanged.connect(self.val_changed)
        self.table.itemChanged.connect(self.val_changed)

        submit = QPushButton("Submit")
        cancel = QPushButton("Cancel")
        button_wid=QWidget()
        button_wid.setLayout(QVBoxLayout())
        button_wid.layout().addWidget(submit)
        button_wid.layout().addWidget(cancel)
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(button_wid)
        self.layout().addWidget(self.table)

        submit.clicked.connect(self.submit_clicked)
        cancel.clicked.connect(lambda : self.close())

        db_dict = db.find_one(name,query={"_id":self.id})
        if table:=db_dict["table"] :
            for row in range(1,self.table.rowCount()):
                for col in range(1,self.table.columnCount()):
                    if row!= col and 1<= row <= group_size:
                        self.table.setItem(row,col,QTableWidgetItem())
                    self.table.item(row,col).setText(table[row-1][col-1])

    def val_changed(self):
        #exclude logic to preliminary?
        check=True
        group_size=len(self.participants)
        for i in range(1,group_size+1):
            for j in range(1,group_size+1):
                if not (self.table.item(i,j) and self.table.item(i,j).text()):
                    check=False
                    break
            if check==False:
                break
        else:
            for i in range(1,group_size+1):
                wins=0
                matches=-1
                hits_given=0
                hits_received=0
                for j in range(1,group_size+1):
                    hit_g=int(self.table.item(i,j).text())
                    hit_r=int(self.table.item(j,i).text())
                    wins += 1 if hit_g>hit_r else 0
                    matches +=1 if self.table.item(i,j).text() else 0
                    hits_given += hit_g if hit_g else 0
                    hits_received += hit_r if hit_r else 0
                self.table.item(i,group_size+1).setText(str(wins))
                self.table.item(i,group_size+2).setText(str(matches))
                self.table.item(i,group_size+3).setText(f"{wins/matches:.2%}")
                self.table.item(i,group_size+4).setText(str(hits_given))
                self.table.item(i,group_size+5).setText(str(hits_received))
                self.table.item(i,group_size+6).setText(str(hits_given-hits_received))
            ind=[*range(1,group_size+1)]
            ind.sort(
                key=lambda x: (
                    int(self.table.item(x,group_size+1).text()),
                    int(self.table.item(x,group_size+6).text())
                            ),reverse=True)
            for i in range(1,group_size+1):
                self.table.item(ind[i-1],group_size+7).setText(str(i))
           
    def submit_clicked(self):
        query = {"_id": self.id}
        table=[]
        for row in range(1,self.table.rowCount()):
            table_inner=[]
            for column in range(1,self.table.columnCount()):
                table_inner.append(self.table.item(row,column).text())
            table.append(table_inner)

        update ={"table":table}

        for i in range(len(table)):
            if not table[i][-1]:
                break
        else:
            update["finished"]=True #type: ignore

        db.update_one(collection=self.name,query=query,update_dict=update)
        self.close()

        if update["finished"]==True:
            values=db.get_distinct_values(collection=self.name,key="finished")
            if all(values):
                if self.round != 1:
                    preliminary_by_preliminary(self.name,round=self.round)
                    self.par.parent().refresh()
                if self.round ==1:
                    create_elimination_round()

            else:
                return None
            