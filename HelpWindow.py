# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Help.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(494, 300)
        self.textEdit = QtGui.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(5, 5, 482, 290))
        self.textEdit.setReadOnly(True)
        text = ("This program was created by Elora Brenneman and Anthony Gatti for Dr. Marla Beauchamp.  It is not to be distributed elsewhere without "\
            "the consent of the original creators.  They can be contacted at:\n"\
            "       Elora Brenneman: brennema@mcmaster.ca\n"\
            "       Anthony Gatti: gattia@mcmaster.ca\n"
            "--------------------------------------------------\n"
            "This program takes raw voltage data collected from AMTI OR6-7 force plates and returns variables of interest related to centre of pressure.  "\
            "Specifcally, centre of pressure position (m), velocity (m/s), and mutli-scale entropy are calculated and available for export.  To run the "\
            "program, a working directory (directory containing trials to be processed) must be pulled into the program using one of two methods: through the File "\
            "menu, or using the shortcut Ctrl+D.  Once the directory is listed in the 'Set-up Processing Parameters' tab, the desired trial can be chosen using "\
            "one of three methods: directly clicking on the trial in the directory list, through the File menu, or by using the shortcut Ctrl+O.  A pop-up message "\
            "will ask the user to confirm the chosen trial.  Once confirmed, the trial name will appear in the text box near the 'Process Trial' button.  Next, "\
            "a force plate must be chosen.  The force plate origin (x, y, z) will populate and a figure indicating the chosen force plate will appear.  The "\
            "'Process Trial' button will process the data.  All results will appear in the 'Results' tab.  Finally, "\
            "any desired outputs can be saved by indicating checkmarks in the boxes next to the variables of interest.  Pressing the 'Save' button will save "
            "these results in the same directory as the original trials.  For more information, contact Elora or Anthony.")
        self.textEdit.setText(text)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "About", None))
        Dialog.setWindowIcon(QtGui.QIcon('python-icon_1_orig.png'))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

