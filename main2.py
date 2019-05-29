from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QDialog,QTabWidget, \
    QComboBox, QCheckBox ,QGroupBox ,QVBoxLayout, QWidget, \
    QLabel, QLineEdit, QDialogButtonBox, QRadioButton, \
    QPushButton, QMainWindow, QHBoxLayout
import sys
from PyQt5.QtGui import QIcon

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

        tabWidget.setFont(QtGui.QFont("MS Sans Serif", 10))
        tabWidget.addTab(InstantSearch(), "Flight")
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
        button.setIconSize(QtCore.QSize(40, 40))
        button.setToolTip("<h4>Search for today's flight<h4>")
        #button.clicked.connect(self.ButtonAction)
        vbox4.addWidget(button)

        groupBox4.setLayout(vbox4)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(groupBox)
        mainLayout.addWidget(groupBox2)
        mainLayout.addWidget(groupBox3)
        mainLayout.addWidget(groupBox4)
        self.setLayout(mainLayout)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    tabdialog = MainFrame()
    tabdialog.show()
    app.exec()