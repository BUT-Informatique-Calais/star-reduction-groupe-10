import sys
from PyQt6.QtWidgets import QApplication
from ImageModel import ImageModel
from ImageView import ImageView
from ImageController import ImageController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = ImageModel()
    view = ImageView()
    controller = ImageController(model, view)
    view.show()
    sys.exit(app.exec())
