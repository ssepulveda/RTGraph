from PyQt5 import QtGui


class PopUp:
    @staticmethod
    def question_yes_no(parent, title, message):
        """
        Shows a Pop up question dialog with yes and no buttons.
        :param parent: Parent window for the dialog.
        :param title: Title of the dialog.
        :type title: str.
        :param message: Message to be shown in the content of the dialog.
        :type message: str.
        :return: True if the Yes button was pressed in the dialog.
        :rtype: bool.
        """
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
        """
        Shows a Pop up warning dialog with a Ok buttons.
        :param parent: Parent window for the dialog.
        :param title: Title of the dialog.
        :type title: str.
        :param message: Message to be shown in the content of the dialog.
        :type message: str.
        :return:
        """
        QtGui.QMessageBox.warning(parent, title, message, QtGui.QMessageBox.Ok)