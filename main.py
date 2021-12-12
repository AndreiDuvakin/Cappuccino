from PyQt5.QtWidgets import QApplication, QMainWindow
import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QListWidgetItem, QPushButton, QListWidget, QTextBrowser


class Coffe(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.data_users_connect = sqlite3.connect('main.db')
        self.data_users_cursor = self.data_users_connect.cursor()

        self.update_widget()

        self.pushButton.clicked.connect(self.finding)

    def finding(self):
        self.listWidget.clear()
        self.coffes = self.data_users_cursor.execute(f"""SELECT ID from main""").fetchall()
        for i in self.coffes:
            name = self.data_users_cursor.execute(f'''SELECT
                     названиесорта from main WHERE ID = {i[0]}''').fetchall()[0][0]
            i2 = QPushButton(f"{name.capitalize()}--({i[0]})")
            list_widget_item = QListWidgetItem()
            if self.lineEdit.text() in i2.text():
                self.listWidget.addItem(list_widget_item)
                self.listWidget.setItemWidget(list_widget_item, i2)
                i2.clicked.connect(self.go)

    def update_widget(self):
        self.listWidget.clear()
        self.coffes = self.data_users_cursor.execute(f"""SELECT ID from main""").fetchall()
        for i in self.coffes:
            name = self.data_users_cursor.execute(f'''SELECT
             названиесорта from main WHERE ID = {i[0]}''').fetchall()[0][0]
            i2 = QPushButton(f"{name.capitalize()}--({i[0]})")
            list_widget_item = QListWidgetItem()
            self.listWidget.addItem(list_widget_item)
            self.listWidget.setItemWidget(list_widget_item, i2)
            i2.clicked.connect(self.go)

    def go(self):
        sender = self.sender()
        self.label_7.setText(sender.text().split('--')[0])
        self.label_8.setText(self.data_users_cursor.execute(f"""SELECT
        степеньобжарки from main WHERE ID =
        {sender.text().split('--')[-1]}""").fetchall()[0][0].capitalize())
        self.label_9.setText(self.data_users_cursor.execute(f"""SELECT
        молотыйвзернах from main WHERE
         ID = {sender.text().split('--')[-1]}""").fetchall()[0][0].capitalize())
        self.label_10.setText(self.data_users_cursor.execute(f"""SELECT
        описаниевкуса from main WHERE
         ID = {sender.text().split('--')[-1]}""").fetchall()[0][0].capitalize())
        self.label_11.setText(self.data_users_cursor.execute(f"""SELECT
        цена from main WHERE
         ID = {sender.text().split('--')[-1]}""").fetchall()[0][0].capitalize())
        self.label_12.setText(self.data_users_cursor.execute(f"""SELECT
        объемупаковки from main WHERE
         ID = {sender.text().split('--')[-1]}""").fetchall()[0][0].capitalize())


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Coffe()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
