from PySide6.QtWidgets import (
    QStackedLayout,
    QWidget,
    QLabel,
    QMessageBox)


from add_window_select_persons import group_selection_wid
from add_window_select_comp import general_button_group

from drag_and_drop_ele import drag_on_me_button,fencer_button_class

from preliminary import preliminary

from dbmongo import db

def create_query(button):
    reg_ex_1= button[2]
    query = {"competition":{"$regex": "^.*"+reg_ex_1+".*$"}}
    return query

class add_widget(QWidget):
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.ind=0

        self.super_layout = QStackedLayout()

        self.wid_first= general_button_group(self)
        self.wid_sec = group_selection_wid(self)
        
        self.super_layout.insertWidget(0,self.wid_first)
        self.super_layout.insertWidget(1,self.wid_sec)

    def next_click(self):
        self.ind +=1
        xpos = self.super_layout.currentWidget().x()
        ypos = self.super_layout.currentWidget().y()
        self.super_layout.setCurrentIndex(self.ind)
        self.super_layout.currentWidget().move(xpos,ypos)

        if self.ind == 1 :
            if self.wid_sec.set_group_amount_wid.text()=="None":
                group_size = 6
                participants = int(self.wid_first.count_label.text().split("/")[0])
                new_size = str(max(participants // group_size + bool(participants%group_size),1))
                self.wid_sec.set_group_amount_wid.setText(new_size)   
        if self.ind == 2:
            if self.wid_first.set_name_label.text() in db.collection_names():
                self.ind=0
                self.super_layout.setCurrentIndex(0)

                msgbox=QMessageBox()
                msgbox.setWindowTitle("Name schon in Benutzung!")
                msgbox.setText("Der Wettbewerbsname wird schon verwendet. Bitte wähle einen neuen Namen!")
                msgbox.setStandardButtons(QMessageBox.Ok)
                msgbox.exec()
                return None

            preliminary_groups=[]
            group_number=-1
            for i in range(self.wid_sec.selection_layout.rowCount()):
                for j in range(6):
                    try:
                        wid_in_grid=self.wid_sec.selection_layout.itemAtPosition(i,j).widget()
                    except AttributeError:
                        break
                    if type(wid_in_grid)==QLabel: #type: ignore
                        preliminary_groups.append([])
                        group_number +=1
                        break
                    elif type(wid_in_grid)==drag_on_me_button: #type: ignore
                        continue
                    elif type(wid_in_grid)==fencer_button_class: #type: ignore
                        preliminary_groups[group_number].append(wid_in_grid.fencer)

            msgbox= QMessageBox()
            msgbox.setText("Do you want to finish the preliminary group setup?")
            msgbox.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
            ret = msgbox.exec()
            if ret==2048:
                name=self.wid_first.set_name_label.text()
                pre_mode=self.wid_first.set_group_widget.currentIndex()+1
                qual_mode=self.wid_first.set_modus_widget.currentText()
                self.create_prelimery(name,preliminary_groups,pre_mode,qual_mode)
            elif ret ==4194304 | ret ==8388608:
                self.prev_clicked()


                    
    def prev_clicked(self):
        self.ind -=1
        self.super_layout.setCurrentIndex(self.ind)
        xpos = self.super_layout.currentWidget().x()
        ypos = self.super_layout.currentWidget().y()
        self.super_layout.setCurrentIndex(self.ind)
        self.super_layout.currentWidget().move(xpos,ypos)

    def cancel_clicked(self):
        self.super_layout.currentWidget().close()
        self.deleteLater()  

    @property
    def ind(self):
        return self._ind

    @ind.setter
    def ind(self,num):
        self._ind = max(0,num)


    def create_prelimery(self,name,preliminary_groups,pre_mode,qual_mode):
        preliminary(name,
            preliminary_groups[0:-1],
            pre_mode,
            qual_mode)
        self.super_layout.currentWidget().close()
    


    

    

