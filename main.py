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
        self.pushButton_2.clicked.connect(self.edit)

    def edit(self):
        self.edit = CoffeEdit(self)
        self.edit.show()

    def finding(self):
        self.listWidget.clear()
        self.coffes = self.data_users_cursor.execute(f"""SELECT ID from main""").fetchall()
        for i in self.coffes:
            name = self.data_users_cursor.execute(f'''SELECT
                     названиесорта from main WHERE ID = {i[0]}''').fetchall()[0][0]
            i2 = QPushButton(f"{name.capitalize()}--({i[0]})")
            list_widget_item = QListWidgetItem()
            if self.lineEdit.text().lower() in i2.text().lower():
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
        self.can_edit = True


class CoffeEdit(QMainWindow):
    def __init__(self, into):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.new_coffe)
        self.into = into
        self.update_widget()
        self.select = []
        self.pushButton_2.clicked.connect(self.edit_coffe_info)

    def edit_coffe_info(self):
        try:
            if self.select == []:
                raise Exception('Объект редактирования не выбран! Выберете его из списка выше!')
            if self.lineEdit_17.text() == '' or self.lineEdit_18.text() == '' \
                    or self.lineEdit_14.text() == '' or self.lineEdit_16.text() == '' \
                    or self.lineEdit_15.text() == '' or self.lineEdit_13.text() == '':
                raise Exception('Не все поля заполнены!')
            self.into.data_users_cursor.execute(
                f'UPDATE main SET названиесорта = \'{self.lineEdit_17.text()}\''
                f' WHERE ID = {int(self.select[0].split("--")[-1][1:-1])}')
            self.into.data_users_cursor.execute(
                f'UPDATE main SET степеньобжарки = \'{self.lineEdit_18.text()}\''
                f' WHERE ID = {int(self.select[0].split("--")[-1][1:-1])}')
            self.into.data_users_cursor.execute(
                f'UPDATE main SET молотыйвзернах = \'{self.lineEdit_14.text()}\''
                f' WHERE ID = {int(self.select[0].split("--")[-1][1:-1])}')
            self.into.data_users_cursor.execute(
                f'UPDATE main SET описаниевкуса = \'{self.lineEdit_16.text()}\''
                f' WHERE ID = {int(self.select[0].split("--")[-1][1:-1])}')
            self.into.data_users_cursor.execute(
                f'UPDATE main SET цена = \'{self.lineEdit_15.text()}\''
                f' WHERE ID = {int(self.select[0].split("--")[-1][1:-1])}')
            self.into.data_users_cursor.execute(
                f'UPDATE main SET объемупаковки = \'{self.lineEdit_13.text()}\''
                f' WHERE ID = {int(self.select[0].split("--")[-1][1:-1])}')
            self.into.data_users_connect.commit()
            self.into.update_widget()
            self.update_widget()
        except Exception as e:
            self.statusBar.showMessage(str(e), 2000)

    def update_widget(self):
        self.listWidget.clear()
        self.coffes = self.into.data_users_cursor.execute(f"""SELECT ID from main""").fetchall()
        for i in self.coffes:
            name = self.into.data_users_cursor.execute(f'''SELECT
                     названиесорта from main WHERE ID = {i[0]}''').fetchall()[0][0]
            i2 = QPushButton(f"{name.capitalize()}--({i[0]})")
            list_widget_item = QListWidgetItem()
            self.listWidget.addItem(list_widget_item)
            self.listWidget.setItemWidget(list_widget_item, i2)
            i2.clicked.connect(self.edit_coffe)
        self.select = []
        self.lineEdit_17.setText('')
        self.lineEdit_18.setText('')
        self.lineEdit_14.setText('')
        self.lineEdit_16.setText('')
        self.lineEdit_15.setText('')
        self.lineEdit_13.setText('')

    def edit_coffe(self):
        sender = self.sender()
        self.listWidget.clear()
        i2 = QPushButton(sender.text())
        list_widget_item = QListWidgetItem()
        self.listWidget.addItem(list_widget_item)
        self.listWidget.setItemWidget(list_widget_item, i2)
        i2.clicked.connect(self.update_widget)
        self.select.append(sender.text())
        data = self.into.data_users_cursor.execute(f'SELECT названиесорта, степеньобжарки,'
                                                   f' молотыйвзернах, описаниевкуса, цена,'
                                                   f' объемупаковки from main WHERE ID'
                                                   f' = {int(self.select[0].split("--")[-1][1:-1])}').fetchall()[0]
        self.lineEdit_17.setText(data[0])
        self.lineEdit_18.setText(data[1])
        self.lineEdit_14.setText(data[2])
        self.lineEdit_16.setText(data[3])
        self.lineEdit_15.setText(data[4])
        self.lineEdit_13.setText(data[5])

    def new_coffe(self):
        try:
            if self.lineEdit.text() == '' or self.lineEdit_2.text() == '' \
                    or self.lineEdit_3.text() == '' or self.lineEdit_4.text() == '' \
                    or self.lineEdit_5.text() == '' or self.lineEdit_6.text() == '':
                raise Exception('Не все поля заполнены!')
            self.into.data_users_cursor.execute(
                f'INSERT INTO main(названиесорта,'
                f' степеньобжарки, молотыйвзернах, описаниевкуса, цена, объемупаковки)'
                f' VALUES(\'{self.lineEdit.text()}\', \'{self.lineEdit_2.text()}\','
                f' \'{self.lineEdit_3.text()}\', \'{self.lineEdit_4.text()}\', \'{self.lineEdit_5.text()}\','
                f' \'{self.lineEdit_6.text()}\')')
            self.into.data_users_connect.commit()
            self.into.update_widget()
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit_3.setText('')
            self.lineEdit_4.setText('')
            self.lineEdit_5.setText('')
            self.lineEdit_6.setText('')
            self.update_widget()
        except Exception as e:
            self.statusBar.showMessage(str(e), 2000)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Coffe()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
