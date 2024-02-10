# import DB

# Database = DB.Database()

# Database.insert_item('SD2343','Nut 34*2*2','NULL',12,50.50,25.00,'DS Holdings','DSHoldings@gmail.com')
# # Database.insert_item('SD2342','Nut 33*21*4','NULL',12,50.40,25.00,'DSS Holdings','DSSHoldings@gmail.com')
# # Database.insert_item('SD2442','Nut 15*21*4','NULL',11,50.40,25.00,'DSS Holdings','DSSHoldings@gmail.com')
# print("Hello World")

# Database.close_connection()

import sys
from PySide6.QtWidgets import QApplication, QComboBox, QVBoxLayout, QWidget

class ComboBoxExample(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Create combo box
        self.comboBox = QComboBox(self)
        self.comboBox.setEditable(True)
        self.comboBox.lineEdit().textChanged.connect(self.updateRecommendations)

        layout.addWidget(self.comboBox)
        self.setLayout(layout)

        # Add some initial items
        self.items = ["Apple", "Banana", "Orange", "Peach", "Pear"]
        self.comboBox.addItems(self.items)

    def updateRecommendations(self, text):
        # Clear current items
        self.comboBox.clear()

        # Filter items based on user input and add them to the combo box
        matching_items = [item for item in self.items if text.lower() in item.lower()]
        self.comboBox.addItems(matching_items)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ComboBoxExample()
    ex.show()
    sys.exit(app.exec())
