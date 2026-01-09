from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QSlider, QVBoxLayout, QHBoxLayout, QMenu, QToolButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage, QIcon

class ImageView(QWidget):
    def __init__(self):
        super().__init__()
        
        # Main window configuration
        self.setWindowTitle("Star Reduction")
        self.setWindowIcon(QIcon("img/star_reduction.png"))
        self.setGeometry(100, 100, 1200, 800)
        self.setContentsMargins(15, 15, 15, 15)

        # Load and Save buttons (logic remains, will be put in menu)
        self.load_button = QPushButton("Importer une image")
        self.save_button = QPushButton("Exporter l'image")

        # Fichier menu button
        self.file_menu_button = QToolButton()
        self.file_menu_button.setText("Fichier")
        self.file_menu_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.file_menu = QMenu()
        self.file_menu.addAction(self.load_button.text(), self.load_button.click)
        self.file_menu.addAction(self.save_button.text(), self.save_button.click)
        self.file_menu_button.setMenu(self.file_menu)
        self.file_menu_button.setStyleSheet("padding:10px; margin:5px;")
        
        # API button
        self.api_button = QPushButton()
        self.api_button.setText("Utiliser l'API Astrometry.net")
        self.api_button.setStyleSheet("margin:5px; padding:4px;")

        # Theme button (light/dark)
        self.theme_button = QPushButton()
        self.theme_button.setIcon(QIcon("img/sun.png"))
        self.theme_button.setFixedSize(60, 60)
        self.theme_button.setStyleSheet("margin:5px; padding:2px;")
        self.dark_mode = True
        self.theme_button.clicked.connect(self.toggle_theme)

        # Star radius slider
        self.star_radius = QSlider(Qt.Orientation.Horizontal)
        self.star_radius.setMinimum(3)
        self.star_radius.setMaximum(20)
        self.star_radius.setValue(10)
        self.star_radius.setTickInterval(1)
        self.star_radius.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.star_radius.setStyleSheet("margin:10px;")

        # Median filter size slider
        self.median_filter = QSlider(Qt.Orientation.Horizontal)
        self.median_filter.setMinimum(3)
        self.median_filter.setMaximum(15)
        self.median_filter.setValue(5)
        self.median_filter.setSingleStep(2)
        self.median_filter.setTickInterval(2)
        self.median_filter.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.median_filter.setStyleSheet("margin:10px;")

        # Image display labels
        self.label_orig = QLabel("Image originale")
        self.label_result = QLabel("Résultat")
        self.label_orig.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_orig.setMinimumSize(500, 500)
        self.label_result.setMinimumSize(500, 500)
        self.label_orig.setScaledContents(True)
        self.label_result.setScaledContents(True)
        self.label_orig.setStyleSheet("border:2px solid gray; margin:5px; padding:5px;")
        self.label_result.setStyleSheet("border:2px solid gray; margin:5px; padding:5px;")

        # Top buttons layout
        top_buttons_layout = QHBoxLayout()
        top_buttons_layout.addWidget(self.file_menu_button)
        top_buttons_layout.addStretch()
        top_buttons_layout.addWidget(self.api_button)
        top_buttons_layout.addStretch()
        top_buttons_layout.addWidget(self.theme_button)
        top_buttons_layout.setContentsMargins(10, 10, 10, 10)
        top_buttons_layout.setSpacing(10)

        # Images layout
        images_layout = QHBoxLayout()
        images_layout.addWidget(self.label_orig)
        images_layout.addWidget(self.label_result)
        images_layout.setContentsMargins(10, 10, 10, 10)
        images_layout.setSpacing(20)

        # Star radius layout
        label_star_radius = QLabel("Rayon des étoiles")
        label_star_radius.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_star_radius.setStyleSheet("margin:5px; padding:5px;")
        star_layout = QVBoxLayout()
        star_layout.addWidget(label_star_radius)
        star_layout.addWidget(self.star_radius)
        star_layout.setContentsMargins(5, 5, 5, 5)

        # Median filter layout
        label_median = QLabel("Filtre médian")
        label_median.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_median.setStyleSheet("margin:5px; padding:5px;")
        median_layout = QVBoxLayout()
        median_layout.addWidget(label_median)
        median_layout.addWidget(self.median_filter)
        median_layout.setContentsMargins(5, 5, 5, 5)

        # Sliders layout
        sliders_layout = QHBoxLayout()
        sliders_layout.addLayout(star_layout)
        sliders_layout.addLayout(median_layout)
        sliders_layout.setContentsMargins(10, 10, 10, 10)
        sliders_layout.setSpacing(20)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_buttons_layout)
        main_layout.addLayout(images_layout)
        main_layout.addLayout(sliders_layout)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        self.setLayout(main_layout)

        # Initial theme
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
