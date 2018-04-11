# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ForcePlateProcessing.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from HelpWindow import Ui_Dialog

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1292, 700)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 0, 1271, 655))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout = QtGui.QGridLayout(self.tab)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.forcePlateImage = QtGui.QLabel(self.tab)
        self.forcePlateImage.setObjectName(_fromUtf8("forcePlateImage"))
        self.forcePlateImage.setPixmap(QtGui.QPixmap('Plates.png'))
        self.gridLayout.addWidget(self.forcePlateImage, 1, 1, 4, 3, QtCore.Qt.AlignCenter)
        self.lineParticipant = QtGui.QLineEdit(self.tab)
        self.lineParticipant.setObjectName(_fromUtf8("lineParticipant"))
        self.gridLayout.addWidget(self.lineParticipant, 0, 0, 1, 1) #good
        self.groupBoxParameters = QtGui.QGroupBox(self.tab)
        self.groupBoxParameters.setObjectName(_fromUtf8("groupBoxParameters"))
        self.formLayout = QtGui.QFormLayout(self.groupBoxParameters)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.labelSampling = QtGui.QLabel(self.groupBoxParameters)
        self.labelSampling.setObjectName(_fromUtf8("labelSampling"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelSampling)
        self.lineSampling = QtGui.QLineEdit(self.groupBoxParameters)
        self.lineSampling.setObjectName(_fromUtf8("lineSampling"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineSampling)
        self.labelDuration = QtGui.QLabel(self.groupBoxParameters)
        self.labelDuration.setObjectName(_fromUtf8("labelDuration"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelDuration)
        self.lineDuration = QtGui.QLineEdit(self.groupBoxParameters)
        self.lineDuration.setObjectName(_fromUtf8("lineDuration"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineDuration)
        self.labelVMax = QtGui.QLabel(self.groupBoxParameters)
        self.labelVMax.setObjectName(_fromUtf8("labelVMax"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.labelVMax)
        self.lineVMax = QtGui.QLineEdit(self.groupBoxParameters)
        self.lineVMax.setAutoFillBackground(False)
        self.lineVMax.setReadOnly(True)
        self.lineVMax.setObjectName(_fromUtf8("lineVMax"))
        self.lineVMax.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.lineVMax.font()      
        font.setPointSize(10)               
        self.lineVMax.setFont(font)  
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineVMax)
        self.labelGain = QtGui.QLabel(self.groupBoxParameters)
        self.labelGain.setObjectName(_fromUtf8("labelGain"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.labelGain)
        self.lineGain = QtGui.QLineEdit(self.groupBoxParameters)
        self.lineGain.setReadOnly(True)
        self.lineGain.setObjectName(_fromUtf8("lineGain"))
        self.lineGain.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.lineGain.font()      
        font.setPointSize(10)               
        self.lineGain.setFont(font) 
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineGain)
        self.labelMult = QtGui.QLabel(self.groupBoxParameters)
        self.labelMult.setObjectName(_fromUtf8("labelMult"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.labelMult)
        self.lineMult = QtGui.QLineEdit(self.groupBoxParameters)
        self.lineMult.setReadOnly(True)
        self.lineMult.setObjectName(_fromUtf8("lineMult"))
        self.lineMult.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.lineMult.font()      
        font.setPointSize(10)               
        self.lineMult.setFont(font) 
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.lineMult)
        self.labelX = QtGui.QLabel(self.groupBoxParameters)
        self.labelX.setObjectName(_fromUtf8("labelX"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.labelX)
        self.lineX = QtGui.QLineEdit(self.groupBoxParameters)
        self.lineX.setReadOnly(True)
        self.lineX.setObjectName(_fromUtf8("lineX"))
        self.lineX.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.lineX.font()      
        font.setPointSize(10)               
        self.lineX.setFont(font) 
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.lineX)
        self.labelY = QtGui.QLabel(self.groupBoxParameters)
        self.labelY.setObjectName(_fromUtf8("labelY"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.labelY)
        self.lineY = QtGui.QLineEdit(self.groupBoxParameters)
        self.lineY.setReadOnly(True)
        self.lineY.setObjectName(_fromUtf8("lineY"))
        self.lineY.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.lineY.font()      
        font.setPointSize(10)               
        self.lineY.setFont(font) 
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.lineY)
        self.labelZ = QtGui.QLabel(self.groupBoxParameters)
        self.labelZ.setObjectName(_fromUtf8("labelZ"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.labelZ)
        self.lineZ = QtGui.QLineEdit(self.groupBoxParameters)
        self.lineZ.setReadOnly(True)
        self.lineZ.setObjectName(_fromUtf8("lineZ"))
        self.lineZ.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.lineZ.font()      
        font.setPointSize(10)               
        self.lineZ.setFont(font) 
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.lineZ)
        self.gridLayout.addWidget(self.groupBoxParameters, 4, 0, 2, 1)
        self.labelDirectory = QtGui.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelDirectory.setFont(font)
        self.labelDirectory.setObjectName(_fromUtf8("labelDirectory"))
        self.gridLayout.addWidget(self.labelDirectory, 1, 0, 1, 1)
        self.comboBoxFP = QtGui.QComboBox(self.tab)
        self.comboBoxFP.setObjectName(_fromUtf8("comboBoxFP"))
        self.comboBoxFP.addItem(_fromUtf8(""))
        self.comboBoxFP.addItem(_fromUtf8(""))
        self.comboBoxFP.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBoxFP, 3, 0, 1, 1)
        self.listDirectory = QtGui.QListWidget(self.tab)
        self.listDirectory.setObjectName(_fromUtf8("listDirectory"))
        self.gridLayout.addWidget(self.listDirectory, 2, 0, 1, 1)
        self.progressTrial = QtGui.QProgressBar(self.tab)
        self.progressTrial.setProperty("value", 0)
        self.progressTrial.setObjectName(_fromUtf8("progressTrial"))
        self.gridLayout.addWidget(self.progressTrial, 5, 1, 1, 1)
        self.lineTrialName = QtGui.QLineEdit(self.tab)
        self.lineTrialName.setObjectName(_fromUtf8("lineTrialName"))
        self.gridLayout.addWidget(self.lineTrialName, 5, 2, 1, 1)
        self.pushProcess = QtGui.QPushButton(self.tab)
        self.pushProcess.setObjectName(_fromUtf8("pushProcess"))
        self.gridLayout.addWidget(self.pushProcess, 5, 3, 1, 1)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))

        # Define second tab
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.formLayoutResults = QtGui.QFormLayout(self.tab_2)
        self.formLayoutResults.setObjectName(_fromUtf8("formLayoutResults"))
        # First groupbox - Results
        self.groupBoxResults = QtGui.QGroupBox(self.tab_2) 
        self.groupBoxResults.setObjectName(_fromUtf8("groupBoxResults"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBoxResults)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lineMeanSpeedy = QtGui.QLineEdit(self.groupBoxResults) 
        self.lineMeanSpeedy.setReadOnly(True)
        self.lineMeanSpeedy.setObjectName(_fromUtf8("lineMeanSpeedy"))
        self.lineMeanSpeedy.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.lineMeanSpeedy.font()      
        font.setPointSize(10)               
        self.lineMeanSpeedy.setFont(font) 
        self.gridLayout_2.addWidget(self.lineMeanSpeedy, 4, 1, 1, 1)
        self.labelSpeed = QtGui.QLabel(self.groupBoxResults) 
        self.labelSpeed.setObjectName(_fromUtf8("labelSpeed"))
        self.gridLayout_2.addWidget(self.labelSpeed, 0, 1, 1, 1)
        self.labelMSE = QtGui.QLabel(self.groupBoxResults) 
        self.labelMSE.setObjectName(_fromUtf8("labelMSE"))
        self.gridLayout_2.addWidget(self.labelMSE, 0, 3, 1, 1)
        self.lineDistancex = QtGui.QLineEdit(self.groupBoxResults) 
        self.lineDistancex.setReadOnly(True)
        self.lineDistancex.setObjectName(_fromUtf8("lineDistancex"))
        self.lineDistancex.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.lineDistancex.font()      
        font.setPointSize(10)               
        self.lineDistancex.setFont(font) 
        self.gridLayout_2.addWidget(self.lineDistancex, 2, 2, 1, 1)
        self.labelDistance = QtGui.QLabel(self.groupBoxResults) 
        self.labelDistance.setObjectName(_fromUtf8("labelDistance"))
        self.gridLayout_2.addWidget(self.labelDistance, 0, 2, 1, 1)
        self.lineMSEx = QtGui.QLineEdit(self.groupBoxResults) 
        self.lineMSEx.setReadOnly(True)
        self.lineMSEx.setObjectName(_fromUtf8("lineMSEx"))
        self.lineMSEx.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.lineMSEx.font()      
        font.setPointSize(10)               
        self.lineMSEx.setFont(font) 
        self.gridLayout_2.addWidget(self.lineMSEx, 2, 3, 1, 1)
        self.labelCOPy = QtGui.QLabel(self.groupBoxResults) 
        self.labelCOPy.setObjectName(_fromUtf8("labelCOPy"))
        self.gridLayout_2.addWidget(self.labelCOPy, 4, 0, 1, 1)
        self.labelCOPx = QtGui.QLabel(self.groupBoxResults) 
        self.labelCOPx.setObjectName(_fromUtf8("labelCOPy"))
        self.gridLayout_2.addWidget(self.labelCOPx, 2, 0, 1, 1)
        self.lineMeanSpeedx = QtGui.QLineEdit(self.groupBoxResults) 
        self.lineMeanSpeedx.setReadOnly(True)
        self.lineMeanSpeedx.setObjectName(_fromUtf8("lineMeanSpeedx"))
        self.lineMeanSpeedx.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.lineMeanSpeedx.font()      
        font.setPointSize(10)               
        self.lineMeanSpeedx.setFont(font) 
        self.gridLayout_2.addWidget(self.lineMeanSpeedx, 2, 1, 1, 1)
        self.lineMSEy = QtGui.QLineEdit(self.groupBoxResults) 
        self.lineMSEy.setReadOnly(True)
        self.lineMSEy.setObjectName(_fromUtf8("lineMSEy"))
        self.lineMSEy.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.lineMSEy.font()      
        font.setPointSize(10)               
        self.lineMSEy.setFont(font) 
        self.gridLayout_2.addWidget(self.lineMSEy, 4, 3, 1, 1)
        self.lineDistancey = QtGui.QLineEdit(self.groupBoxResults) 
        self.lineDistancey.setReadOnly(True)
        self.lineDistancey.setObjectName(_fromUtf8("lineDistancey"))
        self.lineDistancey.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.lineDistancey.font()      
        font.setPointSize(10)               
        self.lineDistancey.setFont(font) 
        self.gridLayout_2.addWidget(self.lineDistancey, 4, 2, 1, 1)
        self.formLayoutResults.setWidget(2, QtGui.QFormLayout.LabelRole, self.groupBoxResults)
        # Second groupbox - Save Results
        self.groupBoxSave = QtGui.QGroupBox(self.tab_2)
        self.groupBoxSave.setObjectName(_fromUtf8("groupBoxSave"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBoxSave)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.checkBoxCOPPos = QtGui.QCheckBox(self.groupBoxSave)
        self.checkBoxCOPPos.setObjectName(_fromUtf8("checkBoxCOPPos"))
        self.gridLayout_3.addWidget(self.checkBoxCOPPos, 0, 0, 1, 1)
        self.checkBoxCOPVel = QtGui.QCheckBox(self.groupBoxSave)
        self.checkBoxCOPVel.setObjectName(_fromUtf8("checkBoxCOPVel"))
        self.gridLayout_3.addWidget(self.checkBoxCOPVel, 1, 0, 1, 1)
        self.checkBoxMSE = QtGui.QCheckBox(self.groupBoxSave)
        self.checkBoxMSE.setObjectName(_fromUtf8("checkBoxMSE"))
        self.gridLayout_3.addWidget(self.checkBoxMSE, 2, 0, 1, 1)
        self.checkBoxTable = QtGui.QCheckBox(self.groupBoxSave)
        self.checkBoxTable.setObjectName(_fromUtf8("checkBoxTable"))
        self.gridLayout_3.addWidget(self.checkBoxTable, 3, 0, 1, 1)
        self.pushSave = QtGui.QPushButton(self.groupBoxSave)
        self.pushSave.setObjectName(_fromUtf8("pushSave"))
        self.gridLayout_3.addWidget(self.pushSave, 4, 0, 1, 1)
        self.formLayoutResults.setWidget(3, QtGui.QFormLayout.LabelRole, self.groupBoxSave)

        # add static text
        self.textFPHelp = QtGui.QTextEdit(self.tab_2)
        self.textFPHelp.setReadOnly(True)
        textFP = ("\n"
            "                                                                                                    NOTE \n"
            "                                         -------------------------------------------------------------------------------------------------------------\n"
            "                                                   If the participant is facing the back wall (or toward the force plate equipment):\n"
            "                                                                                          CoPx = A/P direction \n"
            "                                                                                          CoPy = M/L direction \n"
            "                                           If the participant is facing the wall with the collection computer (or toward the wall partition): \n"
            "                                                                                          CoPx = M/L direction \n"
            "                                                                                          CoPy = A/P direction \n")
        self.textFPHelp.setText(textFP)
        #self.gridLayout_3.addWidget(self.textFPHelp, 0, 1, 4, 1)
        self.formLayoutResults.setWidget(3, QtGui.QFormLayout.FieldRole, self.textFPHelp)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        MainWindow.setCentralWidget(self.centralwidget)
        # Third groupbox - Excursion Results
        self.groupBoxResults2 = QtGui.QGroupBox(self.tab_2) 
        self.groupBoxResults2.setGeometry(QtCore.QRect(480, 10, 721, 111))
        self.groupBoxResults2.setObjectName(_fromUtf8("groupBoxResults2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBoxResults2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label05 = QtGui.QLabel(self.groupBoxResults2) 
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label05.setFont(font)
        self.label05.setObjectName(_fromUtf8("label05"))
        self.gridLayout_3.addWidget(self.label05, 0, 5, 1, 1)
        self.label09 = QtGui.QLabel(self.groupBoxResults2) 
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label09.setFont(font)
        self.label09.setObjectName(_fromUtf8("label09"))
        self.gridLayout_3.addWidget(self.label09, 0, 7, 1, 1)
        self.line095y = QtGui.QLineEdit(self.groupBoxResults2) 
        self.line095y.setReadOnly(True)
        self.line095y.setObjectName(_fromUtf8("line095y"))
        self.line095y.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.line095y.font()      
        font.setPointSize(10)               
        self.line095y.setFont(font) 
        self.gridLayout_3.addWidget(self.line095y, 3, 8, 1, 1)
        self.label075 = QtGui.QLabel(self.groupBoxResults2) 
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label075.setFont(font)
        self.label075.setObjectName(_fromUtf8("label075"))
        self.gridLayout_3.addWidget(self.label075, 0, 6, 1, 1)
        self.line09y = QtGui.QLineEdit(self.groupBoxResults2) 
        self.line09y.setReadOnly(True)
        self.line09y.setObjectName(_fromUtf8("line09y"))
        self.line09y.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.line09y.font()      
        font.setPointSize(10)               
        self.line09y.setFont(font) 
        self.gridLayout_3.addWidget(self.line09y, 3, 7, 1, 1)
        self.line01x = QtGui.QLineEdit(self.groupBoxResults2) 
        self.line01x.setReadOnly(True)
        self.line01x.setObjectName(_fromUtf8("line01x"))
        self.line01x.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.line01x.font()      
        font.setPointSize(10)               
        self.line01x.setFont(font) 
        self.gridLayout_3.addWidget(self.line01x, 1, 3, 1, 1)
        self.line005x = QtGui.QLineEdit(self.groupBoxResults2) 
        self.line005x.setReadOnly(True)
        self.line005x.setObjectName(_fromUtf8("line005x"))
        self.line005x.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.line005x.font()      
        font.setPointSize(10)               
        self.line005x.setFont(font) 
        self.gridLayout_3.addWidget(self.line005x, 1, 2, 1, 1)
        self.labelCOPx2 = QtGui.QLabel(self.groupBoxResults2) 
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelCOPx2.setFont(font)
        self.labelCOPx2.setObjectName(_fromUtf8("labelCOPx2"))
        self.gridLayout_3.addWidget(self.labelCOPx2, 1, 1, 1, 1)
        self.labelCOPy2 = QtGui.QLabel(self.groupBoxResults2) 
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelCOPy2.setFont(font)
        self.labelCOPy2.setObjectName(_fromUtf8("labelCOPy2"))
        self.gridLayout_3.addWidget(self.labelCOPy2, 3, 1, 1, 1)
        self.line05x = QtGui.QLineEdit(self.groupBoxResults2) 
        self.line05x.setReadOnly(True)
        self.line05x.setObjectName(_fromUtf8("line05x"))
        self.line05x.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.line05x.font()      
        font.setPointSize(10)               
        self.line05x.setFont(font) 
        self.gridLayout_3.addWidget(self.line05x, 1, 5, 1, 1)
        self.line005y = QtGui.QLineEdit(self.groupBoxResults2) 
        self.line005y.setReadOnly(True)
        self.line005y.setObjectName(_fromUtf8("line005y"))
        self.line005y.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.line005y.font()      
        font.setPointSize(10)               
        self.line005y.setFont(font) 
        self.gridLayout_3.addWidget(self.line005y, 3, 2, 1, 1)
        self.line025x = QtGui.QLineEdit(self.groupBoxResults2) 
        self.line025x.setReadOnly(True)
        self.line025x.setObjectName(_fromUtf8("line025x"))
        self.line025x.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.line025x.font()      
        font.setPointSize(10)               
        self.line025x.setFont(font) 
        self.gridLayout_3.addWidget(self.line025x, 1, 4, 1, 1)
        self.line025y = QtGui.QLineEdit(self.groupBoxResults2) 
        self.line025y.setReadOnly(True)
        self.line025y.setObjectName(_fromUtf8("line025y"))
        self.line025y.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.line025y.font()      
        font.setPointSize(10)               
        self.line025y.setFont(font) 
        self.gridLayout_3.addWidget(self.line025y, 3, 4, 1, 1)
        self.line01y = QtGui.QLineEdit(self.groupBoxResults2) 
        self.line01y.setReadOnly(True)
        self.line01y.setObjectName(_fromUtf8("line01y"))
        self.line01y.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.line01y.font()      
        font.setPointSize(10)               
        self.line01y.setFont(font) 
        self.gridLayout_3.addWidget(self.line01y, 3, 3, 1, 1)
        self.line05y = QtGui.QLineEdit(self.groupBoxResults2) 
        self.line05y.setReadOnly(True)
        self.line05y.setObjectName(_fromUtf8("line05y"))
        self.line05y.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.line05y.font()      
        font.setPointSize(10)               
        self.line05y.setFont(font) 
        self.gridLayout_3.addWidget(self.line05y, 3, 5, 1, 1)
        self.line075y = QtGui.QLineEdit(self.groupBoxResults2) 
        self.line075y.setReadOnly(True)
        self.line075y.setObjectName(_fromUtf8("line075y"))
        self.line075y.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.line075y.font()      
        font.setPointSize(10)               
        self.line075y.setFont(font) 
        self.gridLayout_3.addWidget(self.line075y, 3, 6, 1, 1)
        self.line09x = QtGui.QLineEdit(self.groupBoxResults2) 
        self.line09x.setReadOnly(True)
        self.line09x.setObjectName(_fromUtf8("line09x"))
        self.line09x.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.line09x.font()      
        font.setPointSize(10)               
        self.line09x.setFont(font) 
        self.gridLayout_3.addWidget(self.line09x, 1, 7, 1, 1)
        self.line075x = QtGui.QLineEdit(self.groupBoxResults2) 
        self.line075x.setReadOnly(True)
        self.line075x.setObjectName(_fromUtf8("line075x"))
        self.line075x.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.line075x.font()      
        font.setPointSize(10)               
        self.line075x.setFont(font) 
        self.gridLayout_3.addWidget(self.line075x, 1, 6, 1, 1)
        self.label01 = QtGui.QLabel(self.groupBoxResults2) 
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label01.setFont(font)
        self.label01.setObjectName(_fromUtf8("label01"))
        self.gridLayout_3.addWidget(self.label01, 0, 3, 1, 1)
        self.label005 = QtGui.QLabel(self.groupBoxResults2) 
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label005.setFont(font)
        self.label005.setObjectName(_fromUtf8("label005"))
        self.gridLayout_3.addWidget(self.label005, 0, 2, 1, 1)
        self.label025 = QtGui.QLabel(self.groupBoxResults2) 
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label025.setFont(font)
        self.label025.setObjectName(_fromUtf8("label025"))
        self.gridLayout_3.addWidget(self.label025, 0, 4, 1, 1)
        self.line095x = QtGui.QLineEdit(self.groupBoxResults2) 
        self.line095x.setReadOnly(True)
        self.line095x.setObjectName(_fromUtf8("line095x"))
        self.line095x.setStyleSheet("QLineEdit { background-color : rgb(211, 211, 211); }")
        font = self.line095x.font()      
        font.setPointSize(10)               
        self.line095x.setFont(font) 
        self.gridLayout_3.addWidget(self.line095x, 1, 8, 1, 1)
        self.label095 = QtGui.QLabel(self.groupBoxResults2) 
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label095.setFont(font)
        self.label095.setObjectName(_fromUtf8("label095"))
        self.gridLayout_3.addWidget(self.label095, 0, 8, 1, 1)
        self.formLayoutResults.setWidget(2, QtGui.QFormLayout.FieldRole, self.groupBoxResults2)
        # Figure
        self.figure = plt.figure()    
        self.canvas = FigureCanvas(self.figure)     
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.formLayoutResults.setWidget(0, QtGui.QFormLayout.SpanningRole, self.canvas)
        self.formLayoutResults.setWidget(1, QtGui.QFormLayout.SpanningRole, self.toolbar)
        # Menu bar characterization
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1292, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_Directory = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.actionOpen_Directory.setFont(font)
        self.actionOpen_Directory.setObjectName(_fromUtf8("actionOpen_Directory"))
        self.actionOpen_Trial = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.actionOpen_Trial.setFont(font)
        self.actionOpen_Trial.setObjectName(_fromUtf8("actionOpen_Trial"))
        self.actionQuit_Application = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.actionQuit_Application.setFont(font)
        self.actionQuit_Application.setObjectName(_fromUtf8("actionQuit_Application"))
        self.actionAbout = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.actionAbout.setFont(font)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.menuFile.addAction(self.actionOpen_Directory)
        self.menuFile.addAction(self.actionOpen_Trial)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit_Application)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addSeparator()
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Centre of Pressure Program", None))
        MainWindow.setWindowIcon(QtGui.QIcon('python-icon_1_orig.png'))
        self.groupBoxParameters.setTitle(_translate("MainWindow", "Force Plate Parameters", None))
        self.lineParticipant.setText(_translate("MainWindow", "Enter Participant Code", None))
        self.labelSampling.setText(_translate("MainWindow", "Sampling Rate (Hz)", None))
        self.lineSampling.setText(_translate("MainWindow", "1000", None))
        self.labelDuration.setText(_translate("MainWindow", "Trial Duration (s)", None))
        self.lineDuration.setText(_translate("MainWindow", "30", None))
        self.labelVMax.setText(_translate("MainWindow", "Voltage Maximum", None))
        self.lineVMax.setText(_translate("MainWindow", "10", None))
        self.labelGain.setText(_translate("MainWindow", "Gain", None))
        self.lineGain.setText(_translate("MainWindow", "4000", None))
        self.labelMult.setText(_translate("MainWindow", "Multiplier", None))
        self.lineMult.setText(_translate("MainWindow", "0.000001", None))
        self.labelX.setText(_translate("MainWindow", "xOrigin (m)", None))
        self.labelY.setText(_translate("MainWindow", "yOrigin (m)", None))
        self.labelZ.setText(_translate("MainWindow", "zOrigin (m)", None))
        self.labelDirectory.setText(_translate("MainWindow", "Directory List", None))
        self.comboBoxFP.setItemText(0, _translate("MainWindow", "Choose Force Plate", None))
        self.comboBoxFP.setItemText(1, _translate("MainWindow", "Force Plate #1", None))
        self.comboBoxFP.setItemText(2, _translate("MainWindow", "Force Plate #2", None))
        self.pushProcess.setText(_translate("MainWindow", "Process Trial", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Set-up Processing Parameters", None))
        self.groupBoxResults.setTitle(_translate("MainWindow", "Results", None))
        self.labelSpeed.setText(_translate("MainWindow", "Mean Speed", None))
        self.labelMSE.setText(_translate("MainWindow", "MSE", None))
        self.labelDistance.setText(_translate("MainWindow", "Distance", None))
        self.labelCOPy.setText(_translate("MainWindow", "CoPy", None))
        self.labelCOPx.setText(_translate("MainWindow", "CoPx", None))
        self.groupBoxSave.setTitle(_translate("MainWindow", "Save", None))
        self.checkBoxCOPPos.setText(_translate("MainWindow", "CoP Position (m)", None))
        self.checkBoxCOPVel.setText(_translate("MainWindow", "CoP Velocity (m/s)", None))
        self.checkBoxMSE.setText(_translate("MainWindow", "Multi-Scale Entropy", None))
        self.checkBoxTable.setText(_translate("MainWindow", "Mean Speed, Distance, Coverage", None))
        self.pushSave.setText(_translate("MainWindow", "Save Results", None))
        self.groupBoxResults2.setTitle(_translate("MainWindow", "CoP Coverage", None))
        self.label05.setText(_translate("MainWindow", "50%", None))
        self.label09.setText(_translate("MainWindow", "90%", None))
        self.label075.setText(_translate("MainWindow", "75%", None))
        self.labelCOPx2.setText(_translate("MainWindow", "CoPx", None))
        self.labelCOPy2.setText(_translate("MainWindow", "CoPy", None))
        self.label01.setText(_translate("MainWindow", "10%", None))
        self.label005.setText(_translate("MainWindow", "5%", None))
        self.label025.setText(_translate("MainWindow", "25%", None))
        self.label095.setText(_translate("MainWindow", "95%", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Results", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.actionOpen_Directory.setText(_translate("MainWindow", "Open Directory", None))
        self.actionOpen_Trial.setText(_translate("MainWindow", "Open Trial", None))
        self.actionQuit_Application.setText(_translate("MainWindow", "Quit Application", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

