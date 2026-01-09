from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QSlider, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage, QIcon

class ImageView(QWidget):
    def __init__(self):
        super().__init__()
        
        # Main window configuration
        self.setWindowTitle("Star Reduction")
        self.setGeometry(100, 100, 1200, 800)

        # Buttons
        self.load_button = QPushButton("Importer une image")
        self.save_button = QPushButton("Exporter l'image")
        self.theme_button = QPushButton()
        self.theme_button.setIcon(QIcon("img/sun.png"))

        # Star radius slider
        self.star_radius = QSlider(Qt.Orientation.Horizontal)
        self.star_radius.setMinimum(3)
        self.star_radius.setMaximum(20)
        self.star_radius.setValue(10)
        self.star_radius.setTickInterval(1)
        self.star_radius.setTickPosition(QSlider.TickPosition.TicksBelow)

        # Median filter size slider
        self.median_filter = QSlider(Qt.Orientation.Horizontal)
        self.median_filter.setMinimum(3)
        self.median_filter.setMaximum(15)
        self.median_filter.setValue(5)
        self.median_filter.setSingleStep(2)
        self.median_filter.setTickInterval(2)
        self.median_filter.setTickPosition(QSlider.TickPosition.TicksBelow)

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
        layout.addWidget(self.theme_button, 0, 2)
        layout.addWidget(self.label_orig, 1, 0)
        layout.addWidget(self.label_result, 1, 1)
                
        label_star_radius = QLabel("Rayon des étoiles")
        label_star_radius.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label_star_radius, 2, 0)
        layout.addWidget(self.star_radius, 3, 0)

        label_median = QLabel("Filtre médian")
        label_median.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label_median, 2, 1)
        layout.addWidget(self.median_filter, 3, 1)


        self.setLayout(layout)
        
        # Mode
        self.dark_mode = True
        self.theme_button.clicked.connect(self.toggle_theme)
        self.set_dark_theme()

    def toggle_theme(self):
        if self.dark_mode:
            self.set_light_theme()
            self.dark_mode = False
            self.theme_button.setIcon(QIcon("img/moon.png"))
        else:
            self.set_dark_theme()
            self.dark_mode = True
            self.theme_button.setIcon(QIcon("img/sun.png"))
            

    def load_stylesheet(self, file_path):
        """Load QSS file"""
        with open(file_path, "r") as f:
            return f.read()

    def set_dark_theme(self):
        """Set dark theme"""
        qss = self.load_stylesheet("style/dark_theme.qss")
        self.setStyleSheet(qss)

    def set_light_theme(self):
        """Set light theme"""
        qss = self.load_stylesheet("style/light_theme.qss")
        self.setStyleSheet(qss)

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
