import sys
import sqlite3
import pandas as pd

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qfluentwidgets import *

class Backend:
    """ Backend class to handle database operations """

    def __init__(self, directory, sql):
        self.directory = directory
        self.sql = sql

    def view_table(self, directory):
        """ View tables in the database and return their headers """
        with sqlite3.connect(directory) as connection:
            tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
            tables = pd.read_sql_query(tables_query, connection)
            database_info = ""
            for table in tables['name']:
                headers_query = f"PRAGMA table_info({table});"
                headers = pd.read_sql_query(headers_query, connection)
                table_info = f"Таблица: {table}\nЗаголовки: {', '.join(headers['name'].tolist())}\n\n"
                database_info += table_info
        return database_info

    def eval_query(self, directory, sql):
        """ Execute a SQL query and return the result """
        with sqlite3.connect(directory) as connection:
            query = f"{sql}"
            res = pd.read_sql(query, connection)
        return res.to_string()

class CustomMessageBox(MessageBoxBase):
    """ Custom message box for directory input """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('Set the directory', self)
        self.urlLineEdit = LineEdit(self)
        self.urlLineEdit.setPlaceholderText('Directory')
        self.urlLineEdit.setClearButtonEnabled(True)
        self.warningLabel = CaptionLabel("The directory is invalid")
        self.warningLabel.setTextColor("#cf1010", QColor(255, 28, 32))

        # Add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.urlLineEdit)
        self.viewLayout.addWidget(self.warningLabel)
        self.warningLabel.hide()

        # Change the text of buttons
        self.yesButton.setText('Yes, set')
        self.cancelButton.setText('Cancel')
        self.widget.setMinimumWidth(350)

    def validate(self):
        """ Validate the directory input """
        isValid = QUrl(self.urlLineEdit.text()).isValid()
        self.warningLabel.setHidden(isValid)
        return isValid

class Demo(QWidget):
    """ Main Demo class for the GUI """

    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)
        self.setStyleSheet("""
            Demo{background: black}
            QLabel{
                font: 20px 'Segoe UI';
                background: rgb(33,32,32);
                border-radius: 8px;
            }
        """)
        self.resize(400, 400)
        self.sql = "DataBase is not selected"

        self.pivot = SegmentedToggleToolWidget(self)
        self.stackedWidget = QStackedWidget(self)

        self.hBoxLayout = QHBoxLayout()
        self.vBoxLayout = QVBoxLayout(self)

        self.buttonInterface = PushButton('Set the directory', self)
        self.viewTableInterface = TextBrowser(self)
        self.promptInterface = TextEdit(self)
        self.executeInterface = PushButton('Execute', self)
        self.viewInterface = TextBrowser(self)

        # Add items to pivot
        self.add_sub_interface(self.buttonInterface, 'folderInterface', FluentIcon.FOLDER_ADD)
        self.add_sub_interface(self.viewTableInterface, 'viewTableInterface', FluentIcon.FOLDER)
        self.add_sub_interface(self.promptInterface, 'promptInterface', FluentIcon.COMMAND_PROMPT)
        self.add_sub_interface(self.executeInterface, 'executeInterface', FluentIcon.DEVELOPER_TOOLS)
        self.add_sub_interface(self.viewInterface, 'viewInterface', FluentIcon.VIEW)

        self.hBoxLayout.addWidget(self.pivot, 0, Qt.AlignCenter)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(30, 10, 30, 30)

        self.stackedWidget.setCurrentWidget(self.buttonInterface)
        self.pivot.setCurrentItem(self.buttonInterface.objectName())
        self.pivot.currentItemChanged.connect(
            lambda k: self.stackedWidget.setCurrentWidget(self.findChild(QWidget, k)))

        self.executeInterface.clicked.connect(self.execute)
        self.buttonInterface.clicked.connect(self.show_dialog)

    def show_dialog(self):
        """ Show custom message box for directory input """
        w = CustomMessageBox(self)
        if w.exec():
            global url
            url = w.urlLineEdit.text()
            self.viewTableInterface.setPlaceholderText(Backend().view_table(url))
            return url

    def execute(self):
        """ Execute SQL query and display result """
        sql = self.promptInterface.toPlainText().replace("\n", " ")
        self.viewInterface.setPlaceholderText(Backend().eval_query(url, sql))

    def add_sub_interface(self, widget, objectName, icon):
        """ Add sub-interface to pivot widget """
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(routeKey=objectName, icon=icon)

if __name__ == '__main__':
    # Enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec_()
