from PySide6.QtWidgets import QCheckBox



from dbmongo import db

class admin_button(QCheckBox):
    def __init__(self):
        super().__init__()

class attendance_box(admin_button):
    def __init__(self, id,checked):
        super().__init__()
        self.id=id
        self.setChecked(checked)
        self.checkStateChanged.connect(lambda : box_update(self.id,self.isChecked(),"attendance"))

class paid_box(admin_button):
    def __init__(self, id,checked):
        super().__init__()
        self.id=id
        self.setChecked(checked)
        self.checkStateChanged.connect(lambda : box_update(self.id,self.isChecked(),"paid"))

class recipe_box(admin_button):
    def __init__(self, id,checked):
        super().__init__()
        self.id = id
        self.setChecked(checked)
        self.checkStateChanged.connect(lambda : box_update(self.id,self.isChecked(),"recipe"))

class attest_box(admin_button):
    def __init__(self, id,checked):
        super().__init__()
        self.id=id
        self.setChecked(checked)
        self.checkStateChanged.connect(lambda : box_update(self.id,self.isChecked(),"attest"))
    

def box_update(id,checked_bool,field):
    db.update_one("Fencer",query={"_id": id},update_dict={ field: "yes" if checked_bool else "no"})
