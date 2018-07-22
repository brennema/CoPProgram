from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import os
import time
import numpy
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from scipy.sparse.csgraph import _validation
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

		# Connect participant code 
		self.lineParticipant.returnPressed.connect(self.participant)
		self.participant = None

		# Connect trial select
		QObject.connect(self.listDirectory, SIGNAL("itemClicked(QListWidgetItem *)"), self.trial_select_list)

		# Connect combobox index change 
		self.comboBoxFP.currentIndexChanged.connect(self.force_plate)

		# Connect progress bar and processing button
		self.pushProcess.clicked.connect(self.process)

		# Connect save results push button
		self.pushSave.clicked.connect(self.save_results)

		# Connect 'X' close button on main window
		self.connect(self, SIGNAL('triggered()'), self.closeEvent)


	def close_application(self):
		'''
		In the menu bar, there is an option to quit the application.  A pop-up window will appear to ask the user to 
		confirm whether they want to close.  A shortcut of Ctrl+q has also been set for this execution.
		'''
		choice = QMessageBox.question(self, 'Quit',
			"Are you sure you want to quit the application?  Make sure you have saved your data!",
			QMessageBox.Yes | QMessageBox.No)
		if choice == QMessageBox.Yes:
			sys.exit()
		else:
			pass

	def help(self):
		'''
		In the menu bar, there is a help option.  A separate window widget will pop up with some help features of the 
		program.  A shortcut of Ctrl+h has also been set for this execution.
		'''
		self.helpwindow = QDialog()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self.helpwindow)
		self.helpwindow.show()

	def browse_folder(self):
		'''
		In the menu bar, there is an option to select the directory where the trials to be processed are located.  
		A shortcut of Ctrl+d has also been set for this execution.
		'''
		self.listDirectory.clear()
		direct = QFileDialog.getExistingDirectory(self, 
			"Pick a folder")

		if direct:
			for file_name in os.listdir(direct): 
				self.listDirectory.addItem(file_name)

		os.chdir(str(direct))
		self.dataFilesLocation = str(direct)

	def trial_select_list(self):
		'''
		In the menu bar, there is an option to select the specific trial to process.  There are two other methods to 
		execute this command.  First there is Ctrl+t.  Second, merely clicking on the trial that populates in the 
		Drectory List in the program will select the trial.  A pop-up window confirming the trial selection will finish
		the exection.  
		'''
		self.fileNameTrial = self.listDirectory.currentItem().text()
		trialSelect = QMessageBox.question(self, 'Trial select',
			"You have chosen: " + str(self.fileNameTrial) + " to process.  "\
			"Is this correct?",
			QMessageBox.Yes | QMessageBox.No)
		self.progressTrial.setValue(0) 

		if trialSelect == QMessageBox.Yes:
			self.lineTrialName.setText(QString(self.fileNameTrial))
		else:
			self.fileNameTrial = None
			pass

	def trial_open(self):
		'''
		See explanation in above function.
		'''
		trialSel = QFileDialog.getOpenFileName(self, "Choose Trial")

		if trialSel:
			trial = QMessageBox.question(self, 'Trial select',
			"You have chosen: " + str(trialSel) + " to process.  "\
			"Is this correct?",
			QMessageBox.Yes | QMessageBox.No)
			if trial == QMessageBox.Yes:
				self.fileNameTrial = trialSel
				self.lineTrialName.setText(QString(self.fileNameTrial))
			else:
				self.fileNameTrial = None
				pass

	def participant(self):
		'''
		When a new participant is added, the program will prompt whether this is a new participant or not.  The answer
		will be stored in 'self', for future use. 
		'''
		self.participant = str(self.lineParticipant.text())
		part = QMessageBox.question(self, 'Participant',
			                        "Is this the correct participant code? <br> <br> "
			                        "<i>Ensure data is saved before changing participants.<br>"
			                        "<b>Analyzed data will be cleared</i></b>",
			QMessageBox.Yes | QMessageBox.No) # I changed this.  Since the results save with a time/day stamp I think it doesn't matter if the participant folder already exists.
		if part == QMessageBox.Yes:
			self.table = pd.DataFrame({'Filename':[], 'Mean Speed (COPx)':[], 'Mean Speed (COPy)':[], 'Distance COPx':[], 
				'Distance COPy':[], 'Mean Position COPx':[], 'Mean Position COPy':[], 'SD Position COPx':[], 
				'SD Position COPy':[], 'Min Position COPx':[], 'Min Position COPy':[], 'Max Position COPx':[], 
				'Max Position COPy':[], 'RMS Position COPx':[], 'RMS Position COPy':[], 'x5':[], 'x10':[], 'x25':[], 
				'x50':[], 'x75':[], 'x90':[], 'x95':[], 'y5':[], 'y10':[], 'y25':[], 'y50':[], 'y75':[], 'y90':[], 'y95':[], 
				'Effective Sampling Rate (MSE)':[], 'Low Frequency Cutoff (MSE)':[], 'High Frequency Cutoff (MSE)':[], 'r - fraction of SD (MSE)':[], 
				'Max scale factor (MSE)':[], 'm - sequence length (MSE)':[]}, 
				columns=['Filename', 'Mean Speed (COPx)', 'Mean Speed (COPy)', 'Distance COPx', 
				'Distance COPy', 'Mean Position COPx', 'Mean Position COPy', 'SD Position COPx', 
				'SD Position COPy', 'Min Position COPx', 'Min Position COPy', 'Max Position COPx', 
				'Max Position COPy', 'RMS Position COPx', 'RMS Position COPy', 'x5', 'x10', 'x25', 
				'x50', 'x75', 'x90', 'x95', 'y5', 'y10', 'y25', 'y50', 'y75', 'y90', 'y95', 
				'Effective Sampling Rate (MSE)', 'Low Frequency Cutoff (MSE)', 'High Frequency Cutoff (MSE)', 
				'r - fraction of SD (MSE)', 'Max scale factor (MSE)', 'm - sequence length (MSE)'])
			self.position_table = pd.DataFrame()
			self.velocity_table = pd.DataFrame()
			self.mse_table = pd.DataFrame()
			self.trial = 1
			#removed the below as it cleared the directory - but this is unwanted is someone just did things in a different order. 
			# self.listDirectory.clear() # Clear the directory list.  This triggers for the user that they need to choose a new directory with new participant trials. 
		else:
			pass 

	def force_plate(self): 
		'''
		The choosebox allows to choose which force plate to use.  The origin of the force plate and the accompanying 
		sensitivity matrix will be chosen.  As well, to help the user, the force plate in the figure that is chosen
		with the groupbox will turn red. Try/except cases are presented that inform the user if something goes wrong. 
		'''
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
		'''
		Main processing function.  See comments throughout. 
		'''
		######## ARBITRARY PROGRESS UPDATE ##########
		self.progressTrial.setValue(0)

		warnings.filterwarnings("ignore")
		numpy.set_printoptions(precision=4, suppress=True)
		self.figure.clf() #clear any previous data in the results
		self.lineSpeedx.setText(QString())
		self.lineSpeedy.setText(QString())
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
		self.lineMinPosx.setText(QString())
		self.lineMaxPosx.setText(QString())
		self.lineMinPosy.setText(QString())
		self.lineMaxPosy.setText(QString())
		self.lineRMSx.setText(QString())
		self.lineRMSy.setText(QString())
		self.lineMeanPosx.setText(QString())
		self.lineMeanPosy.setText(QString())
		self.lineSDPosx.setText(QString())
		self.lineSDPosy.setText(QString())

		if self.fileNameTrial == None:
			QMessageBox.warning(self, 'Warning', 
				                "No trial chosen!  Please select a trial to continue processing.",
				                QMessageBox.Ok)
			return
		else:
			pass

		if self.participant == None:
			QMessageBox.warning(self, 'Warning',
				                "No participant entered.<br> Please enter a participant code.<br>"
				                "<i> Ensure that you press Enter after typing the participant name</i>",
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

		try: analog_data = pd.read_csv(str(self.fileNameTrial), sep=',', skiprows=3, usecols=range(1,13))
		except:
			errorBox = QMessageBox.critical(self, 'File Error', 'You are procssing a file named: ' +
				str(self.fileNameTrial) + '. This file is in the wrong format.  Choose a file with the ending: _Odau_1.csv')
			return None

		if plateNum == 1: 
			forcePlateAnalog = numpy.asarray(analog_data.loc[:,['Analog_1', 'Analog_2', 'Analog_3', 'Analog_4', 
				'Analog_5', 'Analog_6',]])
		elif plateNum == 2:
			forcePlateAnalog = numpy.asarray(analog_data.loc[:,['Analog_7', 'Analog_8', 'Analog_9', 'Analog_10', 
				'Analog_11', 'Analog_12',]])

		######## ARBITRARY PROGRESS UPDATE ##########
		self.progressTrial.setValue(10)

		samplingRate = int(self.lineSampling.text())
		samplingDuration = int(self.lineDuration.text()) 
		gain = int(self.lineGain.text())
		vMax = int(self.lineVMax.text())
		multiplier = float(self.lineMult.text())
		Zo_m = float(self.lineZ.text())/1000
		timeVel = numpy.linspace(0, samplingDuration, ((samplingRate * samplingDuration)-1)) 
		forces_moments = numpy.matmul(sensitivityMatrix, forcePlateAnalog.T).T
		forces_moments = forces_moments/(gain*vMax*multiplier)

		######## ARBITRARY PROGRESS UPDATE ##########
		self.progressTrial.setValue(20)

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
		CofPx_filt = CofPfunctions.filterData(CofPx, freqCutoff=20, samplingRate=1000, order=2)
		CofPy_filt = CofPfunctions.filterData(CofPy, freqCutoff=20, samplingRate=1000, order=2)
		centeredCofPx = CofPx_filt - (CofPx_filt.mean())
		centeredCofPy = CofPy_filt - (CofPy_filt.mean())
		velocity_x = numpy.diff(centeredCofPx) / (1./samplingRate)
		velocity_y = numpy.diff(centeredCofPy) / (1./samplingRate)
		velocity_resultant = numpy.sqrt(velocity_x**2 + velocity_y**2)

		######## ARBITRARY PROGRESS UPDATE ##########
		self.progressTrial.setValue(30)
		
		framesPos = numpy.linspace(1, (samplingRate * samplingDuration), (samplingRate * samplingDuration)) 
		framesVel = numpy.linspace(1, (samplingRate * samplingDuration)-1, (samplingRate * samplingDuration)-1) 
		self.centredCofPx = numpy.vstack((framesPos, centeredCofPx))
		self.centredCofPy = numpy.vstack((framesPos, centeredCofPy))
		self.centredCofP = numpy.vstack((framesPos, centeredCofPx, centeredCofPy))
		self.velocityx = numpy.vstack((framesVel, velocity_x))
		self.velocityy = numpy.vstack((framesVel, velocity_y))
		self.velocity = numpy.vstack((framesVel, velocity_x, velocity_y))

		distance_x_005 = CofPfunctions.getDistance_Coverage(CofPx_filt, 0.05) #just making sure filtered data gets input here as filterData was not called in this function
		distance_x_010 = CofPfunctions.getDistance_Coverage(CofPx_filt, 0.1)
		distance_x_025 = CofPfunctions.getDistance_Coverage(CofPx_filt, 0.25)
		distance_x_050 = CofPfunctions.getDistance_Coverage(CofPx_filt, 0.5)
		distance_x_075 = CofPfunctions.getDistance_Coverage(CofPx_filt, 0.75)
		distance_x_090 = CofPfunctions.getDistance_Coverage(CofPx_filt, 0.9)
		distance_x_095 = CofPfunctions.getDistance_Coverage(CofPx_filt, 0.95)

		distance_y_005 = CofPfunctions.getDistance_Coverage(CofPy_filt, 0.05)
		distance_y_010 = CofPfunctions.getDistance_Coverage(CofPy_filt, 0.1)
		distance_y_025 = CofPfunctions.getDistance_Coverage(CofPy_filt, 0.25)
		distance_y_050 = CofPfunctions.getDistance_Coverage(CofPy_filt, 0.5)
		distance_y_075 = CofPfunctions.getDistance_Coverage(CofPy_filt, 0.75)
		distance_y_090 = CofPfunctions.getDistance_Coverage(CofPy_filt, 0.9)
		distance_y_095 = CofPfunctions.getDistance_Coverage(CofPy_filt, 0.95)

		distance_x = CofPfunctions.getDistanceCofP(CofPx, filter=True, freqCutoff=20, samplingRate=1000, order=2)
		distance_y = CofPfunctions.getDistanceCofP(CofPy, filter=True, freqCutoff=20, samplingRate=1000, order=2)
		distance_xy = CofPfunctions.getDistanceBothAxes(CofPx, CofPy, filter=True, freqCutoff=20, samplingRate=1000, order=2)

		speed_x = distance_x/((1./samplingRate) * len(CofPx)) 
		speed_y = distance_y/((1./samplingRate) * len(CofPy)) 
		speed_xy = distance_xy/((1./samplingRate) * len(CofPx)) 

		min_x, max_x, mean_x, sd_x = CofPfunctions.getCenteredSummaryStatistics(CofPx_filt)
		min_y, max_y, mean_y, sd_y = CofPfunctions.getCenteredSummaryStatistics(CofPy_filt)
		rms_x = CofPfunctions.getRMS(CofPx_filt)
		rms_y = CofPfunctions.getRMS(CofPy_filt)

		######## ARBITRARY PROGRESS UPDATE ##########
		self.progressTrial.setValue(40)

		mse_x, mse_x_auc, effectiveSamplingRate, lowFreqCutoff = CofPfunctions.filterGetMSE_coarse(CofPx-CofPx.mean(), r_fraction=0.15, max_scale_factor=20, 
                        m=2, pointsLastMSE =300, upperFreqCutoff=20, 
                        samplingRate=float(self.lineSampling.text()))
		mse_y, mse_y_auc, effectiveSamplingRate, lowFreqCutoff = CofPfunctions.filterGetMSE_coarse(CofPy-CofPy.mean(), r_fraction=0.15, max_scale_factor=40, 
                        m=2, pointsLastMSE =300, upperFreqCutoff=20, 
                        samplingRate=float(self.lineSampling.text()))

		######## ARBITRARY PROGRESS UPDATE ##########
		self.progressTrial.setValue(50)

		# mse_x = numpy.random.randint(1000,size=40)
		# mse_y = numpy.random.randint(1000,size=40)

		# mse_x_area = numpy.trapz(mse_x)
		# mse_y_area = numpy.trapz(mse_y)

		######## ARBITRARY PROGRESS UPDATE ##########
		self.progressTrial.setValue(80)

		# Populate these with the new variables
		self.lineSpeedx.setText(QString(str.format('{0:.4f}', speed_x)))
		self.lineSpeedy.setText(QString(str.format('{0:.4f}', speed_y)))
		self.lineDistancex.setText(QString(str.format('{0:.4f}', distance_x)))
		self.lineDistancey.setText(QString(str.format('{0:.4f}', distance_y)))
		self.lineMSEx.setText(QString(str.format('{0:.4f}', mse_x_auc)))
		self.lineMSEy.setText(QString(str.format('{0:.4f}', mse_y_auc)))

		#min/max values
		self.lineMinPosx.setText(QString(str.format('{0:.4f}', min_x)))
		self.lineMaxPosx.setText(QString(str.format('{0:.4f}', max_x)))
		self.lineMinPosy.setText(QString(str.format('{0:.4f}', min_y)))
		self.lineMaxPosy.setText(QString(str.format('{0:.4f}', max_y)))

		#RMSvalue
		self.lineRMSx.setText(QString(str.format('{0:.4f}', rms_x)))
		self.lineRMSy.setText(QString(str.format('{0:.4f}', rms_y)))

		#mean positions (absolute)
		self.lineMeanPosx.setText(QString(str.format('{0:.4f}', mean_x)))
		self.lineMeanPosy.setText(QString(str.format('{0:.4f}', mean_y)))

		#sd positions (absolute)
		self.lineSDPosx.setText(QString(str.format('{0:.4f}', sd_x)))
		self.lineSDPosy.setText(QString(str.format('{0:.4f}', sd_y)))

		#percentile distances from the center. 
		self.line005x.setText(QString(str.format('{0:.4f}', distance_x_005)))
		self.line005y.setText(QString(str.format('{0:.4f}', distance_y_005)))
		self.line01x.setText(QString(str.format('{0:.4f}', distance_x_010)))
		self.line01y.setText(QString(str.format('{0:.4f}', distance_y_010)))
		self.line025x.setText(QString(str.format('{0:.4f}', distance_x_025)))
		self.line025y.setText(QString(str.format('{0:.4f}', distance_y_025)))
		self.line05x.setText(QString(str.format('{0:.4f}', distance_x_050)))
		self.line05y.setText(QString(str.format('{0:.4f}', distance_y_050)))
		self.line075x.setText(QString(str.format('{0:.4f}', distance_x_075)))
		self.line075y.setText(QString(str.format('{0:.4f}', distance_y_075)))
		self.line09x.setText(QString(str.format('{0:.4f}', distance_x_090)))
		self.line09y.setText(QString(str.format('{0:.4f}', distance_y_090)))
		self.line095x.setText(QString(str.format('{0:.4f}', distance_x_095)))
		self.line095y.setText(QString(str.format('{0:.4f}', distance_y_095)))

		######## ARBITRARY PROGRESS UPDATE ##########
		self.progressTrial.setValue(90)
		scales = numpy.arange(1, 41, 1)

		ax1 = self.figure.add_subplot(131) #these subplots will change (centred COP, Vel., MSE)
		ax1.plot(centeredCofPx, centeredCofPy, 'k')
		ax1.set_title('Centred CoPy vs CoPx (m)')
		ax2 = self.figure.add_subplot(132)
		ax2.plot(timeVel, velocity_x, label="Vel x")
		ax2.plot(timeVel, velocity_y, label="Vel y")
		ax2.set_title('Vel (m/s) vs Time (s)')
		ax2.legend()
		ax3 = self.figure.add_subplot(133) 
		ax3.plot(scales, mse_x, label="MSEx")
		ax3.plot(scales, mse_y, label="MSEy")
		ax3.set_title('MSE')
		ax3.legend()
		self.canvas.draw()

		self.table = self.table.append({'Filename':str(self.fileNameTrial), 'Mean Speed (COPx)':speed_x, 
			'Mean Speed (COPy)':speed_y, 'Distance COPx':distance_x, 'Distance COPy':distance_y, 'Mean Position COPx':mean_x,
			'Mean Position COPy':mean_y, 'SD Position COPx':sd_x, 'SD Position COPy':sd_y, 'Min Position COPx':min_x,
			'Min Position COPy':min_y, 'Max Position COPx':max_x, 'Max Position COPy':max_y, 'RMS Position COPx':rms_x,
			'RMS Position COPy':rms_y, 'x5':distance_x_005, 'x10':distance_x_010, 'x25':distance_x_025, 'x50':distance_x_050, 
			'x75':distance_x_075, 'x90':distance_x_090, 'x95':distance_x_095, 'y5':distance_y_005, 'y10':distance_y_010, 
			'y25':distance_y_025, 'y50':distance_y_050, 'y75':distance_y_075, 'y90':distance_y_090, 'y95':distance_y_095,
			'Effective Sampling Rate (MSE)':effectiveSamplingRate, 'Low Frequency Cutoff (MSE)':lowFreqCutoff,
			'High Frequency Cutoff (MSE)':20, 'r - fraction of SD (MSE)':0.15, 'Max scale factor (MSE)':20,
			'm - sequence length (MSE)':2}, 
			ignore_index=True)

		# I added the trial name as well to each iteration, just in case they process trials out of order
		velocity_df = pd.DataFrame({'Frames': framesVel.T, 'Velocity_x':velocity_x.T, 'Velocity_y':velocity_y.T})
		columns_velocity = [('Trial ' + str(self.trial), str(self.fileNameTrial), 'Frames'), 
			('Trial ' + str(self.trial), str(self.fileNameTrial), 'Velocity_x'), 
			('Trial ' + str(self.trial), str(self.fileNameTrial), 'Velocity_y')]
		velocity_df.columns = pd.MultiIndex.from_tuples(columns_velocity)
		self.velocity_table = pd.concat([self.velocity_table, velocity_df], axis=1)

		position_df = pd.DataFrame({'Frames': framesPos.T, 'Position_x':centeredCofPx.T, 'Position_y':centeredCofPy.T})
		columns_position = [('Trial ' + str(self.trial), str(self.fileNameTrial), 'Frames'), 
			('Trial ' + str(self.trial), str(self.fileNameTrial), 'Position_x'), 
			('Trial ' + str(self.trial), str(self.fileNameTrial), 'Position_y')]
		position_df.columns = pd.MultiIndex.from_tuples(columns_position)
		self.position_table = pd.concat([self.position_table, position_df], axis=1)

		mse_df = pd.DataFrame({'Frames': numpy.arange(1,len(mse_x)+1,1), 'MSE_x':mse_x, 'MSE_y':mse_y})
		columns_mse = [('Trial ' + str(self.trial), str(self.fileNameTrial), 'Frames'), 
			('Trial ' + str(self.trial), str(self.fileNameTrial), 'MSE_x'), 
			('Trial ' + str(self.trial), str(self.fileNameTrial), 'MSE_y')]
		mse_df.columns = pd.MultiIndex.from_tuples(columns_mse)
		self.mse_table = pd.concat([self.mse_table, mse_df], axis=1)

		self.trial += 1

		######## ARBITRARY PROGRESS UPDATE ##########
		self.progressTrial.setValue(100)

	def save_results(self):
		resultsFolderName = 'Results_' + self.participant + '-' + time.strftime("%d-%B-%Y_%I%M%p")
		saveLocation = str(os.path.join(str(self.dataFilesLocation), resultsFolderName))
		os.mkdir(saveLocation)

		if self.checkBoxCOPPos.isChecked():
			filepath = os.path.join(saveLocation, 'COP_Position_' + self.participant + '.xlsx')
			self.position_table.to_excel(filepath)
		elif not self.checkBoxCOPPos.isChecked():
			pass

		if self.checkBoxCOPVel.isChecked():
			filepath = os.path.join(saveLocation, 'COP_Velocity_' + self.participant + '.xlsx')
			self.velocity_table.to_excel(filepath)
		elif not self.checkBoxCOPVel.isChecked():
			pass

		if self.checkBoxMSE.isChecked():
			filepath = os.path.join(saveLocation, 'MSE_' + self.participant + '.xlsx')
			self.mse_table.to_excel(filepath)
		elif not self.checkBoxMSE.isChecked():
			pass

		if self.checkBoxTable.isChecked():
			filepath = os.path.join(saveLocation, 'Table_Results_' + self.participant + '.xlsx')
			self.table.to_excel(filepath, index=False)
		elif not self.checkBoxTable.isChecked():
			pass

		saved = QMessageBox.information(self, 'Saved Results',
			"Results have been saved!")	#add a popup window to inform user the results are saved	

	def closeEvent(self, event):
    	
		choiceQuit = QMessageBox.question(self, 'Quit',
			"Are you sure you want to quit the application?  Make sure you have saved your data!",
			QMessageBox.Yes | QMessageBox.No)
		if choiceQuit == QMessageBox.Yes:
			self.destroy()
		else:
			event.ignore()
   		


def main():
	app = QApplication(sys.argv)
	form = ExampleApp()
	form.show()
	app.exec_()


if __name__ == '__main__':
	main()