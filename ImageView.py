from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QSlider, QGridLayout, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage

class ImageView(QWidget):
    def __init__(self):
        super().__init__()
        
        # Main window configuration
        self.setWindowTitle("Star Reduction MVC")
        self.setGeometry(100, 100, 1200, 800)

        # Buttons
        self.load_button = QPushButton("Importer une image")
        self.save_button = QPushButton("Exporter l'image")

        # Star radius slider
        self.erode_slider = QSlider(Qt.Orientation.Horizontal)
        self.erode_slider.setMinimum(3)
        self.erode_slider.setMaximum(20)
        self.erode_slider.setValue(10)
        self.erode_slider.setTickInterval(1)
        self.erode_slider.setTickPosition(QSlider.TickPosition.TicksBelow)

        # Median filter size slider
        self.iter_slider = QSlider(Qt.Orientation.Horizontal)
        self.iter_slider.setMinimum(3)
        self.iter_slider.setMaximum(15)
        self.iter_slider.setValue(5)
        self.iter_slider.setSingleStep(2)
        self.iter_slider.setTickInterval(2)
        self.iter_slider.setTickPosition(QSlider.TickPosition.TicksBelow)

        # Image display labels
        self.label_orig = QLabel("Image originale")
        self.label_result = QLabel("Résultat")
        self.label_orig.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_result.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Label size and automatic scaling
        self.label_orig.setMinimumSize(500, 500)
        self.label_result.setMinimumSize(500, 500)
        self.label_orig.setScaledContents(True)
        self.label_result.setScaledContents(True)

        # Layout
        layout = QGridLayout()
        layout.addWidget(self.load_button, 0, 0)
        layout.addWidget(self.save_button, 0, 1)
        layout.addWidget(self.label_orig, 1, 0)
        layout.addWidget(self.label_result, 1, 1)
        layout.addWidget(QLabel("Rayon des étoiles"), 2, 0)
        layout.addWidget(self.erode_slider, 3, 0)
        layout.addWidget(QLabel("Filtre médian"), 2, 1)
        layout.addWidget(self.iter_slider, 3, 1)

        self.setLayout(layout)

    def update_image(self, label: QLabel, image):
        """Convert numpy image to QPixmap and update label"""
        
        # Grayscale image
        if image.ndim == 2:
            h, w = image.shape
            bytes_per_line = w
            qimage = QImage(image.data, w, h, bytes_per_line, QImage.Format.Format_Grayscale8)
            
        # Color image (BGR -> RGB)
        else:
            h, w, ch = image.shape
            bytes_per_line = ch * w
            import cv2 as cv
            image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            qimage = QImage(image_rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        label.setPixmap(pixmap)
