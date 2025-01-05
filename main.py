import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtCore import QObject, pyqtSlot
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QUrl

class Backend(QObject):
    @pyqtSlot(result=str)
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(None, "Select Folder")
        return folder if folder else ""
    
# Determine if we are running from a PyInstaller bundle
if getattr(sys, 'frozen', False):
    # If frozen, the QML files will be located in the same directory as the executable
    resource_path = sys._MEIPASS
else:
    # During development, use the regular path
    resource_path = os.path.dirname(os.path.abspath(__file__))

app = QApplication(sys.argv)
engine = QQmlApplicationEngine()

# Create and register the backend object
backend = Backend()
engine.rootContext().setContextProperty("backend", backend)

# Define the resource path
resource_path = os.path.join(resource_path, 'UI')

qml_file = QUrl.fromLocalFile(os.path.join(resource_path, 'main.qml'))
engine.load(qml_file)

# Exit if no root objects are loaded
if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec())