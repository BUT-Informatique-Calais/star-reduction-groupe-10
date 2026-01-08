import sys
from PyQt6.QtWidgets import QApplication
from prototype.ImageModel import ImageModel
from prototype.ImageView import ImageView
from prototype.ImageController import ImageController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = ImageModel()
    view = ImageView()
    controller = ImageController(model, view)
    view.show()
    sys.exit(app.exec())
