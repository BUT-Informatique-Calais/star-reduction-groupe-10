from PyQt6.QtWidgets import QFileDialog
import cv2 as cv

class ImageController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Connect UI events to controller methods
        self.view.load_button.clicked.connect(self.load_image)
        self.view.save_button.clicked.connect(self.save_image)
        self.view.median_filter.sliderReleased.connect(self.update_result)
        self.view.star_radius.sliderReleased.connect(self.update_result)

    def load_image(self):
        """Open a file dialog and load a FITS image"""
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Choose a FITS file", "", "FITS Files (*.fits)"
        )
        if file_path:
            self.model.load_fits(file_path)
            self.view.update_image(self.view.label_orig, self.model.image_orig)
            self.update_result()

    def save_image(self):
        """Save the processed image to disk"""
        if self.model.I_final_normalized is None:
            return
        file_path, _ = QFileDialog.getSaveFileName(
            None, "Save image", "", "PNG Files (*.png)"
        )
        if file_path:
            if not file_path.lower().endswith(".png"):
                file_path += ".png"
            cv.imwrite(file_path, self.model.I_final_normalized)

    def update_result(self):
        """Update the result image when parameters change"""
        if self.model.image_orig is None:
            return

        # Update model parameters from sliders
        self.model.mask_radius = self.view.star_radius.value()
        self.model.median_size = self.view.median_filter.value()

        # Recompute star reduction
        result = self.model.apply_star_reduction()
        self.view.update_image(self.view.label_result, result)

