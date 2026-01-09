import sys
from PyQt6.QtWidgets import QApplication, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QSlider
from PyQt6.QtCore import Qt

class Interface(QWidget):
    def __init__(self):
        super().__init__()
        
        # Layout Button
        self.layout_button = QHBoxLayout()
        self.layout_button.addWidget(QPushButton("Import"))
        self.layout_button.addWidget(QPushButton("Export"))
        
        # Layout Left
        self.layout_left = QVBoxLayout()

        # Slider Érosion
        self.slider_erosion = QSlider(Qt.Orientation.Horizontal)
        self.slider_erosion.setMinimum(0)
        self.slider_erosion.setMaximum(10)
        self.slider_erosion.setTickPosition(QSlider.TickPosition.TicksBelow)
        
        # Slider Itération
        self.slider_iteration = QSlider(Qt.Orientation.Horizontal)
        self.slider_iteration.setMinimum(0)
        self.slider_iteration.setMaximum(10)
        self.slider_iteration.setTickPosition(QSlider.TickPosition.TicksBelow)
        
        
        self.layout_left.addLayout(self.layout_button)
        self.layout_left.addWidget(QLabel("Erosion"))
        self.layout_left.addWidget(self.slider_erosion)
        self.layout_left.addWidget(QLabel("Itération"))
        self.layout_left.addWidget(self.slider_iteration)
        
        
        # Layout Right
        self.layout_right = QVBoxLayout()
        self.layout_right.addWidget(QLabel("Image d'Origine"))
        self.layout_right.addWidget(QLabel("Image après traitement"))
                
        # Layout principal
        self.layout = QHBoxLayout()
        self.layout.addLayout(self.layout_left)
        self.layout.addLayout(self.layout_right)
        self.setLayout(self.layout)
        self.setWindowTitle("Star Réduction") 
        
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = Interface()
    sys.exit(app.exec())
