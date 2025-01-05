import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtCore import QObject, pyqtSlot
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QUrl
import pytesseract
from PIL import Image

class Backend(QObject):
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    @pyqtSlot(result=str)
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(None, "Select Folder")
        return folder if folder else ""
    
    @pyqtSlot(str)
    def get_file_name(self, file_path):
        files = os.listdir(file_path)
        count = 0
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', 'jp2','.tiff']  # Add any image extensions you want to support
        
        for file in files:
            # Check if the file has an image extension
            if any(file.lower().endswith(ext) for ext in image_extensions):
                count += 1
                # Full path to the image
                image_path = os.path.join(file_path, file)
                
                # Generate the corresponding text file name
                text_file_name = os.path.join(file_path, '{0}.txt'.format(file))
                
                # Open the text file and write the OCR result
                with open(text_file_name, "w") as f:
                    text = pytesseract.image_to_string(Image.open(image_path), lang='nep')
                    f.write(text)
                
                # Print progress
                print("{:.2f}% Completed".format((count / len(files)) * 100))
    
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