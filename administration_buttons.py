from PySide6.QtWidgets import QCheckBox
import pymongo

class admin_button(QCheckBox):
    client = pymongo.MongoClient("localhost:27017")
    def __init__(self):
        super().__init__()

class attandance_box(admin_button):
    def __init__(self, id,checked):
        super().__init__()
        self.id=id
        self.setChecked(checked)
        self.checkStateChanged.connect(lambda : box_update(self.id,self.isChecked(),"attandence"))

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
    client = pymongo.MongoClient("localhost:27017")
    collection=client.get_database("Tournament").get_collection("Fencer")
    collection.update_one({"_id": id}, {"$set":{ field: "yes" if checked_bool else "no"}})