print("\n>--- Money Management Application ---\n")
print("> Connecting to database...\n")
import sys
import subprocess
import sqlite3

from datetime import date
from functools import partial
from PySide2 import QtCore, QtGui, QtWidgets

global YOURMONEY
incomeList = ["Salary", "Gift", "Sale", "Other"]
expenditureList = ["Food & Drink", "Gas", "Fuel", "Electricity", "Cellphone", "Water", "Internet", "Home rent", "Medical", "Entertainment", "Other Fee", "Fine"]

font = QtGui.QFont()
font.setFamily("Tekton Pro Ext")
font.setPointSize(12)
font.setWeight(10)

def getYourMoney():
	global YOURMONEY
	con = sqlite3.connect(r'.\MoneyDatabase.db')
	cur = con.cursor()
	result = cur.execute("SELECT YourMoney FROM MoneyManagement ORDER BY ID DESC LIMIT 1")
	data = cur.fetchall()
	YOURMONEY = data[0][0]
	con.close()


try: getYourMoney()
except: YOURMONEY = 0

def createDb():
	con = sqlite3.connect(r'.\MoneyDatabase.db')	
	cur = con.cursor()	
	cur.executescript("""
	DROP TABLE IF EXISTS MoneyManagement;
	CREATE TABLE "MoneyManagement" (
	"ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"YourMoney"	REAL NOT NULL DEFAULT 0.00,
	"Income"	REAL,
	"Expenditure"	REAL,
	"Currency "	TEXT NOT NULL DEFAULT 'USD',
	"Reason"	TEXT,
	"Day"	INTEGER NOT NULL,
	"Month"	INTEGER NOT NULL,
	"Year"	INTEGER NOT NULL
	);""")
	con.close()
	

class MainWidget(QtWidgets.QMainWindow):
	def __init__(self, parent=None):
		super(MainWidget, self).__init__()
		self.initUI()

	def initUI(self):
		global YOURMONEY
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.setWindowTitle("Money Management Application")
		self.setSizePolicy(sizePolicy)
		self.layout = QtWidgets.QGridLayout()

		self.centralwidget = QtWidgets.QWidget(self)
		self.centralwidget.setObjectName("centralwidget")
		self.centralwidget.setSizePolicy(sizePolicy)
		self.setCentralWidget(self.centralwidget)
		self.centralwidget.setLayout(self.layout)

		d = date.today()
		today = d.strftime("%d/%m/%Y")

		self.label_1 = QtWidgets.QLabel(self.centralwidget)
		self.label_1.setFont(font)
		self.label_1.setObjectName("Date")
		self.label_1.setText(QtWidgets.QApplication.translate("self.centralwidget", "Date: {}".format(str(today)), None, -1))

		self.currency = QtWidgets.QComboBox(self.centralwidget)
		self.currency.setCurrentIndex(-1)
		self.currency.addItems(["USD","EUR","AUD","GBP","VND"])
		self.currency.currentIndexChanged.connect(self.setTextLabel2)

		self.type = QtWidgets.QComboBox(self.centralwidget)
		self.type.setCurrentIndex(-1)
		self.type.addItems(["Income", "Expenditure"])
		self.type.currentIndexChanged.connect(self.setReasonList)

		self.reason = QtWidgets.QComboBox(self.centralwidget)
		self.reason.setCurrentIndex(-1)

		self.label_2 = QtWidgets.QLabel(self.centralwidget)
		self.label_2.setFont(font)
		self.label_2.setObjectName("Your money")
		self.label_2.setText(QtWidgets.QApplication.translate("self.centralwidget", "Your Money: {} {}".format(str(YOURMONEY), self.currency.currentText()), None, -1))

		self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
		self.lineEdit.setPlaceholderText("Money...")
		reg_ex = QtCore.QRegExp("[0-9]+[0-9]")
		input_validator = QtGui.QRegExpValidator(reg_ex, self.lineEdit)
		self.lineEdit.setValidator(input_validator)
		self.lineEdit.setClearButtonEnabled(True)

		self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
		self.tableWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		self.tableWidget.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
		self.tableWidget.setDefaultDropAction(QtCore.Qt.CopyAction)
		self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.AnyKeyPressed|QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed|QtWidgets.QAbstractItemView.SelectedClicked)
		self.tableWidget.setObjectName("tableWidget")
		self.tableWidget.setColumnCount(9)
		self.tableWidget.setRowCount(100)

		self.pushButton = QtWidgets.QPushButton(self.centralwidget)
		self.pushButton.setFont(font)
		self.pushButton.setObjectName("pushButton")
		self.pushButton.setText(QtWidgets.QApplication.translate("self.centralwidget", "Add to database", None, -1))
		self.pushButton.clicked.connect(partial(self.add))

		self.pushButton_1 = QtWidgets.QPushButton(self.centralwidget)
		self.pushButton_1.setFont(font)
		self.pushButton_1.setObjectName("pushButton_1")
		self.pushButton_1.setText(QtWidgets.QApplication.translate("self.centralwidget", "Get Report Today", None, -1))
		self.pushButton_1.clicked.connect(partial(self.getReportbyDay))

		self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
		self.pushButton_2.setFont(font)
		self.pushButton_2.setObjectName("pushButton_2")
		self.pushButton_2.setText(QtWidgets.QApplication.translate("self.centralwidget", "Get Report This Month", None, -1))
		self.pushButton_2.clicked.connect(partial(self.getReportbyMonth))

		self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
		self.pushButton_3.setFont(font)
		self.pushButton_3.setObjectName("pushButton_3")
		self.pushButton_3.setText(QtWidgets.QApplication.translate("self.centralwidget", "Get Report This Year", None, -1))
		self.pushButton_3.clicked.connect(partial(self.getReportbyYear))

		self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
		self.pushButton_4.setFont(font)
		self.pushButton_4.setObjectName("pushButton_4")
		self.pushButton_4.setText(QtWidgets.QApplication.translate("self.centralwidget", "Clear Data", None, -1))
		self.pushButton_4.clicked.connect(partial(self.resetDatabase))
		
		self.date = QtWidgets.QDateEdit(QtCore.QDate(date.today().year, date.today().month, date.today().day), self.centralwidget)
		self.date.setFont(font)
		self.date.setStyleSheet("background-color: rgb(50, 50, 50);")
		self.date.setDisplayFormat("dd / MM / yyyy")
		self.date.setCurrentSection(QtWidgets.QDateTimeEdit.Section.DaySection)

		self.label_3 = QtWidgets.QLabel(self.centralwidget)
		self.label_3.setFont(font)
		self.label_3.setObjectName("Income")

		self.label_4 = QtWidgets.QLabel(self.centralwidget)
		self.label_4.setFont(font)
		self.label_4.setObjectName("Expenditure")
		

		self.layout.addWidget(self.label_1, 1, 1, 0)
		self.layout.addWidget(self.label_2, 1, 2, 0)
		self.layout.addWidget(self.currency, 1, 5, -1)
		self.layout.addWidget(self.type, 2, 1, 0)
		self.layout.addWidget(self.reason, 2, 2, 0)
		self.layout.addWidget(self.lineEdit, 2, 3, 0)
		self.layout.addWidget(self.date, 2, 4, 0)
		self.layout.addWidget(self.pushButton, 2, 5, -1)
		self.layout.addWidget(self.pushButton_1, 3, 2, QtCore.Qt.AlignTop)
		self.layout.addWidget(self.pushButton_2, 3, 3, QtCore.Qt.AlignTop)
		self.layout.addWidget(self.pushButton_3, 3, 4, QtCore.Qt.AlignTop)
		self.layout.addWidget(self.pushButton_4, 3, 5, QtCore.Qt.AlignTop)
		self.layout.addWidget(self.label_3, 4, 2, QtCore.Qt.AlignTop)
		self.layout.addWidget(self.label_4, 4, 4, QtCore.Qt.AlignTop)

		self.layout.addWidget(self.tableWidget, 3, 1, 0)

		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setHorizontalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setHorizontalHeaderItem(1, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setHorizontalHeaderItem(2, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setHorizontalHeaderItem(3, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setHorizontalHeaderItem(4, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setHorizontalHeaderItem(5, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setHorizontalHeaderItem(6, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setHorizontalHeaderItem(7, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setHorizontalHeaderItem(8, item)


		
		self.tableWidget.horizontalHeaderItem(0).setText(QtWidgets.QApplication.translate("self.centralwidget", "ID", None, -1))
		self.tableWidget.horizontalHeaderItem(1).setText(QtWidgets.QApplication.translate("self.centralwidget", "Your Money", None, -1))
		self.tableWidget.horizontalHeaderItem(2).setText(QtWidgets.QApplication.translate("self.centralwidget", "Income", None, -1))
		self.tableWidget.horizontalHeaderItem(3).setText(QtWidgets.QApplication.translate("self.centralwidget", "Expenditure", None, -1))
		self.tableWidget.horizontalHeaderItem(4).setText(QtWidgets.QApplication.translate("self.centralwidget", "Currency", None, -1))
		self.tableWidget.horizontalHeaderItem(5).setText(QtWidgets.QApplication.translate("self.centralwidget", "Reason", None, -1))
		self.tableWidget.horizontalHeaderItem(6).setText(QtWidgets.QApplication.translate("self.centralwidget", "Day", None, -1))
		self.tableWidget.horizontalHeaderItem(7).setText(QtWidgets.QApplication.translate("self.centralwidget", "Month", None, -1))
		self.tableWidget.horizontalHeaderItem(8).setText(QtWidgets.QApplication.translate("self.centralwidget", "Year", None, -1))
		#self.tableWidget.horizontalHeader().setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

	def add(self):
		global YOURMONEY
		money = self.lineEdit.text()
		typ = self.type.currentText()
		reason = self.reason.currentText()
		currency = self.currency.currentText()
		QDate = self.date.date()
		day = QDate.day()
		month = QDate.month()
		year = QDate.year()
		if(typ == "Income"):
			YOURMONEY = YOURMONEY + int(money)
			data = (None, YOURMONEY, money, 0, currency, reason, day, month, year)
		else:
			YOURMONEY = YOURMONEY - int(money)
			data = (None, YOURMONEY, 0, money, currency, reason, day, month, year)
		con = sqlite3.connect(r'.\MoneyDatabase.db')
		cur = con.cursor()
		cur.execute('INSERT INTO MoneyManagement VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
		con.commit()	
		con.close()
		getYourMoney()
		self.label_2.setText(QtWidgets.QApplication.translate("self.centralwidget", "Your Money: {} {}".format(str(YOURMONEY), self.currency.currentText()), None, -1))

		msg = QtWidgets.QMessageBox()
		msg.setIcon(msg.Information)
		msg.setText("Add Data Successfully!")
		msg.setWindowTitle("Announcement")
		msg.exec_()

	def setTextLabel2(self):
		self.label_2.setText(QtWidgets.QApplication.translate("self.centralwidget", "Your Money: {} {}".format(str(YOURMONEY), self.currency.currentText()), None, -1))

	def setReasonList(self):
		self.reason.clear()
		currentType = self.type.currentText()
		if(currentType == "Income"):
			self.reason.addItems(incomeList)
		else:
			self.reason.addItems(expenditureList)


	def resetDatabase(self):
		createDb()
		msg = QtWidgets.QMessageBox()
		msg.setIcon(msg.Information)
		msg.setText("Reset Data Successfully!")
		msg.setWindowTitle("Announcement")
		msg.exec_()

	def getReportbyDay(self):
		income = 0
		expenditure = 0
		self.tableWidget.clear()
		condition = (date.today().day, )
		con = sqlite3.connect(r'.\MoneyDatabase.db')
		cur = con.cursor()
		i = cur.execute('SELECT Income FROM MoneyManagement WHERE Day=(?)', condition)
		for row_number, row_data in enumerate(i):
			for column_number, data in enumerate(row_data):
				temp = str(str(data).split(".")[0])
				data = int(temp)
				income = income + data
		e = cur.execute('SELECT Expenditure FROM MoneyManagement WHERE Day=(?)', condition)
		for row_number, row_data in enumerate(e):
			for column_number, data in enumerate(row_data):
				temp = str(str(data).split(".")[0])
				data = int(temp)
				expenditure = expenditure + data
		result = cur.execute('SELECT * FROM MoneyManagement WHERE Day=(?)', condition)	
		for row_number, row_data in enumerate(result):
			for column_number, data in enumerate(row_data):
				self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
		con.close()
		
		self.label_3.setText(QtWidgets.QApplication.translate("self.centralwidget", "Your Income today is: {}".format(str(income)), None, -1))

		self.label_4.setText(QtWidgets.QApplication.translate("self.centralwidget", "Your Expenditure today is: {}".format(str(expenditure)), None, -1))

		


	def getReportbyMonth(self):
		income = 0
		expenditure = 0
		self.tableWidget.clear()
		condition = (date.today().month, )
		con = sqlite3.connect(r'.\MoneyDatabase.db')
		cur = con.cursor()
		i = cur.execute('SELECT Income FROM MoneyManagement WHERE Month=(?)', condition)
		for row_number, row_data in enumerate(i):
			for column_number, data in enumerate(row_data):
				temp = str(str(data).split(".")[0])
				data = int(temp)
				income = income + data
		e = cur.execute('SELECT Expenditure FROM MoneyManagement WHERE Month=(?)', condition)
		for row_number, row_data in enumerate(e):
			for column_number, data in enumerate(row_data):
				temp = str(str(data).split(".")[0])
				data = int(temp)
				expenditure = expenditure + data
		result = cur.execute('SELECT * FROM MoneyManagement WHERE Month=(?)', condition)	
		for row_number, row_data in enumerate(result):
			for column_number, data in enumerate(row_data):
				self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
		con.close()

		self.label_3.setText(QtWidgets.QApplication.translate("self.centralwidget", "Your Income this month is: {}".format(str(income)), None, -1))

		self.label_4.setText(QtWidgets.QApplication.translate("self.centralwidget", "Your Expenditure this month is: {}".format(str(expenditure)), None, -1))

	def getReportbyYear(self):
		income = 0
		expenditure = 0
		self.tableWidget.clear()
		condition = (date.today().year, )
		con = sqlite3.connect(r'.\MoneyDatabase.db')
		cur = con.cursor()
		i = cur.execute('SELECT Income FROM MoneyManagement WHERE Year=(?)', condition)
		for row_number, row_data in enumerate(i):
			for column_number, data in enumerate(row_data):
				temp = str(str(data).split(".")[0])
				data = int(temp)
				income = income + data
		e = cur.execute('SELECT Expenditure FROM MoneyManagement WHERE Year=(?)', condition)
		for row_number, row_data in enumerate(e):
			for column_number, data in enumerate(row_data):
				temp = str(str(data).split(".")[0])
				data = int(temp)
				expenditure = expenditure + data
		result = cur.execute('SELECT * FROM MoneyManagement WHERE Year=(?)', condition)	
		for row_number, row_data in enumerate(result):
			for column_number, data in enumerate(row_data):
				self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
		con.close()

		self.label_3.setText(QtWidgets.QApplication.translate("self.centralwidget", "Your Income this year is: {}".format(str(income)), None, -1))

		self.label_4.setText(QtWidgets.QApplication.translate("self.centralwidget", "Your Expenditure this year is: {}".format(str(expenditure)), None, -1))


if(__name__ == '__main__'):
	app = QtWidgets.QApplication(sys.argv)
	app.setStyle("Fusion")
	palette = QtGui.QPalette()
	palette.setColor(QtGui.QPalette.Window, QtGui.QColor(50,50,50))
	palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(60,224,238))
	palette.setColor(QtGui.QPalette.Base, QtGui.QColor(0,0,0))
	palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
	palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
	palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
	palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53,53,53))
	palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(60,224,238))

	app.setPalette(palette)
	app.setWindowIcon(QtGui.QIcon('./icon.jpg'))
	window = MainWidget()
	window.show()
	sys.exit(app.exec_())