import sqlite3
from typing import Union

class Database:
    def __init__(self,db_name = 'database.db'): #Create Database and Create Table if does not exists.
        self.database_connection = sqlite3.connect(db_name)
        self.cursor = self.database_connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Stock (ItemCode TEXT PRIMARY KEY, ItemName TEXT,ItemImage BLOB,Quantity INTEGER, UnitBuyingPrice REAL, UnitSellingPrice REAL, SupplierName TEXT, SupplierEmail TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Customers (InvoiceNumber TEXT PRIMARY KEY,DateTime TEXT,TotalAmount REAL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Orders (ID INTEGER PRIMARY KEY, InvoiceNumber TEXT, ItemCode TEXT, Quantity INTEGER, SellingPrice REAL, FOREIGN KEY (ItemCode) REFERENCES Stock(ItemCode))")
        self.database_connection.commit()
    
    def insert_item(self, ItemCode : str, ItemName: str, ItemImage, Quantity: int, UnitBuyingPrice: float, UnitSellingPrice: float, SupplierName: str, SupplierEmail: str) -> int:
        """
        This function return 1 or 0

        Returns:
        -If data successfully added to database return 1. Otherwise return 0.
        """
        try:
            self.cursor.execute("""INSERT INTO Stock VALUES (?,?,?,?,?,?,?,?)""", (ItemCode, ItemName, ItemImage, Quantity, UnitBuyingPrice, UnitSellingPrice, SupplierName, SupplierEmail))
        except:
            return 0
        else:
            self.database_connection.commit()
            return 1
    
    def get_item_data_ByName(self,ItemName: str) -> Union[int,list]:
        """
        This function return either 0 or list.

        Returns:
        -If data not found in database then return 0. Otherwise return list of data.
        """
        self.cursor.execute("""SELECT * FROM Stock WHERE ItemName like ?""",(ItemName + '%',))
        result = self.cursor.fetchall()
        if len(result) == 0:
            return 0
        else:
            return result
    
    def get_item_data_ByCode(self,ItemCode: str)-> Union[int,list]:
        """
        This function return either 0 or list.

        Returns:
        -If data not found in database then return 0.Otherwise return list of data.
        """
        self.cursor.execute("""SELECT * FROM Stock WHERE ItemCode = ?""",(ItemCode,))
        result = self.cursor.fetchall()
        if len(result) == 0:
            return 0
        else:
            return result
        
    def get_current_quantity(self, ItemCode: str) -> list:
        self.cursor.execute("""SELECT Quantity FROM Stock WHERE ItemCode = ?""",(ItemCode,))
        result = self.cursor.fetchall()
        return [x for x in result[0]]
    
    def update_data(self, ItemCode : str, ItemName: str, ItemImage, Quantity: int, UnitBuyingPrice: float, UnitSellingPrice: float, SupplierName: str, SupplierEmail: str):
        """
        This function return 1 or 0

        Returns:
        -If data successfully updated to database return 1. Otherwise return 0.
        """
        try:
            self.cursor.execute("""UPDATE Stock SET ItemName = ?, ItemImage = ?, Quantity = ?, UnitBuyingPrice = ?, UnitSellingPrice = ?, SupplierName = ?, SupplierEmail = ? WHERE ItemCode = ?""", (ItemName, ItemImage, Quantity, UnitBuyingPrice, UnitSellingPrice, SupplierName, SupplierEmail, ItemCode))
        except:
            return 0
        else:
            self.database_connection.commit()
            return 1
    
    def delete_data(self,ItemCode : str):
        """
        This function return 1 or 0

        Returns:
        -If data successfully deleted to database return 1. Otherwise return 0.
        """
        try:
            self.cursor.execute("""DELETE FROM Stock WHERE ItemCode = ?""",(ItemCode,))
        except:
            return 0
        else:
            self.database_connection.commit()
            return 1

    def place_order(self, InvoiceNumber: str, Item_dictionary: dict, TotalAmount: float):
        """
        Parameters:
        -Item_dictionary = {ItemCode:(Quantity,SellingPrice)}
        """
        self.cursor.execute("""INSERT INTO Customers VALUES (?,"NULL",?)""",(InvoiceNumber,TotalAmount))
        self.database_connection.commit()
        for item_code,quantity_price in Item_dictionary.items():
            self.cursor.execute("""INSERT INTO Orders (InvoiceNumber, ItemCode, Quantity, SellingPrice) VALUES (?,?,?,?)""",(InvoiceNumber, item_code, quantity_price[0], quantity_price[1]))
            self.database_connection.commit()
            data = self.__update_stock_ByOrder(item_code,quantity_price[0])
    
    def __update_stock_ByOrder(self, ItemCode, Quantity):
        self.cursor.execute("""SELECT Quantity FROM Stock WHERE ItemCode = ?""", (ItemCode,))
        current_quantity = self.cursor.fetchall()
        updated_quantity = int(current_quantity[0][0]) - Quantity
        self.cursor.execute("""UPDATE Stock SET Quantity = ? WHERE ItemCode = ?""", (updated_quantity,ItemCode))
        self.database_connection.commit()

    def get_table_data(self):
        self.cursor.execute("""SELECT ItemName FROM Stock ORDER BY ItemName ASC""")
        result = self.cursor.fetchall()
        return [x[0] for x in result]
    
    def get_all_table_data(self):
        self.cursor.execute("""SELECT * FROM Stock ORDER BY ItemCode ASC""")
        result = self.cursor.fetchall()
        return result

    def close_connection(self):
        self.cursor.close()
        self.database_connection.close()