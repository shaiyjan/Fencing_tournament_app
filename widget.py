from PySide6.QtWidgets import QGridLayout,QFileDialog, QWidget,QPushButton, QVBoxLayout, QHBoxLayout

from addwindow import add_widget
from delayed_widget import delayed_widget

import csv
import pymongo

from utility import connect_database

class Widget(QWidget):
    def __init__(self,parent,menu_toggle_size):
        super().__init__(parent)
        layout= QHBoxLayout()
        self.menu =LWidget()
        self.menu.setFixedWidth(menu_toggle_size)
        layout.addWidget(self.menu)
        self.fill_widget = QWidget()
        layout.addWidget(self.fill_widget)
        self.setLayout(layout)

class LWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QMessageBox")

        button_add=QPushButton("Neuer Wettbewerb")
        button_read=QPushButton("Read von CSV")
        button_delayed=QPushButton("Delayed Participant")

        button_add.clicked.connect(self.button_add_clicked)
        button_read.clicked.connect(self.button_read_clicked)
        button_delayed.clicked.connect(self.button_delayed_participant_clicked)

        layout= QVBoxLayout()
        layout.addWidget(button_add)
        layout.addWidget(button_read)
        layout.addWidget(button_delayed)
        layout.addWidget(QWidget())
        layout.addStretch()
        self.setLayout(layout)

    def button_add_clicked(self):
        global wid
        wid=add_widget()

    def button_read_clicked(self):
        filebox= QFileDialog()
        filebox.exec()
        selected_files = filebox.selectedFiles()
        read_to_db(selected_files)

    def button_delayed_participant_clicked(self):
        global delay_window 
        delay_window =  delayed_widget()
        delay_window.show()

def read_to_db(files):


    list_of_dict=[]
    for file in files:
        with open(file,encoding="UTF-16 LE") as f:
            reader = csv.DictReader(f,delimiter=";")
            for line in reader:
                line["recipe"]="no"
                line["attandence"]="no"
                line["attest"]="no"
                line['id'] = line['\ufeffid']
                del line['\ufeffid']
                list_of_dict.append(line)

    collection = connect_database()
    collection.insert_many(list_of_dict)
