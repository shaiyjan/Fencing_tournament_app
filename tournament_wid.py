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
from PySide6.QtGui import QColor, QPainter #type:ignore

from dbmongo import db

from preliminary import preliminary_by_preliminary
from elimination import create_elimination_round, next_match


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

        if phase_box_str.startswith("Vorrunde"):
            query={"type":"preliminary",
            "round": int(phase_box_str[phase_box_str.find(" ")+1:])}
        elif phase_box_str.startswith("K.O."):
            query={"type":"elimination",
                "round": int(phase_box_str[phase_box_str.find(" - ")+3:])}
        else:
            query={}

        matches=db.find_all(collection=self.name,query=query)
        
        for row in range(2,self.layout().rowCount()): #type: ignore
            for col in range(self.layout().columnCount()): #type: ignore
                try:
                    self.layout().itemAtPosition(row,col).widget().deleteLater() # type: ignore
                except:
                    ...

        for ind,match in enumerate(matches):
            if match["type"]=="preliminary":
                button = group_button(name=self.name,
                    parent=self,
                    match=match)
                button.setFixedHeight(150)
                button.setFixedWidth(200)
                self.layout().addWidget(button,2+ind // 4,ind % 4) #type: ignore
            elif match["type"]=="elimination":
                button = elimination_button(name=self.name,
                            parent=self,
                            match=match)
                button.setFixedHeight(150)
                button.setFixedWidth(200)
                self.layout().addWidget(button,2+ind // 4,ind % 4) #type: ignore

    def refresh(self):
        self.phase_box.clear()
   
        prel_list= db.get_distinct_values(collection=self.name,key="round",filter={"type":"preliminary"})    
        elim_list= db.get_distinct_values(collection=self.name,key="round",filter={"type":"elimination"})
        self.phase_box.addItems(
            set(["Vorrunde "+str(el) for el in prel_list])) #type: ignore

        self.phase_box.addItems(
            set(["K.O. - "+str(el) for el in elim_list])) #type:ignore

        self.phase_box.addItem("Alle")

        for row in range(2,self.layout().rowCount()): #type: ignore
            for col in range(self.layout().columnCount()): #type: ignore 
                try:
                    self.layout().itemAtPosition(row,col).deleteLater() #type: ignore
                except:
                    ...

class elimination_button(QPushButton):
    def __init__(self,name,parent,match):
        super().__init__()
        self.par=parent
        self.name=name
        self.match=match
        self.setLayout(QGridLayout())
        self.clicked.connect(self.click)
        self.layout().addLayout(QHBoxLayout(),0,0,1,2) #type: ignore
        self.color= Qt.green if match["finished"] else Qt.red #type: ignore
        self.layout().itemAtPosition(0,0).addWidget(LightWidget(self.color)) #type:ignore
        self.layout().itemAtPosition(0,0).addWidget(    #type:ignore
                        QLabel(name+" Runde: " + str(match["round"])))
        self.layout().addWidget(QLabel(str(match["fencer1"]["lastname"])),1,0) #type:ignore
        self.layout().addWidget(QLabel(str(match["score1"])),1,1) #type:ignore
        if match["fencer2"]:
            self.layout().addWidget(QLabel(str(match["fencer2"]["lastname"])),2,0) #type:ignore
            self.layout().addWidget(QLabel(str(match["score2"])),2,1) #type:ignore
        else:
            self.layout().addWidget(QLabel("None"),2,0)  #type:ignore

    def click(self):
        wid=elim_insertion_widget(
            parent=self,
            match=self.match,
            name=self.name
            )
        wid.show()

class elim_insertion_widget(QTableWidget):
    def __init__(self,parent,match,name):
        super().__init__()
        self.par=parent
        self.id=match["_id"]
        self.name=name
        self.match=match

        self.table= QTableWidget()

        self.table.setRowCount(3)
        self.table.setColumnCount(3)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)

        if match["finished"]==True:
            self.table.setItem(1,2,QTableWidgetItem())
            self.table.setItem(2,2,QTableWidgetItem())
            self.table.item(1,2).setText(str(match["score1"]))
            self.table.item(2,2).setText(str(match["score2"]))

        

        self.table.setItem(0,0,QTableWidgetItem())
        self.table.item(0,0).setFlags(Qt.ItemFlag.ItemIsSelectable)
        self.table.item(0,0).setText(self.name)
        self.table.setItem(0,1,QTableWidgetItem())
        self.table.item(0,1).setFlags(Qt.ItemFlag.ItemIsSelectable)
        self.table.item(0,1).setText(str("Runde: "+ str(match["round"])))
        self.table.setItem(0,2,QTableWidgetItem())
        self.table.item(0,2).setFlags(Qt.ItemFlag.ItemIsSelectable)
        self.table.item(0,2).setText(str("Platzierung:"+str(match["placing"])))
        self.table.setItem(1,0,QTableWidgetItem())
        self.table.setSpan(1,0,1,2)
        self.table.item(1,0).setFlags(Qt.ItemFlag.ItemIsSelectable)
        self.table.item(1,0).setText(match["fencer1"]["lastname"]+","+match["fencer1"]["firstname"])
        self.table.setItem(2,0,QTableWidgetItem())
        self.table.setSpan(2,0,1,2)
        self.table.item(2,0).setFlags(Qt.ItemFlag.ItemIsSelectable)
        if match["fencer2"]:
            self.table.item(2,0).setText(match["fencer2"]["lastname"]+","+match["fencer2"]["firstname"])

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

    def submit_clicked(self):
        query = {"_id": self.id}

        if self.table.item(1,2).text() and self.table.item(2,2).text():
            update={"score1":self.table.item(1,2).text(),
                    "score2":self.table.item(2,2).text(),
                    "finished":True}

            db.update_one(collection=self.name,query=query,update_dict=update)

            query= {"round":self.match["round"],
                    "placing":
                            min((self.match["round"]>>1)-1-self.match["placing"],
                                    self.match["placing"])}
            other_match=db.find_one(collection=self.name,
                                query=query)
            if self.match["round"]!=2 and other_match["finished"]==True:
                next_match(self.name,self.match,other_match)

class group_button(QPushButton):
    def __init__(self,name,parent,match):
        super().__init__(parent=parent)
        self.round=round
        self.name=name 
        self.match=match
        self.round=match["round"]
        self.round_name="Vorrunde "+ str(match["round"])
        self.bson_id=match["_id"]
        self.participants=match["group"]
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QWidget())
        self.layout().itemAt(0).widget().setLayout(QHBoxLayout())
        
        
        self.color= Qt.green if match["finished"] else Qt.red #type: ignore
        self.layout().itemAt(0).widget().layout().addWidget(LightWidget(self.color))
        self.layout().itemAt(0).widget().layout().addWidget(QLabel(self.round_name))
        self.layout().itemAt(0).widget().layout().addStretch() #type:ignore

        self.layout().addWidget(QLabel("Gruppe: " + str(match["group_number"])))
        
        for el in self.participants:
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
                    create_elimination_round(tournament=self.name)
                    self.par.parent().refresh()

            else:
                return None
            
class LightWidget(QWidget):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.heightForWidth(True)
        self.setFixedWidth(10)
        self.setFixedHeight(10)

    def paintEvent(self, e):
        with QPainter(self) as painter:
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(self.color)
            painter.drawEllipse(0, 0, self.width(), self.height())