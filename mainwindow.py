from PySide6.QtCore import QSize

from PySide6.QtWidgets import (
    QMainWindow,
    QToolBar,
    QScrollArea,
    QFileDialog, 
    QWidget,
    QPushButton, 
    QVBoxLayout, 
    QHBoxLayout,
    QStackedWidget)

from administration_widget import administation_layout
from delayed_widget import delayed_widget,delete_widget
from addwindow import add_widget

from screeninfo import screeninfo
from dbmongo import db

from tournament_wid import tournament_wid

import csv

screenheight=screeninfo.get_monitors()[0].height
screenwidth=screeninfo.get_monitors()[0].width

menu_toggle_size=146

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Turnier-Organisator")
        self.setMinimumSize(QSize(800,300))

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&Menu")
        refresh_action = menu_bar.addAction("Refresh")
        refresh_action.triggered.connect(self.update_tournament_sheets)
        quit_action = file_menu.addAction("Quit")

        quit_action.triggered.connect(self.quit_app)

        self.toolbar =QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)
        self.toolbar.addAction(quit_action)

        admin_menu_button = self.toolbar.addAction("Administration")
        left_menu_toggle_button = self.toolbar.addAction("Toggle Menu") 
    
        admin_menu_button.triggered.connect(self.button_admin_clicked)  
        left_menu_toggle_button.triggered.connect(self.button_menu_toggle_clicked)
        self.toolbar.addSeparator()

        self.main_wid = QWidget()
        self.main_wid.setLayout(QHBoxLayout())
        self.menu =LWidget(self)
        self.menu.setFixedWidth(menu_toggle_size)
        self.main_wid.layout().addWidget(self.menu)

        scroll_area=QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.fill_widget = QStackedWidget()
        scroll_area.setWidget(self.fill_widget)
        scroll_area.setStyleSheet("background-color: light gray")

        self.fill_widget.addWidget(QWidget())
        self.fill_widget.widget(0).setLayout(administation_layout())

        self.main_wid.layout().addWidget(scroll_area)

        self.setCentralWidget(self.main_wid)

        self.tournament_actions=[]

    def button_admin_clicked(self):
        self.fill_widget.setCurrentIndex(0)
        
    def button_menu_toggle_clicked(self):
        global menu_toggle_size 
        wid_to_toggle = self.menu
        if wid_to_toggle.width()==0:
            wid_to_toggle.setFixedWidth(menu_toggle_size)
        else:
            wid_to_toggle.setFixedWidth(0)

    def quit_app(self):
        self.app.quit()

    def build_lambda(self,ind):
            return lambda : (
                self.fill_widget.setCurrentIndex(ind+1),
                self.fill_widget.currentWidget().refresh()
            )

    def update_tournament_sheets(self):
        while self.tournament_actions:
            self.toolbar.removeAction(self.tournament_actions.pop())

        tournament_names= db.collection_names()
        tournament_names.remove("Fencer")
        tournament_names.remove("Organisation")
        self.tournament_actions=[]
        for ind in range(len(tournament_names)):
            tour=tournament_names[ind]
            tourn_wid=tournament_wid(name=tour)
            self.fill_widget.insertWidget(ind+1,tourn_wid)
            action=self.toolbar.addAction(tour)
            action.triggered.connect(self.build_lambda(ind))
            self.tournament_actions.append((action))

class LWidget(QWidget):
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.setWindowTitle("QMessageBox")

        button_add=QPushButton("Neuer Wettbewerb")
        button_read=QPushButton("Read von CSV")
        button_delayed=QPushButton("Delayed Participant")
        button_drop=QPushButton("Wettbewerb löschen")

        button_add.clicked.connect(lambda : add_widget(parent))
        button_read.clicked.connect(self.button_read_clicked)
        button_delayed.clicked.connect(self.button_delayed_participant_clicked)
        button_drop.clicked.connect(self.delete_tournament)

        layout= QVBoxLayout()
        layout.addWidget(button_add)
        layout.addWidget(button_read)
        layout.addWidget(button_delayed)
        layout.addWidget(button_drop)
        layout.addWidget(QWidget())
        layout.addStretch()
        self.setLayout(layout)

    def button_read_clicked(self):
        filebox= QFileDialog()
        filebox.exec()
        selected_files = filebox.selectedFiles()
        read_to_db(selected_files)

    def button_delayed_participant_clicked(self):
        global delay_window 
        delay_window = delayed_widget()
        delay_window.show()

    def delete_tournament(self):
        global delete_window
        delete_window = delete_widget()
        delete_window.show()
        
def read_to_db(files):
    list_of_dict=[]
    for file in files:
        with open(file,encoding="UTF-16 LE") as f:
            reader = csv.DictReader(f,delimiter=";")
            for line in reader:
                line['recipe']="no"
                line['attendance']="no"
                line['attest']="no"
                line['id'] = line['\ufeffid']
                line['note'] =""
                del line['\ufeffid']
                list_of_dict.append(line)

    db.insert("Fencer",list_of_dict)