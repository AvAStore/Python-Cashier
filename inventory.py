import DB
from PySide6.QtWidgets import QMainWindow,QWidget,QMessageBox


def recommend(self):
        Database = DB.Database()
        self.comboBox_3.clear()
        self.comboBox_3.addItems(Database.get_table_data())
        print(Database.get_table_data())
        self.pushButton_14.clicked.connect(self.deleteDB)

def itemtexttrig(self):
    self.clearfields(0)
    self.pushButton_12.setEnabled(True)
    self.lineEdit_9.setEnabled(True)

def edititem(self):
    Database = DB.Database()
    Database.update_data(self.lineEdit_9.text(),self.comboBox_3.currentText(),'NULL',int(self.lineEdit_6.text()),float(self.lineEdit_7.text()),float(self.lineEdit_8.text()),self.lineEdit_10.text(),self.lineEdit_11.text())
    Database.close_connection()
    self.clearfields()
    self.popupMessage("Successful","Item Edit successfully")


def deleteDB(self):
    Database = DB.Database()
    Database.delete_data(self.lineEdit_9.text())
    Database.close_connection()
    self.clearfields()
    self.popupMessage("Successful","Item Delete successfully")
    self.recommend()



def selectitem(self,itemname):
    Database = DB.Database()
    list=Database.get_item_data_ByName(itemname)
    ItmCo,ItmNa,ItmImg,Qnt,UBP,USP,Sup,Email=list[0]
    self.lineEdit_9.setText(ItmCo)
    self.lineEdit_6.setText(str(Qnt))
    self.lineEdit_7.setText(str(UBP))
    self.lineEdit_8.setText(str(USP))
    self.lineEdit_10.setText(Sup)
    self.lineEdit_11.setText(Email)
    Database.close_connection()
    self.pushButton_12.setEnabled(False)
    self.lineEdit_9.setEnabled(False)


def additeamtoDB(self):
    Database = DB.Database()
    try:
        verify=Database.insert_item(self.lineEdit_9.text(),self.comboBox_3.currentText(),'NULL',int(self.lineEdit_6.text()),float(self.lineEdit_7.text()),float(self.lineEdit_8.text()),self.lineEdit_10.text(),self.lineEdit_11.text())
        if verify==1:
            self.clearfields()
            self.popupMessage("Successful","Item added successfully")
            self.recommend()
        else:
            self.popupMessage("Database Error","Check Item code already exist!")
    except:
        self.popupMessage("Input Data error","Check Details")
    Database.close_connection()

def clearfields(self,NameWant=1):
        self.lineEdit_9.setText('')
        if NameWant == 1:
            self.comboBox_3.clearEditText()
        self.lineEdit_6.setText('')
        self.lineEdit_7.setText('')
        self.lineEdit_8.setText('')
        self.lineEdit_10.setText('')
        self.lineEdit_11.setText('')

def popupMessage(self,Messege,Messege1):
    message=QMessageBox()
    ret=QMessageBox.information(self,Messege,Messege1,QMessageBox.Ok)
    if ret ==QMessageBox.Ok:
        print("User choose OK")