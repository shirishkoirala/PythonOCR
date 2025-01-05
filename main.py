import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtCore import QObject, pyqtSlot
from PyQt6.QtWidgets import QFileDialog

class Backend(QObject):
    @pyqtSlot(result=str)
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(None, "Select Folder")
        return folder if folder else ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Create and register the backend object
    backend = Backend()
    engine.rootContext().setContextProperty("backend", backend)

    # Load the QML file
    engine.load("main.qml")

    # Exit if no root objects are loaded
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())