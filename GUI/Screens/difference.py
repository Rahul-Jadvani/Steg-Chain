import flet as ft
import cv2
import numpy as np
import matplotlib
from io import BytesIO
from typing import Optional

matplotlib.use('Agg')  # Use the Agg backend to avoid GUI interaction
import matplotlib.pyplot as plt

class DifferenceStego:
    """
    Mock class for Difference Steganography calculations.
    Replace with actual implementation from your Steganography module.
    """
    @staticmethod
    def calculatePSNR(img1, img2):
        """Calculate Peak Signal-to-Noise Ratio"""
        mse = np.mean((img1 - img2) ** 2)
        if mse == 0:
            return 100
        max_pixel = 255.0
        return 20 * np.log10(max_pixel / np.sqrt(mse))

    @staticmethod
    def calculateMSE(img1, img2):
        """Calculate Mean Squared Error"""
        return np.mean((img1 - img2) ** 2)

    @staticmethod
    def calculateSSIM(img1, img2):
        """
        Simplified SSIM calculation.
        For full implementation, consider using skimage.metrics.structural_similarity
        """
        # Convert images to grayscale if they're color
        if len(img1.shape) > 2:
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        # Normalize pixel values
        img1 = img1.astype(np.float64)
        img2 = img2.astype(np.float64)
        
        # Calculate mean
        mu1 = np.mean(img1)
        mu2 = np.mean(img2)
        
        # Calculate variance
        sigma1 = np.var(img1)
        sigma2 = np.var(img2)
        
        # Constants for stability
        k1, k2 = 0.01, 0.03
        L = 255  # Dynamic range of pixel values
        
        # Calculate SSIM
        numerator = (2 * mu1 * mu2 + (k1 * L)**2) * (2 * sigma1 * sigma2 + (k2 * L)**2)
        denominator = (mu1**2 + mu2**2 + (k1 * L)**2) * (sigma1 + sigma2 + (k2 * L)**2)
        
        return numerator / denominator if denominator != 0 else 1.0

class Difference:
    def __init__(self, page: ft.Page):
        """
        Initialize the Difference analysis panel.
        
        :param page: Flet page object for UI interactions
        """
        self.page = page
        self._original_image_path: Optional[str] = None
        self._stego_image_path: Optional[str] = None
        self.information = "Choose both Original and Stego Images to calculate the differences."
        
        # UI Elements
        self.response_message = ft.Text("", color=ft.colors.GREEN_ACCENT_700)
        self.psnr = ft.Text("PSNR: N/A", color=ft.colors.WHITE)
        self.mse = ft.Text("MSE: N/A", color=ft.colors.WHITE)
        self.ssim = ft.Text("SSIM: N/A", color=ft.colors.WHITE)

    def difference_panel(self) -> ft.Container:
        """
        Create the difference analysis panel UI.
        
        :return: Flet Container with difference analysis controls
        """
        def handle_calculate_event(e):
            """Handle the calculation of image differences"""
            if not self._original_image_path or not self._stego_image_path:
                self.show_response("Both images must be selected.", is_error=True)
                return

            try:
                # Load images
                original = self._load_image(self._original_image_path)
                stego = self._load_image(self._stego_image_path)

                # Validate image dimensions
                if original.shape != stego.shape:
                    raise ValueError("Images must have identical dimensions.")

                # Calculate metrics
                psnr_value = DifferenceStego.calculatePSNR(original, stego)
                mse_value = DifferenceStego.calculateMSE(original, stego)
                ssim_value = DifferenceStego.calculateSSIM(original, stego)

                # Update metrics display
                self._update_metrics(psnr_value, mse_value, ssim_value)

                # Generate and display graphs
                self._generate_and_display_graphs(original, stego, psnr_value, mse_value, ssim_value)

            except Exception as err:
                self.show_response(f"Analysis Error: {str(err)}", is_error=True)
                # Reset metrics to default
                self._reset_metrics()

        # File picker setup
        original_picker = ft.FilePicker(on_result=self._on_original_selected)
        stego_picker = ft.FilePicker(on_result=self._on_stego_selected)
        self.page.overlay.extend([original_picker, stego_picker])

        return ft.Container(
            expand=True,
            content=ft.Column(
                [
                    ft.Text("Compare Images", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text(self.information, width=500.0),
                    ft.ElevatedButton("Select Original Image", on_click=lambda _: original_picker.pick_files(
                        allowed_extensions=['jpg', 'jpeg', 'png', 'bmp', 'gif']
                    )),
                    ft.ElevatedButton("Select Stego Image", on_click=lambda _: stego_picker.pick_files(
                        allowed_extensions=['jpg', 'jpeg', 'png', 'bmp', 'gif']
                    )),
                    ft.FilledButton("Calculate Differences", on_click=handle_calculate_event),
                    self.response_message,
                    self.psnr,
                    self.mse,
                    self.ssim,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
        )

    def _load_image(self, path: str) -> np.ndarray:
        """
        Safely load an image with comprehensive error checking.
        
        :param path: Path to the image file
        :return: Numpy array representing the image
        :raises ValueError: If image cannot be loaded
        """
        image = cv2.imread(path)
        if image is None:
            raise ValueError(f"Failed to load image from path: {path}")
        return image

    def _on_original_selected(self, e: ft.FilePickerResultEvent):
        """Handle original image selection with error checking"""
        if e.files:
            self._original_image_path = e.files[0].path
            self.show_response("Original image selected", is_error=False)

    def _on_stego_selected(self, e: ft.FilePickerResultEvent):
        """Handle stego image selection with error checking"""
        if e.files:
            self._stego_image_path = e.files[0].path
            self.show_response("Stego image selected", is_error=False)

    def show_response(self, message: str, is_error: bool = False):
        """
        Display a response message with appropriate color coding.
        
        :param message: Message to display
        :param is_error: Flag to indicate if message is an error
        """
        self.response_message.value = message
        self.response_message.color = ft.colors.RED_ACCENT_700 if is_error else ft.colors.GREEN_ACCENT_700
        self.response_message.update()

    def _update_metrics(self, psnr_value: float, mse_value: float, ssim_value: float):
        """
        Update metric display texts.
        
        :param psnr_value: Peak Signal-to-Noise Ratio
        :param mse_value: Mean Squared Error
        :param ssim_value: Structural Similarity Index
        """
        self.psnr.value = f"PSNR: {psnr_value:.2f}"
        self.mse.value = f"MSE: {mse_value:.4f}"
        self.ssim.value = f"SSIM: {ssim_value:.4f}"
        
        self.psnr.update()
        self.mse.update()
        self.ssim.update()
        
        self.show_response("Difference calculated successfully!", is_error=False)

    def _reset_metrics(self):
        """Reset metrics to default values"""
        self.psnr.value = "PSNR: N/A"
        self.mse.value = "MSE: N/A"
        self.ssim.value = "SSIM: N/A"
        
        self.psnr.update()
        self.mse.update()
        self.ssim.update()

    def _generate_and_display_graphs(self, original, stego, psnr_value, mse_value, ssim_value):
        """
        Generate comparison graphs and display in the Flet UI.
        
        :param original: Original image numpy array
        :param stego: Stego image numpy array
        :param psnr_value: Peak Signal-to-Noise Ratio
        :param mse_value: Mean Squared Error
        :param ssim_value: Structural Similarity Index
        """
        try:
            plt.close('all')  # Close any existing plots to prevent resource leaks

            # Create a figure with multiple subplots
            fig, axes = plt.subplots(3, 2, figsize=(15, 18))
            plt.subplots_adjust(hspace=0.4, wspace=0.3)

            # Plot Original Image
            axes[0, 0].imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
            axes[0, 0].set_title("Original Image")
            axes[0, 0].axis('off')

            # Plot Stego Image
            axes[0, 1].imshow(cv2.cvtColor(stego, cv2.COLOR_BGR2RGB))
            axes[0, 1].set_title("Stego Image")
            axes[0, 1].axis('off')

            # Plot Difference Image
            diff = cv2.absdiff(original, stego)
            axes[1, 0].imshow(cv2.cvtColor(diff, cv2.COLOR_BGR2RGB))
            axes[1, 0].set_title("Difference Image")
            axes[1, 0].axis('off')

            # Plot PSNR
            axes[1, 1].barh([0], [psnr_value], color='green')
            axes[1, 1].set_title(f"PSNR: {psnr_value:.2f}")
            axes[1, 1].axis('off')

            # Plot MSE
            axes[2, 0].barh([0], [mse_value], color='blue')
            axes[2, 0].set_title(f"MSE: {mse_value:.4f}")
            axes[2, 0].axis('off')

            # Plot SSIM
            axes[2, 1].barh([0], [ssim_value], color='red')
            axes[2, 1].set_title(f"SSIM: {ssim_value:.4f}")
            axes[2, 1].axis('off')

            # Convert Matplotlib figure to image
            buf = BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            image = ft.Image(src=buf)
            self.page.add(image)

        except Exception as e:
            self.show_response(f"Graph generation failed: {str(e)}", is_error=True)
            print(f"Error in graph generation: {e}")
