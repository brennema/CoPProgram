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


sys.path.append(os.path.join(os.getcwd(),'CofPfunctions')) # add path to CofP functions to directory
import CofPfunctions


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
		self.progressTrial.setValue(0) 

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
		numpy.set_printoptions(precision=4, suppress=True) #just for now for troubleshooting
		xPos = self.lineX
		yPos = self.lineY
		zPos = self.lineZ
		plateNum = self.comboBoxFP.currentIndex()
		samplingRate = int(self.lineSampling.text())
		if plateNum == 0:
			self.forcePlateImage.setPixmap(QPixmap(str(os.path.join(self.dirCurrent,'Plates.png'))))
		elif plateNum == 1: 
			self.forcePlateImage.setPixmap(QPixmap(str(os.path.join(self.dirCurrent,'Plate1.png'))))
			try: dataFrame = pd.read_excel(str(os.path.join(self.dirCurrent,'SensitivityMatrix-FP1.xlsx')), header=None, skiprows=6, skip_footer=4, usecols=range(9,12))
			except:
				errorBox = QMessageBox.critical(self, 'File Not Found', 'The origin information for force plate #' +
					str(plateNum) + ' is not found.  This file does not exist, or may be corrupt.') #try/except for finding sensitivity matrix excel sheet
			originPlate = numpy.asarray(dataFrame)
			x = originPlate[0, 0]/1000
			y = originPlate[0, 1]/1000
			z = originPlate[0, 2]/1000
			xPos.setText(QString(str(x)))
			yPos.setText(QString(str(y)))
			zPos.setText(QString(str(z)))
		elif plateNum == 2:
			self.forcePlateImage.setPixmap(QPixmap(str(os.path.join(self.dirCurrent,'Plate2.png'))))
			try: dataFrame = pd.read_excel(str(os.path.join(self.dirCurrent,'SensitivityMatrix-FP2.xlsx')), header=None, skiprows=6, skip_footer=4, usecols=range(9,12))
			except:
				errorBox = QMessageBox.critical(self, 'File Not Found', 'The origin information for force plate #' +
					str(plateNum) + ' is not found.  This file does not exist, or may be corrupt.') #same for plate 2
			originPlate = numpy.asarray(dataFrame)
			x = originPlate[0, 0]/1000
			y = originPlate[0, 1]/1000
			z = originPlate[0, 2]/1000
			xPos.setText(QString(str(x)))
			yPos.setText(QString(str(y)))
			zPos.setText(QString(str(z)))

	def process(self):
		warnings.filterwarnings("ignore")
		numpy.set_printoptions(precision=4, suppress=True) #just for now for troubleshooting
		self.figure.clf() #clear any previous data in the results
		self.lineMeanSpeedx.setText(QString())
		self.lineMeanSpeedy.setText(QString())
		self.lineDistancex.setText(QString())
		self.lineDistancey.setText(QString())
		self.lineMSEx.setText(QString())
		self.lineMSEy.setText(QString())
		self.line005x.setText(QString())
		self.line005y.setText(QString())
		self.line01x.setText(QString())
		self.line01y.setText(QString())
		self.line025x.setText(QString())
		self.line025y.setText(QString())
		self.line05x.setText(QString())
		self.line05y.setText(QString())
		self.line075x.setText(QString())
		self.line075y.setText(QString())
		self.line09x.setText(QString())
		self.line09y.setText(QString())
		self.line095x.setText(QString())
		self.line095y.setText(QString())

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
			try: dataFrame = pd.read_excel(str(os.path.join(self.dirCurrent,'SensitivityMatrix-FP1.xlsx')), header=None, skiprows=5, usecols=range(1,7))
			except:
				errorBox = QMessageBox.critical(self, 'File Not Found', 'The sensitivity matrix for force plate #' +
					str(plateNum) + ' is not found. This file does not exist, or may be corrupt.')
			sensitivityMatrix = numpy.asarray(dataFrame)
		elif plateNum == 2:
			try: dataFrame = pd.read_excel(str(os.path.join(self.dirCurrent,'SensitivityMatrix-FP2.xlsx')), header=None, skiprows=5, usecols=range(1,7))
			except:
				errorBox = QMessageBox.critical(self, 'File Not Found', 'The sensitivity matrix for force plate #' +
					str(plateNum) + ' is not found. This file does not exist, or may be corrupt.')
			sensitivityMatrix = numpy.asarray(dataFrame)

		try: analog_data = pd.read_csv(str(fileNameTrial), sep=',', skiprows=3, usecols=range(1,13))
		except:
			errorBox = QMessageBox.critical(self, 'File Error', 'You are procssing a file named: ' +
				str(fileNameTrial) + '. This file is in the wrong format.  Choose a file with the ending: _Odau_1.csv')
			return None

		if plateNum == 1: 
			forcePlateAnalog = numpy.asarray(analog_data.loc[:,['Analog_1', 'Analog_2', 'Analog_3', 'Analog_4', 
				'Analog_5', 'Analog_6',]])
		elif plateNum == 2:
			forcePlateAnalog = numpy.asarray(analog_data.loc[:,['Analog_7', 'Analog_8', 'Analog_9', 'Analog_10', 
				'Analog_11', 'Analog_12',]])

		samplingRate = int(self.lineSampling.text())
		samplingDuration = int(self.lineDuration.text()) #added trial duration in seconds
		gain = int(self.lineGain.text())
		vMax = int(self.lineVMax.text())
		multiplier = float(self.lineMult.text())
		Zo_m = float(self.lineZ.text())/1000
		timeVel = numpy.linspace(0, samplingDuration, ((samplingRate * samplingDuration)-1)) #instead of hard-coding for specific sampling rates, durations
		forces_moments = numpy.matmul(sensitivityMatrix, forcePlateAnalog.T).T
		forces_moments = forces_moments/(gain*vMax*multiplier)

		FzChannel = forces_moments[:, 2] # Test for person on the force plate
		bodyMass = FzChannel.mean()
		if bodyMass < 300: #set really low for now; our test trials were actually collected at gain=2000 meaning calculated N values will be low
			errorBox = QMessageBox.critical(self, 'Threshold Error', 'No force detected on the force plate.  Ensure ' +
				'the correct force plate was chosen for processing.')
			return 
		else:
			pass

		CofPx = ((Zo_m * (forces_moments[:, 0])) - (forces_moments[:, 4])) / forces_moments[:, 2]
		CofPy = ((Zo_m * (forces_moments[:, 1])) - (forces_moments[:, 3])) / forces_moments[:, 2]
		centeredCofPx = CofPx - (CofPx.mean())
		centeredCofPy = CofPy - (CofPy.mean())
		velocity_x = numpy.diff(centeredCofPx) / (1./samplingRate)
		velocity_y = numpy.diff(centeredCofPy) / (1./samplingRate)
		velocity_resultant = numpy.sqrt(velocity_x**2 + velocity_y**2)
		
		framesPos = numpy.linspace(1, (samplingRate * samplingDuration), (samplingRate * samplingDuration)) #same as above
		framesVel = numpy.linspace(1, (samplingRate * samplingDuration)-1, (samplingRate * samplingDuration)-1) #same as above
		self.centredCofPx = numpy.vstack((framesPos, centeredCofPx))
		self.centredCofPy = numpy.vstack((framesPos, centeredCofPy))
		self.centredCofP = numpy.vstack((framesPos, centeredCofPx, centeredCofPy))
		self.velocityx = numpy.vstack((framesVel, velocity_x))
		self.velocityy = numpy.vstack((framesVel, velocity_y))
		self.velocity = numpy.vstack((framesVel, velocity_x, velocity_y))

		self.completed = 0
		while self.completed < 100:
			self.completed += 0.0005
			self.progressTrial.setValue(self.completed)


		distance_x_005 = CofPfunctions.getDistance_Coverage(CofPx, 0.05)
		distance_x_010 = CofPfunctions.getDistance_Coverage(CofPx, 0.1)
		distance_x_025 = CofPfunctions.getDistance_Coverage(CofPx, 0.25)
		distance_x_050 = CofPfunctions.getDistance_Coverage(CofPx, 0.5)
		distance_x_075 = CofPfunctions.getDistance_Coverage(CofPx, 0.75)
		distance_x_090 = CofPfunctions.getDistance_Coverage(CofPx, 0.9)
		distance_x_095 = CofPfunctions.getDistance_Coverage(CofPx, 0.95)

		distance_y_005 = CofPfunctions.getDistance_Coverage(CofPy, 0.05)
		distance_y_010 = CofPfunctions.getDistance_Coverage(CofPy, 0.1)
		distance_y_025 = CofPfunctions.getDistance_Coverage(CofPy, 0.25)
		distance_y_050 = CofPfunctions.getDistance_Coverage(CofPy, 0.5)
		distance_y_075 = CofPfunctions.getDistance_Coverage(CofPy, 0.75)
		distance_y_090 = CofPfunctions.getDistance_Coverage(CofPy, 0.9)
		distance_y_095 = CofPfunctions.getDistance_Coverage(CofPy, 0.95)

		distance_x = CofPfunctions.getDistanceCofP(CofPx, filter=True, freqCutoff=20, samplingRate=1000, order=2)
		distance_y = CofPfunctions.getDistanceCofP(CofPy, filter=True, freqCutoff=20, samplingRate=1000, order=2)
		distance_xy = CofPfunctions.getDistanceBothAxes(CofPx, CofPy, filter=True, freqCutoff=20, samplingRate=1000, order=2)

		speed_x = distance_x/((1./samplingRate) * len(CofPx)) 
		speed_y = distance_y/((1./samplingRate) * len(CofPy)) 
		speed_xy = distance_xy/((1./samplingRate) * len(CofPx)) 



		######### Populate these with the new variables
		self.lineMeanSpeedx.setText(QString(str.format('{0:.4f}',speed_x)))
		self.lineMeanSpeedy.setText(QString(str.format('{0:.4f}',speed_y)))
		self.lineDistancex.setText(QString(str.format('{0:.4f}',distance_x)))
		self.lineDistancey.setText(QString(str.format('{0:.4f}',distance_y)))
		#self.lineMSEx.setText(QString())
		#self.lineMSEy.setText(QString())

		self.line005x.setText(QString(str.format('{0:.4f}',distance_x_005)))
		self.line005y.setText(QString(str.format('{0:.4f}',distance_y_005)))
		self.line01x.setText(QString(str.format('{0:.4f}',distance_x_010)))
		self.line01y.setText(QString(str.format('{0:.4f}',distance_y_010)))
		self.line025x.setText(QString(str.format('{0:.4f}',distance_x_025)))
		self.line025y.setText(QString(str.format('{0:.4f}',distance_y_025)))
		self.line05x.setText(QString(str.format('{0:.4f}',distance_x_050)))
		self.line05y.setText(QString(str.format('{0:.4f}',distance_y_050)))
		self.line075x.setText(QString(str.format('{0:.4f}',distance_x_075)))
		self.line075y.setText(QString(str.format('{0:.4f}',distance_y_075)))
		self.line09x.setText(QString(str.format('{0:.4f}',distance_x_090)))
		self.line09y.setText(QString(str.format('{0:.4f}',distance_y_090)))
		self.line095x.setText(QString(str.format('{0:.4f}',distance_x_095)))
		self.line095y.setText(QString(str.format('{0:.4f}',distance_y_095)))

		ax1 = self.figure.add_subplot(131) #these subplots will change (centred COP, Vel., MSE)
		ax1.plot(CofPx, CofPy, 'k')
		ax1.set_title('CoPy vs CoPx (m)')
		ax2 = self.figure.add_subplot(132)
		ax2.plot(centeredCofPx, centeredCofPy, 'k')
		ax2.set_title('Centred CoPy vs CoPx (m)')
		ax3 = self.figure.add_subplot(133) 
		ax3.plot(timeVel, velocity_x, label="Vel x")
		ax3.plot(timeVel, velocity_y, label="Vel y")
		ax3.set_title('Vel (m/s) vs Time (s)')
		ax3.legend()
		self.canvas.draw()

	def save_results(self):
		centredCofPx = self.centredCofPx #this way, only ML or AP can be saved... or both if both are clicked
		centredCofPy = self.centredCofPy
		centredCofP = self.centredCofP
		velocityx = self.velocityx
		velocityy = self.velocityy
		velocity = self.velocity
		if self.checkBoxCOPPos.isChecked() and self.checkBoxCOPPosy.isChecked():
			datafr = pd.DataFrame(centredCofP.T, columns=['Frames', 'COPx', 'COPy'])
			filepath = str(self.lineTrialName.text()) + '_COP_Position.xlsx'
			datafr.to_excel(filepath, index=False)
		elif self.checkBoxCOPPos.isChecked():
			datafr = pd.DataFrame(centredCofPx.T, columns=['Frames', 'COPx'])
			filepath = str(self.lineTrialName.text()) + '_COP_Positionx.xlsx'
			datafr.to_excel(filepath, index=False)
		elif self.checkBoxCOPPosy.isChecked():
			datafr = pd.DataFrame(centredCofPy.T, columns=['Frames', 'COPy'])
			filepath = str(self.lineTrialName.text()) + '_COP_Positiony.xlsx'
			datafr.to_excel(filepath, index=False)
		elif not self.checkBoxCOPPos.isChecked() and self.checkBoxCOPPosy.isChecked():
			pass

		if self.checkBoxCOPVel.isChecked() and self.checkBoxCOPVely.isChecked():
			datafra = pd.DataFrame(velocity.T, columns=['Frames', 'COPx Vel.', 'COPy Vel.'])
			filepaths = str(self.lineTrialName.text()) + '_COP_Velocity.xlsx'
			datafra.to_excel(filepaths, index=False)
		elif self.checkBoxCOPVel.isChecked():
			datafra = pd.DataFrame(velocityx.T, columns=['Frames', 'COPx Vel.'])
			filepaths = str(self.lineTrialName.text()) + '_COP_Velocityx.xlsx'
			datafra.to_excel(filepaths, index=False)
		elif self.checkBoxCOPVely.isChecked():
			datafra = pd.DataFrame(velocityy.T, columns=['Frames', 'COPy Vel.'])
			filepaths = str(self.lineTrialName.text()) + '_COP_Velocityy.xlsx'
			datafra.to_excel(filepaths, index=False)
		elif not self.checkBoxCOPVel.isChecked() and self.checkBoxCOPVely.isChecked():
			pass


def main():
	app = QApplication(sys.argv)
	form = ExampleApp()
	form.show()
	app.exec_()


if __name__ == '__main__':
	main()