from PyQt4 import QtGui


class PopUp:
    @staticmethod
    def question_yes_no(parent, title, message):
        ans = QtGui.QMessageBox.question(parent,
                                         title,
                                         message,
                                         QtGui.QMessageBox.Yes,
                                         QtGui.QMessageBox.No)
        if ans == QtGui.QMessageBox.Yes:
            return True
        else:
            return False

    @staticmethod
    def warning(parent, title, message):
        QtGui.QMessageBox.warning(parent, title, message, QtGui.QMessageBox.Ok)