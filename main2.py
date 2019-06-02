from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QDialog,QTabWidget, \
    QComboBox, QCheckBox ,QGroupBox ,QVBoxLayout, QWidget, \
    QLabel, QLineEdit, QDialogButtonBox, QRadioButton, \
    QPushButton, QHBoxLayout, QTableWidget, QTableView, QGridLayout, QTableWidgetItem
import sys
from PyQt5.QtGui import QIcon
import test_table as tt
import pandas as pd

df = pd.read_pickle("airports.pkl")

class MainFrame(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Airport Query System")
        self.setWindowIcon(QIcon("icon.svg"))
        #self.setStyleSheet('background-color:grey')

        self.top = 200
        self.left = 1800
        self.width = 500
        self.height = 700
        self.setGeometry(self.left, self.top, self.width, self.height)

        vbox = QVBoxLayout()
        tabWidget = QTabWidget()

        buttonbox = QDialogButtonBox(QDialogButtonBox.Close)
        buttonbox.rejected.connect(self.reject)
        buttonbox.setFont(QtGui.QFont("MS Sans Serif", 10))
        buttonbox.setToolTip("<h4>Close the application。<h4>")

        tabWidget.setFont(QtGui.QFont("MS Sans Serif", 10))
        tabWidget.addTab(InstantSearch(), "Flight")
        tabWidget.addTab(Library(), "Library")
        #tabWidget.addTab(TabPeronsalDetails(), "Personal Details")


        vbox.addWidget(tabWidget)
        vbox.addWidget(buttonbox)

        self.setLayout(vbox)

class InstantSearch(QWidget):
    def __init__(self):
        super().__init__()

        groupBox = QGroupBox("")
        vbox = QVBoxLayout()

        label = QLabel("Airport: ")
        label.setFont(QtGui.QFont("MS Sans Serif", 10))
        code = QLineEdit()
        vbox.addWidget(label)
        vbox.addWidget(code)

        label2 = QLabel("Airline: ")
        label2.setFont(QtGui.QFont("MS Sans Serif", 10))
        airline = QLineEdit()
        vbox.addWidget(label2)
        vbox.addWidget(airline)

        label3 = QLabel("Origin/Arrival: ")
        label3.setFont(QtGui.QFont("MS Sans Serif", 10))
        dest = QLineEdit()
        vbox.addWidget(label3)
        vbox.addWidget(dest)

        label4 = QLabel("Flight #: ")
        label4.setFont(QtGui.QFont("MS Sans Serif", 10))
        flightnum = QLineEdit()
        vbox.addWidget(label4)
        vbox.addWidget(flightnum)
        groupBox.setLayout(vbox)

        groupBox2 = QGroupBox("")

        vbox2 = QHBoxLayout()
        radiobtn1 = QRadioButton("Departure")
        radiobtn1.setFont(QtGui.QFont("MS Sans Serif", 10))
        radiobtn1.setIcon(QtGui.QIcon("dep.png"))
        radiobtn1.setChecked(True)
        vbox2.addWidget(radiobtn1)

        radiobtn2 = QRadioButton("Arrival")
        radiobtn2.setFont(QtGui.QFont("MS Sans Serif", 10))
        radiobtn2.setIcon(QtGui.QIcon("arr.png"))
        vbox2.addWidget(radiobtn2)

        groupBox2.setLayout(vbox2)

        groupBox3 = QGroupBox("")

        vbox3 = QHBoxLayout()
        check1 = QCheckBox("No CodeShare")
        check1.setFont(QtGui.QFont("MS Sans Serif", 10))
        vbox3.addWidget(check1)
        check2 = QCheckBox("No Cargo")
        check2.setFont(QtGui.QFont("MS Sans Serif", 10))
        vbox3.addWidget(check2)
        groupBox3.setLayout(vbox3)

        groupBox4 = QGroupBox("")
        vbox4 = QVBoxLayout()
        lst = ['12 AM - 3 AM', '3 AM - 6 AM',
               '6 AM - 9 AM', '9 AM - 12 PM', '12 PM - 3 PM',
               '3 PM - 6 PM', '6 PM - 9 PM', '9 PM - 12 AM', "All Day"]
        combo = QComboBox()
        combo.addItems(lst)
        combo.setFont(QtGui.QFont("MS Sans Serif", 10))
        vbox4.addWidget(combo)

        button = QPushButton("Search", self)
        button.setIcon(QtGui.QIcon("search.png"))
        button.setFont(QtGui.QFont("MS Sans Serif", 10))
        button.setIconSize(QtCore.QSize(25, 25))
        button.setToolTip("<h4>Search for today's flight<h4>")
        button.clicked.connect(self.on_click)
        vbox4.addWidget(button)

        groupBox4.setLayout(vbox4)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(groupBox)
        mainLayout.addWidget(groupBox2)
        mainLayout.addWidget(groupBox3)
        mainLayout.addWidget(groupBox4)
        self.setLayout(mainLayout)

    def on_click(self):
        #mydialog = QDialog(self)
        app = QApplication(sys.argv)
        view = PrettyWidget()
        view.show()
        app.exec()
        #myWindow = Window()
        #myWindow.show()


class PrettyWidget(QDialog):
    def __init__(self):
        super(PrettyWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 300, 400, 200)
        self.setWindowTitle('Table')

        # Grid Layout
        grid = QGridLayout()
        self.setLayout(grid)

        # Data
        data = {'Kitty': ['1', '2', '3', '3'],
                'Cat': ['4', '5', '6', '2'],
                'Meow': ['7', '8', '9', '5'],
                'Purr': ['4', '3', '4', '8'], }

        # Create Empty 5x5 Table
        table = QTableWidget(self)
        table.setRowCount(5)
        table.setColumnCount(5)

        horHeaders = []
        for n, key in enumerate(sorted(data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(data[key]):
                newitem = QTableWidgetItem(item)
                table.setItem(m, n, newitem)

        # Add Header
        table.setHorizontalHeaderLabels(horHeaders)

        # Adjust size of Table
        table.resizeColumnsToContents()
        table.resizeRowsToContents()

        # Add Table to Grid
        grid.addWidget(table, 0, 0)

        self.show()

class table(QTableView):
    def __init__(self):
        super().__init__()

        self.title = "PyQt5 Tables"
        self.top = 100
        self.left = 100
        self.width = 1500
        self.height = 700

        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()


class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, df = pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        return QtCore.QVariant(str(self._df.ix[index.row(), index.column()]))

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()



class Library(QWidget):
    def __init__(self):
        super().__init__()

        groupBox = QGroupBox("Library to look up the Airport or Airline Code: ")
        groupBox.setFont(QtGui.QFont("MS Sans Serif", 10))
        vbox = QVBoxLayout()

        #label = QLabel("Library to look up the Airport or Airline Code: ")
        #label.setFont(QtGui.QFont("MS Sans Serif", 10))
        code = QLineEdit()
        #vbox.addWidget(label)
        vbox.addWidget(code)
        groupBox.setLayout(vbox)

        groupBox2 = QGroupBox("")
        vbox2 = QHBoxLayout()
        radiobtn1 = QRadioButton("Airport")
        radiobtn1.setFont(QtGui.QFont("MS Sans Serif", 10))
        radiobtn1.setIcon(QtGui.QIcon("airport.png"))
        radiobtn1.setChecked(True)
        vbox2.addWidget(radiobtn1)
        radiobtn2 = QRadioButton("Airline")
        radiobtn2.setFont(QtGui.QFont("MS Sans Serif", 10))
        radiobtn2.setIcon(QtGui.QIcon("airline.png"))
        vbox2.addWidget(radiobtn2)
        groupBox2.setLayout(vbox2)

        groupBox3 = QGroupBox("")
        vbox3 = QHBoxLayout()
        button = QPushButton("Search", self)
        button.setIcon(QtGui.QIcon("library.png"))
        button.setFont(QtGui.QFont("MS Sans Serif", 10))
        button.setIconSize(QtCore.QSize(25, 25))
        button.setToolTip("<h4>Search the IATA code from the Aviation Library.<h4>")
        button2 = QPushButton("More", self)
        button2.setIcon(QtGui.QIcon("more info.png"))
        button2.setFont(QtGui.QFont("MS Sans Serif", 10))
        button2.setIconSize(QtCore.QSize(25, 25))
        button2.setToolTip("<h4>This will obtain the more information of the airport or airline.<h4>")
        vbox3.addWidget(button)
        vbox3.addWidget(button2)
        groupBox3.setLayout(vbox3)

        table = QTableWidget(self)  # Create a table
        table.setColumnCount(4)  # Set three columns
        table.setRowCount(1)
        table.setHorizontalHeaderLabels(["IATA", "ICAO", "Name", "Country"])
        table.resizeColumnsToContents()


        mainLayout = QVBoxLayout()
        mainLayout.addWidget(groupBox)
        mainLayout.addWidget(groupBox2)
        mainLayout.addWidget(groupBox3)
        mainLayout.addWidget(table)
        self.setLayout(mainLayout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tabdialog = MainFrame()
    tabdialog.show()
    app.exec()