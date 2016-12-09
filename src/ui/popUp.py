from PyQt4 import QtGui


class PopUp:
    @staticmethod
    def question_yes_no(title, message):
        ans = QtGui.QMessageBox.question(None,
                                         title,
                                         message,
                                         QtGui.QMessageBox.Yes,
                                         QtGui.QMessageBox.No)
        if ans == QtGui.QMessageBox.Yes:
            return True
        else:
            return False
