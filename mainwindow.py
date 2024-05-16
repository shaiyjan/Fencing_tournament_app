from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow , QToolBar, QPushButton

from widget import Widget
from administration_widget import administation_layout

from screeninfo import screeninfo

screenheight=screeninfo.get_monitors()[0].height
screenwidth=screeninfo.get_monitors()[0].width

menu_toggle_size=146

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Turnier-Organisator")
        self.setMinimumSize(QSize(900,480))

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&Menu")
        quit_action = file_menu.addAction("Quit")
        quit_action.triggered.connect(self.quit_app)

        toolbar =QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        toolbar.addAction(quit_action)

        admin_menu_button = QPushButton("Administration")
        left_menu_toggle_button = QPushButton("Toggle Menu")
    
        admin_menu_button.clicked.connect(self.button_admin_clicked)
        left_menu_toggle_button.clicked.connect(self.button_menu_toggle_clicked)

        toolbar.addWidget(left_menu_toggle_button)
        toolbar.addWidget(admin_menu_button)

        self.Wid = Widget(self,menu_toggle_size)
        
        self.setCentralWidget(self.Wid)
        # button2.setDisabled(self.button_checked)

    def button_admin_clicked(self):
        self.Wid.fill_widget.setLayout(administation_layout())
        
    def button_menu_toggle_clicked(self):
        global menu_toggle_size 
        wid_to_toggle = self.Wid.menu
        if wid_to_toggle.width()==0:
            wid_to_toggle.setFixedWidth(menu_toggle_size)
        else:
            wid_to_toggle.setFixedWidth(0)


    def quit_app(self):
        self.app.quit()