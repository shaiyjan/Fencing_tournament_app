from PySide6.QtWidgets import QGridLayout,QPushButton,QLabel
from PySide6.QtCore import Qt,QMimeData, QSize
from PySide6.QtGui import QDrag #type: ignore

class drag_on_me_button(QPushButton):
    def __init__(self,*args,x,y,**kwargs):
        super().__init__(*args,**kwargs)
        self.x=x
        self.y=y
        self.setFixedSize(QSize(100,60))
        self.setAcceptDrops(True)

    #copies data to mime on left-click and hold
    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton: #type: ignore
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            drag.exec(Qt.MoveAction) # type: ignore 

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        layout=self.parent().layout() #type:ignore 
        #layout: QGridLayout
        x,y = e.source().x,e.source().y
        x_self,y_self=self.x,self.y

        e.source().x=self.x
        e.source().y=self.y
        layout.addWidget(e.source(),self.x,self.y)

        self.x=x
        self.y=y
        layout.addWidget(self,x,y)
        
        e.accept()

class fencer_button_class(drag_on_me_button):
    def __init__(self,x,y,*,fencer):
        super().__init__(x=x,y=y)
        self.setFixedSize(QSize(100,60))
        self.fencer=fencer
        self.id=fencer["_id"]
        self.setLayout(QGridLayout())
        weapon, gender, age, sing_team = fencer["competition"].strip().split()
        self.layout().addWidget(QLabel(fencer["lastname"]),0,0,1,2) #type: ignore
        self.layout().addWidget(QLabel(fencer["firstname"]),1,0,1,2) #type: ignore
        self.layout().addWidget(QLabel(weapon),2,0) #type: ignore
        self.layout().addWidget(QLabel(age),2,1) #type: ignore
