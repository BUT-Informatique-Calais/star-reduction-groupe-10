from PyQt6.QtWidgets import QFileDialog
from optimisation import StarReductionThread


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
            import cv2 as cv
            cv.imwrite(file_path, self.model.I_final_normalized)
    def update_result(self):
        if self.model.image_orig is None:
            return

        # Update parameters
        self.model.mask_radius = self.view.star_radius.value()
        self.model.median_size = self.view.median_filter.value()

        # Désactive les sliders pour éviter de spammer le thread
        self.view.star_radius.setEnabled(False)
        self.view.median_filter.setEnabled(False)

        # Crée et démarre le thread
        self.thread = StarReductionThread(self.model)
        self.thread.finished.connect(self.on_thread_finished)
        self.thread.start()


    def on_thread_finished(self, result):
        self.view.update_image(self.view.label_result, result)
        # Réactive les sliders
        self.view.star_radius.setEnabled(True)
        self.view.median_filter.setEnabled(True)
