import sys, sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidgetItem, QLabel

con = sqlite3.connect("coffee.db")
cur = con.cursor()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.updatedb()
        self.pushButton.clicked.connect(self.selectelem)

    def updatedb(self):  # Общее обновление TableWidget
        result = cur.execute('''SELECT ID from coffe WHERE ID like '%' ''').fetchall()
        print(result)
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(1)
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def updatetext(self, result):
        self.label_7.setText(str(result[1]))
        self.label_8.setText(str(result[2]))
        if result[3] == "True":
            self.label_3.setText("В зернах")
        else:
            self.label_3.setText("Молотый")
        self.label_9.setText(str(result[4]))
        self.label_10.setText(str(result[5]))
        self.label_11.setText(str(result[6]))

    def selectelem(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        names = [self.tableWidget.item(i, 0).text() for i in rows]
        result = cur.execute("SELECT * from coffe WHERE ID in (" +
                             ", ".join('?' * len(names)) + ")", names).fetchone()
        self.updatetext(result)
        self.updatedb()


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
