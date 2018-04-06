from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import os
import numpy
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import warnings

import ProgramGeometry #imports layout from QtDesigner
from HelpWindow import Ui_Dialog


class ExampleApp(QMainWindow, ProgramGeometry.Ui_MainWindow):
	def __init__(self, parent=None):
		super(ExampleApp, self).__init__(parent)
		self.setupUi(self)
		QApplication.setStyle(QStyleFactory.create("Cleanlooks"))
		self.dirCurrent = os.getcwd()

		# Define menu bar actions
		self.actionQuit_Application.setShortcut("Ctrl+Q")
		self.actionQuit_Application.setStatusTip('Leave the Application')
		self.actionQuit_Application.triggered.connect(self.close_application)

		self.actionOpen_Trial.setShortcut("Ctrl+O")
		self.actionOpen_Trial.setStatusTip('Open Trial for Processing')
		self.actionOpen_Trial.triggered.connect(self.trial_open)

		self.actionOpen_Directory.setShortcut("Ctrl+D")
		self.actionOpen_Directory.setStatusTip('Open Directory Containing Trials for Processing')
		self.actionOpen_Directory.triggered.connect(self.browse_folder)

		self.actionAbout.setShortcut("Ctrl+H")
		self.actionAbout.setStatusTip('Program help and contact information')
		self.actionAbout.triggered.connect(self.help)

		# Select trial from list widget
		QObject.connect(self.listDirectory, SIGNAL("itemClicked(QListWidgetItem *)"), self.trial_select_list)

		# Combo box
		self.comboBoxFP.currentIndexChanged.connect(self.force_plate)

		# Progress bar and processing button
		self.pushProcess.clicked.connect(self.process)

		# Save push bar
		self.pushSave.clicked.connect(self.save_results)


	# Executables
	def close_application(self):
		choice = QMessageBox.question(self, 'Quit',
			"Are you sure you want to quit the application?",
			QMessageBox.Yes | QMessageBox.No)
		if choice == QMessageBox.Yes:
			sys.exit()
		else:
			pass

	def help(self):
		self.helpwindow = QDialog()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self.helpwindow)
		self.helpwindow.show()

	def browse_folder(self):
		self.listDirectory.clear()
		direct = QFileDialog.getExistingDirectory(self, 
			"Pick a folder")

		if direct:
			for file_name in os.listdir(direct): 
				self.listDirectory.addItem(file_name)

		os.chdir(str(direct))

	def trial_select_list(self):
		fileNameTrial = self.listDirectory.currentItem().text()
		trialSelect = QMessageBox.question(self, 'Trial select',
			"You have chosen: " + str(fileNameTrial) + " to process.  "\
			"Is this correct?",
			QMessageBox.Yes | QMessageBox.No)
		if trialSelect == QMessageBox.Yes:
			trialName = fileNameTrial
			self.lineTrialName.setText(QString(trialName))
		else:
			trialName = []
			pass

	def trial_open(self):
		trialSel = QFileDialog.getOpenFileName(self, "Choose Trial")

		if trialSel:
			trial = QMessageBox.question(self, 'Trial select',
			"You have chosen: " + str(trialSel) + " to process.  "\
			"Is this correct?",
			QMessageBox.Yes | QMessageBox.No)
			if trial == QMessageBox.Yes:
				trialName = trialSel
				self.lineTrialName.setText(QString(trialName))
			else:
				trialName = []
				pass

	def force_plate(self): 
		xPos = self.lineX
		yPos = self.lineY
		zPos = self.lineZ
		plateNum = self.comboBoxFP.currentIndex()
		samplingRate = int(self.lineSampling.text())
		if plateNum == 0:
			self.forcePlateImage.setPixmap(QPixmap(str(self.dirCurrent) + '\Plates.png'))
		elif plateNum == 1: 
			self.forcePlateImage.setPixmap(QPixmap(str(self.dirCurrent) + '\Plate1.png'))
			x = 0.5/1000
			y = -0.5/1000
			z = -41.4/1000
			xPos.setText(QString(str(x)))
			yPos.setText(QString(str(y)))
			zPos.setText(QString(str(z)))
		elif plateNum == 2:
			self.forcePlateImage.setPixmap(QPixmap(str(self.dirCurrent) + '\Plate2.png'))
			x = -0.2/1000
			y = 0.6/1000
			z = -39.8/1000
			xPos.setText(QString(str(x)))
			yPos.setText(QString(str(y)))
			zPos.setText(QString(str(z)))

	def process(self):
		warnings.filterwarnings("ignore")
		self.figure.clf() #clear any previous data in the results
		self.lineMeanCOPx.setText(QString())
		self.lineMeanCOPy.setText(QString())
		self.lineSDCOPx.setText(QString())
		self.lineSDCOPy.setText(QString())
		self.lineCOVCOPx.setText(QString())
		self.lineCOVCOPy.setText(QString())
		self.lineMinCOPx.setText(QString())
		self.lineMinCOPy.setText(QString())
		self.lineMaxCOPx.setText(QString())
		self.lineMaxCOPy.setText(QString())

		fileNameTrial = self.lineTrialName.text()
		if len(fileNameTrial) <= 1:
			noTrial = QMessageBox.warning(self, 'Warning', 
				"No trial chosen!  Please select a trial to continue processing.",
				QMessageBox.Ok)
			return
		else:
			pass

		plateNum = self.comboBoxFP.currentIndex()
		if plateNum == 0:
			noTrial = QMessageBox.warning(self, 'Warning',
				"No force plate chosen!  Please select a force plate to continue processing.",
				QMessageBox.Ok)
			return
		elif plateNum == 1: 
			sensitivityMatrix = numpy.array([[1.4783, -0.0058, 0.0063, 0.0004, 0.0001, 0], 
				[0.0075, 1.4736, 0.0111, 0.0005, 0, 0], [0.0141, -0.0151, 5.8125, -0.0079, 0.0011, -0.0012],
				[0.0020, -0.0024, 0.0016, 0.5868, -0.0014, 0.0002], [0.0029, -0.0013, 0.0057, -0.0002, 0.5875, 0.0003],
				[0.0011, 0.0049, 0.0009, -0.0017, -0.0006, 0.2955]])
		elif plateNum == 2:
			sensitivityMatrix = numpy.array([[1.4836, -0.0013, 0.0118, 0.0001, 0.0003, 0], 
				[-0.0015, 1.4831, 0.0161, 0.0002, 0.0008, 0], [0.0161, 0.0097, 5.8133, 0.0051, 0.0002, 0.0003],
				[0.0071, -0.0028, 0.0069, 0.5908, 0.0043, -0.0003], [0.0138, 0.0054, -0.0048, 0.0026, 0.5938, 0.0007],
				[0.0011, 0.0063, 0.0003, -0.0030, 0.0011, 0.2978]]) 
		
		analog_data = pd.read_csv(str(fileNameTrial), sep=',', skiprows=3, usecols=range(1,13))
		if plateNum == 1: 
			forcePlateAnalog = numpy.asarray(analog_data.loc[:,['Analog_1', 'Analog_2', 'Analog_3', 'Analog_4', 
				'Analog_5', 'Analog_6',]])
		elif plateNum == 2:
			forcePlateAnalog = numpy.asarray(analog_data.loc[:,['Analog_7', 'Analog_8', 'Analog_9', 'Analog_10', 
				'Analog_11', 'Analog_12',]])

		samplingRate = int(self.lineSampling.text())
		gain = int(self.lineGain.text())
		vMax = int(self.lineVMax.text())
		multiplier = float(self.lineMult.text())
		Zo_m = float(self.lineZ.text())/1000
		timeVel = numpy.linspace(0, 30, 29999)
		forces_moments = numpy.matmul(sensitivityMatrix, forcePlateAnalog.T).T
		forces_moments = forces_moments/(gain*vMax*multiplier)
		CofPx = ((Zo_m * (forces_moments[:, 0])) - (forces_moments[:, 4])) / forces_moments[:, 2]
		CofPy = ((Zo_m * (forces_moments[:, 1])) - (forces_moments[:, 3])) / forces_moments[:, 2]
		meanCOPx = str(round(CofPx.mean(), 4))
		meanCOPy = str(round(CofPy.mean(), 4))
		stdCOPx = str(round(CofPx.std(), 4))
		stdCOPy = str(round(CofPy.std(), 4))
		covCOPx = str(round(CofPx.std()/CofPx.mean() * 100, 4))
		covCOPy = str(round(CofPy.std()/CofPy.mean() * 100, 4))
		minCOPx = str(round(CofPx.min(), 4))
		minCOPy = str(round(CofPy.min(), 4))
		maxCOPx = str(round(CofPx.max(), 4))
		maxCOPy = str(round(CofPy.max(), 4))

		centeredCofPx = CofPx - (CofPx.mean())
		centeredCofPy = CofPy - (CofPy.mean())

		velocity_x = numpy.diff(centeredCofPx) / (1./samplingRate)
		velocity_y = numpy.diff(centeredCofPy) / (1./samplingRate)
		velocity_resultant = numpy.sqrt(velocity_x**2 + velocity_y**2)
		
		framesPos = numpy.linspace(1, 30000, 30000)
		framesVel = numpy.linspace(1, 29999, 29999)
		self.centredCofP = numpy.vstack((framesPos, centeredCofPx, centeredCofPy))
		self.velocity = numpy.vstack((framesVel, velocity_x, velocity_y))

		self.completed = 0
		while self.completed < 100:
			self.completed += 0.0005
			self.progressTrial.setValue(self.completed)

		self.lineMeanCOPx.setText(QString(meanCOPx))
		self.lineMeanCOPy.setText(QString(meanCOPy))
		self.lineSDCOPx.setText(QString(stdCOPx))
		self.lineSDCOPy.setText(QString(stdCOPy))
		self.lineCOVCOPx.setText(QString(covCOPx))
		self.lineCOVCOPy.setText(QString(covCOPy))
		self.lineMinCOPx.setText(QString(minCOPx))
		self.lineMinCOPy.setText(QString(minCOPy))
		self.lineMaxCOPx.setText(QString(maxCOPx))
		self.lineMaxCOPy.setText(QString(maxCOPy))

		ax1 = self.figure.add_subplot(131)
		ax1.plot(CofPx, CofPy, 'k')
		ax1.set_title('CoPy vs CoPx (m)')
		ax2 = self.figure.add_subplot(132)
		ax2.plot(centeredCofPx, centeredCofPy, 'k')
		ax2.set_title('Centred CoPy vs CoPx (m)')
		ax3 = self.figure.add_subplot(133) 
		ax3.plot(timeVel, velocity_x, label="Vel x")
		ax3.plot(timeVel, velocity_y, label="Vel y")
		ax3.set_title('CoP Velocity (m/s) vs Time (s)')
		ax3.legend()
		self.canvas.draw()

	def save_results(self):
		centredCofP = self.centredCofP
		velocity = self.velocity
		if self.checkBoxCOPPos.isChecked():
			datafr = pd.DataFrame(centredCofP.T, columns=['Frames', 'COPx', 'COPy'])
			filepath = str(self.lineTrialName.text()) + '_COP_Position.xlsx'
			datafr.to_excel(filepath, index=False)
		elif not self.checkBoxCOPPos.isChecked():
			pass

		if self.checkBoxCOPVel.isChecked():
			datafra = pd.DataFrame(velocity.T, columns=['Frames', 'COPx Vel.', 'COPy Vel.'])
			filepaths = str(self.lineTrialName.text()) + '_COP_Velocity.xlsx'
			datafra.to_excel(filepaths, index=False)
		elif not self.checkBoxCOPVel.isChecked():
			pass


def main():
	app = QApplication(sys.argv)
	form = ExampleApp()
	form.show()
	app.exec_()


if __name__ == '__main__':
	main()