import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QObject


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(822, 426)

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.lineEdit = QtWidgets.QLineEdit(parent=self.centralwidget)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())

        self.show_adress = QtWidgets.QLabel(self)
        self.show_adress.setGeometry(10, 170, 170, 300)
        self.show_adress.setWordWrap(True)

        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.findButton = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.findButton.sizePolicy().hasHeightForWidth())
        self.findButton.setSizePolicy(sizePolicy)
        self.findButton.setText("")
        self.findButton.setObjectName("findButton")
        self.horizontalLayout_2.addWidget(self.findButton)

        self.clearButton = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clearButton.sizePolicy().hasHeightForWidth())
        self.clearButton.setSizePolicy(sizePolicy)
        self.clearButton.setText("")
        self.clearButton.setDefault(False)
        self.clearButton.setFlat(False)
        self.clearButton.setObjectName("clearButton")

        self.horizontalLayout_2.addWidget(self.clearButton)
        self.horizontalLayout_2.setStretch(0, 10)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.darkThemeButton = QtWidgets.QRadioButton(parent=self.centralwidget)
        self.darkThemeButton.setChecked(True)
        self.darkThemeButton.setObjectName("darkThemeButton")

        self.themeButtonGroup = QtWidgets.QButtonGroup(MainWindow)
        self.themeButtonGroup.setObjectName("themeButtonGroup")
        self.themeButtonGroup.addButton(self.darkThemeButton)
        self.verticalLayout.addWidget(self.darkThemeButton)

        self.lightThemeButton = QtWidgets.QRadioButton(parent=self.centralwidget)
        self.lightThemeButton.setObjectName("lightThemeButton")
        self.themeButtonGroup.addButton(self.lightThemeButton)
        self.verticalLayout.addWidget(self.lightThemeButton)

        self.mapTypeComboBox = QtWidgets.QComboBox(parent=self.centralwidget)
        self.mapTypeComboBox.setObjectName("mapTypeComboBox")
        self.mapTypeComboBox.addItem("")
        self.mapTypeComboBox.addItem("")
        self.mapTypeComboBox.addItem("")
        self.mapTypeComboBox.addItem("")

        self.verticalLayout.addWidget(self.mapTypeComboBox)

        self.postIndexCheckBox = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.postIndexCheckBox.setObjectName("postIndexCheckBox")

        self.verticalLayout.addWidget(self.postIndexCheckBox)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout.setStretch(4, 1)
        self.verticalLayout.setStretch(5, 10)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)

        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 5)

        MainWindow.setCentralWidget(self.centralwidget)

        self.findButton.setText('Искать')
        self.clearButton.setText('Сброс')

        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Maps API. Часть №8"))
        self.darkThemeButton.setText(_translate("MainWindow", "Темная"))
        self.lightThemeButton.setText(_translate("MainWindow", "Светлая"))
        self.mapTypeComboBox.setItemText(0, _translate("MainWindow", "Базовая карта"))
        self.mapTypeComboBox.setItemText(1, _translate("MainWindow", "Для автомобильной навигации"))
        self.mapTypeComboBox.setItemText(2, _translate("MainWindow", "Для общественного транспорта"))
        self.mapTypeComboBox.setItemText(3, _translate("MainWindow", "Административная"))
        self.postIndexCheckBox.setText(_translate("MainWindow", "Почтовый индекс"))