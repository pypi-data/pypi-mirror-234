from PySide2 import QtWidgets, QtCore
print ("Using PySide2")
"""
try:
    from PySide2 import QtWidgets, QtCore
    print ("Using PySide2")
except:
    try:
        print("Unable to use PySide2")
        from PyQt5 import QtWidgets, QtCore
        print("Using PyQt5")
    except:
        print("Unable to use PyQt5")
"""
"""
try:
    from PyQt5 import sip
except ImportError:
    import sip
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTabWidget
"""
"""
from cioblender.validation_tab import ValidationTab

from cioblender.progress_tab import ProgressTab
from cioblender.response_tab import ResponseTab
"""
#from cioblender import validation
import time
"""
"""
class SubmissionDialog(QtWidgets.QMainWindow):

    def __init__(self, payload, parent=None):
        super(SubmissionDialog, self).__init__(parent)
        self.setWindowTitle("Conductor Submission")
        #self.setStyleSheet(hou.qt.styleSheet())

        #self.payload = payload

        #self.layout = QtWidgets.QVBoxLayout()
        #self.tab_widget = QtWidgets.QTabWidget()
        #self.setLayout(self.layout)
        #self.layout.addWidget(self.tab_widget)
        #self.setMinimumSize(1200, 742)  # Set minimum window size

        """
        self.validation_tab = ValidationTab(payload, self)
        self.tab_widget.addTab(self.validation_tab, "Validation")

        self.progress_tab = ProgressTab(payload, self)
        self.tab_widget.addTab(self.progress_tab, "Progress")

        self.response_tab = ResponseTab(payload, self)
        self.tab_widget.addTab(self.response_tab, "Response")
        
        #self.setGeometry(200, 200, 1100, 756)
        # self.setMinimumSize(900, 556)  # Set minimum window size
        

        self.tab_widget.setTabEnabled(1, False)
        self.tab_widget.setTabEnabled(2, False)


 
        #self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        self.run()
"""


    def show_validation_tab(self):
        pass


    def show_progress_tab(self):
        self.tab_widget.setTabEnabled(1, True)
        self.tab_widget.setCurrentWidget(self.progress_tab)
        # self.tab_widget.setTabEnabled(0, False)
        # self.tab_widget.setTabEnabled(2, False)
        QtCore.QCoreApplication.processEvents()
        time.sleep(1)

    def show_response_tab(self):
        self.tab_widget.setTabEnabled(2, True)
        self.tab_widget.setCurrentWidget(self.response_tab)
        self.tab_widget.setTabEnabled(0, False)
        # self.tab_widget.setTabEnabled(1, False)
        QtCore.QCoreApplication.processEvents()
        time.sleep(1)

    def run(self):
        #errors, warnings, notices = validation.run(self.payload)
        #self.validation_tab.populate(errors, warnings, notices)
        pass

    def on_close(self):
        self.accept()


