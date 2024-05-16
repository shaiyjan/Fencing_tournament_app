from PySide6.QtWidgets import QStackedLayout,QWidget, QLabel, QLineEdit
from PySide6.QtCore import QSize

from add_window_select_persons import group_selection_wid
from add_window_select_comp import general_button_group

from drag_and_drop_ele import drag_on_me_button,fencer_button_class


from utility import clearLayout ,connect_database





def create_query(button):
    reg_ex_1= button[2]
    query = {"competition":{"$regex": "^.*"+reg_ex_1+".*$"}}
    return query

class add_widget(QWidget):
    def __init__(self):
        super().__init__()
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
                participants = int(self.wid_first.count_label.text())
                new_size = str(max(participants // group_size + bool(participants%group_size),1))
                self.wid_sec.set_group_amount_wid.setText(new_size)   
        if self.ind == 2:
            preliminary_groups=[]
            group_number=-1
            for i in range(self.wid_sec.selection_layout.rowCount()):
                for j in range(6):
                    try:
                        wid_in_grid=self.wid_sec.selection_layout.itemAtPosition(i,j).widget()
                    except AttributeError:
                        break
                    if type(wid_in_grid)==QLabel:
                        preliminary_groups.append([])
                        group_number +=1
                        break
                    elif type(wid_in_grid)==drag_on_me_button:
                        continue
                    elif type(wid_in_grid)==fencer_button_class:
                        preliminary_groups[group_number].append(wid_in_grid.id)
            for group in preliminary_groups:
                print(group)

                        

             
                    
    def prev_clicked(self):
        self.ind -=1
        self.super_layout.setCurrentIndex(self.ind)
        xpos = self.super_layout.currentWidget().x()
        ypos = self.super_layout.currentWidget().y()
        self.super_layout.setCurrentIndex(self.ind)
        self.super_layout.currentWidget().move(xpos,ypos)

    def cancel_clicked(self):
        self.super_layout.currentWidget().close()    

    @property
    def ind(self):
        return self._ind

    @ind.setter
    def ind(self,num):
        self._ind = max(0,num)


    


    

    

