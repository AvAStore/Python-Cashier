import sys
import DB
from PySide6.QtCore import Qt,QSize
from PySide6.QtWidgets import QMainWindow,QWidget,QMessageBox,QTableWidgetItem,QPushButton
from PySide6.QtGui import QFont,QFontDatabase,QIcon
from ui_main import Ui_MainWindow
import datetime

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showMaximized() # Maximize window
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Coustom Main Window..")
        QFontDatabase.addApplicationFont("horyzen/Horyzen Regular.ttf")
        QFontDatabase.addApplicationFont("horyzen/Horyzen Light.ttf")
        self.stackedWidget.setCurrentWidget(self.page)
        self.pushButton.clicked.connect(self.close)
        self.pushButton_2.clicked.connect(self.minimize)
        self.pushButton_3.clicked.connect(self.CashiePage)
        self.pushButton_4.clicked.connect(self.InventoryPage)
        self.pushButton_7.clicked.connect(self.Loginpage)
        self.pushButton_11.clicked.connect(self.Coustmeradditem)
        self.pushButton_12.clicked.connect(self.additeamtoDB)
        self.pushButton_13.clicked.connect(self.edititem)
        self.pushButton_10.clicked.connect(self.placeOder)
        self.pushButton_15.clicked.connect(self.finishOder)
        self.pushButton_14.clicked.connect(self.deleteDB)
        
        self.comboBox_3.textActivated.connect(self.selectitem)
        self.comboBox_2.textActivated.connect(self.Custitemlist)
        self.comboBox_3.editTextChanged.connect(self.itemtexttrig)
        self.comboBox_2.editTextChanged.connect(self.Custclear)
        self.lineEdit_12.editingFinished.connect(self.Custitemlistbycode)
        self.lineEdit_12.textEdited.connect(self.Custitemreset)
        
        self.pushButton_15.setEnabled(False)

        self.Oderinglist={}
        self.totalPrice=0

        self.recommend()

    def placeOder(self):
        invoice_num = self.__generate_invoice_number()
        try:
            cashRecive=float(self.lineEdit_3.text())
            if cashRecive>=self.totalPrice:
                Database = DB.Database()
                Database.place_order(invoice_num,self. Oderinglist,self.totalPrice)
                Database.close_connection()
                self.label_8.setText(invoice_num)
                self.lineEdit_13.setText(str(cashRecive-self.totalPrice))
                self.pushButton_11.setEnabled(False)
                self.pushButton_10.setEnabled(False)
                self.pushButton_15.setEnabled(True)
                self.lineEdit_3.setEnabled(False)
                self.tableWidget.setEnabled(False)

            else:
                self.popupMessage("Invalid Amount","Please Check the Amount.")
        except:
            self.popupMessage("Invalid Amount","Please Check the Amount.")

    def finishOder(self):
        self.Oderinglist={}
        self.totalPrice=0
        self.refreshOderlist()
        self.label_8.setText("")
        self.lineEdit_13.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_2.setText("")
        self.pushButton_11.setEnabled(True)
        self.lineEdit_3.setEnabled(True)
        self.pushButton_15.setEnabled(False)
        self.pushButton_10.setEnabled(True)
        self.tableWidget.setEnabled(True)

    def __generate_invoice_number(self):
        now = datetime.datetime.now()
        date_part = now.strftime("%Y%m%d")  # Format: YearMonthDay
        time_part = now.strftime("%H%M%S")  # Format: HourMinuteSecond
        invoice_number = f"INV-{date_part}-{time_part}"
        return invoice_number

    def Custitemlist(self,itemname):
        Database = DB.Database()
        list=Database.get_item_data_ByName(itemname)
        ItmCo,ItmNa,ItmImg,Qnt,UBP,USP,Sup,Email=list[0]
        self.comboBox_2.setCurrentText(ItmNa)
        self.lineEdit_12.setText(ItmCo)
        self.lineEdit_5.setText(str(USP))
        Database.close_connection()

    def Coustmeradditem(self):
        Database = DB.Database()
        list=Database.get_item_data_ByCode(self.lineEdit_12.text())
        ItmCo,ItmNa,ItmImg,Qnt,UBP,USP,Sup,Email=list[0]
        Database.close_connection()
        try:
            buying_quantity = int(self.lineEdit_4.text())
            if buying_quantity <= 0:
                self.popupMessage("Invalid quantity",f"Please enter valid quantity maximum:{Qnt}")
            elif Qnt>=int(buying_quantity):
                self.Oderinglist.update({ItmCo:(buying_quantity,USP,ItmNa)})
                self.clearfields(1)
                self.refreshOderlist()
            else:
                self.popupMessage("Stock exceed",f"Only Have:{Qnt}")
        except:
            self.popupMessage("Invalid quantity",f"Please enter valid quantity maximum:{Qnt}")

    def refreshOderlist(self):
        OderRow=0
        buttonlist=[]
        self.totalPrice=0
        AllQuntity=0
        self.tableWidget.setRowCount(len(self.Oderinglist.items()))
        for x,y in self.Oderinglist.items():
            button = QPushButton("Remove")
            button.clicked.connect(lambda code=x, x3=x: self.DeleteOderiteamButton(x3))
            buttonlist.append(button)
            
            self.tableWidget.setItem(OderRow,0,QTableWidgetItem(x))
            self.tableWidget.setItem(OderRow,1,QTableWidgetItem(y[2]))
            self.tableWidget.setItem(OderRow,2,QTableWidgetItem(str(y[0])))
            self.tableWidget.setItem(OderRow,3,QTableWidgetItem(str(y[1])))
            self.tableWidget.setItem(OderRow,4,QTableWidgetItem(str(y[0]*y[1])))
            self.tableWidget.setCellWidget(OderRow,5,buttonlist[OderRow])
            self.totalPrice=self.totalPrice+y[0]*y[1]
            AllQuntity+=y[0]
            OderRow+=1
        self.label_22.setText(str(self.totalPrice))
        self.lineEdit_2.setText(str(self.totalPrice))
        self.label_26.setText(str(len(self.Oderinglist.items())))
        self.label_24.setText(str(AllQuntity))

        


    def DeleteOderiteamButton(self,code):
        del self.Oderinglist[code]
        self.refreshOderlist()  
        print(f"Deleteing:{code}")
        print(self.Oderinglist)

    def Custitemlistbycode(self):
        Database = DB.Database()
        list=Database.get_item_data_ByCode(self.lineEdit_12.text())
        ItmCo,ItmNa,ItmImg,Qnt,UBP,USP,Sup,Email=list[0]
        self.comboBox_2.setCurrentText(ItmNa)
        self.lineEdit_12.setText(ItmCo)
        self.lineEdit_5.setText(str(USP))
        Database.close_connection()

    def Custitemreset(self):
        self.comboBox_2.setCurrentText("")
        self.lineEdit_5.setText("")

    def Custclear(self):
        self.lineEdit_5.setText("")
        self.lineEdit_12.setText("")

    def itemListing(self):
        pass

    def Cashertable(self):
        self.tableWidget.setColumnWidth(0,int(((self.tableWidget.frameGeometry().width())/6)))
        self.tableWidget.setColumnWidth(1,int(((self.tableWidget.frameGeometry().width())/6)))
        self.tableWidget.setColumnWidth(2,int(((self.tableWidget.frameGeometry().width())/6)))
        self.tableWidget.setColumnWidth(3,int(((self.tableWidget.frameGeometry().width())/6)))
        self.tableWidget.setColumnWidth(4,int(((self.tableWidget.frameGeometry().width())/6)))
        self.tableWidget.setColumnWidth(5,int(((self.tableWidget.frameGeometry().width())/6)))


    def Showitemlisttable(self):
        self.tableWidget_2.setColumnWidth(0,int(((self.tableWidget_2.frameGeometry().width())/8)))
        self.tableWidget_2.setColumnWidth(1,int(((self.tableWidget_2.frameGeometry().width())/8)))
        self.tableWidget_2.setColumnWidth(2,int(((self.tableWidget_2.frameGeometry().width())/8)))
        self.tableWidget_2.setColumnWidth(3,int(((self.tableWidget_2.frameGeometry().width())/8)))
        self.tableWidget_2.setColumnWidth(4,int(((self.tableWidget_2.frameGeometry().width())/8)))
        self.tableWidget_2.setColumnWidth(5,int(((self.tableWidget_2.frameGeometry().width())/8)))
        self.tableWidget_2.setColumnWidth(6,int(((self.tableWidget_2.frameGeometry().width())/8)))
        self.tableWidget_2.setColumnWidth(7,int(((self.tableWidget_2.frameGeometry().width())/10)))


        Database = DB.Database()
        tabledata=Database.get_all_table_data()
        self.tableWidget_2.setRowCount(len(tabledata))
        Database.close_connection()
        buttonlist=[]
        cursorrow=0
        for row in tabledata:
            button = QPushButton("Edit")
            button.clicked.connect(lambda r=row, row=row: self.editButtonClicked(row))

            """
            def anonymus(r=row,row=row):
               self.editButtonClicked(row)
            """
            
            buttonlist.append(button)
            self.tableWidget_2.setItem(cursorrow,0,QTableWidgetItem(row[0]))
            self.tableWidget_2.setItem(cursorrow,1,QTableWidgetItem(row[1]))
            self.tableWidget_2.setItem(cursorrow,2,QTableWidgetItem(str(row[3])))
            self.tableWidget_2.setItem(cursorrow,3,QTableWidgetItem(str(row[4])))
            self.tableWidget_2.setItem(cursorrow,4,QTableWidgetItem(str(row[5])))
            self.tableWidget_2.setItem(cursorrow,5,QTableWidgetItem(str(row[6])))
            self.tableWidget_2.setItem(cursorrow,6,QTableWidgetItem(row[7]))
            self.tableWidget_2.setCellWidget(cursorrow,7,buttonlist[cursorrow])
            cursorrow+=1


    def editButtonClicked(self, row):
        self.comboBox_3.setCurrentText(row[1])
        self.selectitem(row[1])


    def recommend(self):
        Database = DB.Database()
        self.comboBox_3.clear()
        self.comboBox_2.clear()
        self.comboBox_3.addItems(Database.get_table_data())
        self.comboBox_2.addItems(Database.get_table_data())
        Database.close_connection()


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
        self.Showitemlisttable()


    def deleteDB(self):
        Database = DB.Database()
        Database.delete_data(self.lineEdit_9.text())
        Database.close_connection()
        self.clearfields()
        self.recommend()
        self.Showitemlisttable()
        self.popupMessage("Successful","Item Delete successfully")




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
                self.Showitemlisttable()
                self.popupMessage("Successful","Item added successfully")
                self.recommend()
            else:
                self.popupMessage("Database Error","Check Item code already exist!")
        except:
            self.popupMessage("Input Data error","Check Details")
        Database.close_connection()



    def Loginpage(self):
        self.stackedWidget.setCurrentWidget(self.page)

    def CashiePage(self):
        self.stackedWidget.setCurrentWidget(self.page_2)
        self.recommend()
        self.Cashertable()
                

    def InventoryPage(self):
        self.stackedWidget.setCurrentWidget(self.page_3)
        self.Showitemlisttable()     

    def minimize(self):
        self.showMinimized()

    def close(self):
        sys.exit()
    
    def clearfields(self,NameWant=1):
        self.lineEdit_9.setText('')
        if NameWant == 1:
            self.comboBox_3.clearEditText()
            self.comboBox_2.clearEditText()
        self.lineEdit_6.setText('')
        self.lineEdit_7.setText('')
        self.lineEdit_8.setText('')
        self.lineEdit_10.setText('')
        self.lineEdit_11.setText('')

        self.lineEdit_12.setText('')
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')

        

    def popupMessage(self,Messege,Messege1):
        message=QMessageBox()
        ret=QMessageBox.information(self,Messege,Messege1,QMessageBox.Ok)
        if ret ==QMessageBox.Ok:
            print(Messege1)
            print("User choose OK")
    
