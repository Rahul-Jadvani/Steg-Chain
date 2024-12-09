import flet as ft
import cv2
import numpy as np
import matplotlib
from io import BytesIO
from typing import Optional
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Configure Matplotlib to use Agg backend
matplotlib.use('Agg')


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
        if len(img1.shape) > 2:
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        img1 = img1.astype(np.float64)
        img2 = img2.astype(np.float64)

        mu1, mu2 = np.mean(img1), np.mean(img2)
        sigma1, sigma2 = np.var(img1), np.var(img2)

        k1, k2 = 0.01, 0.03
        L = 255

        numerator = (2 * mu1 * mu2 + (k1 * L) ** 2) * (2 * sigma1 * sigma2 + (k2 * L) ** 2)
        denominator = (mu1 ** 2 + mu2 ** 2 + (k1 * L) ** 2) * (sigma1 + sigma2 + (k2 * L) ** 2)

        return numerator / denominator if denominator != 0 else 1.0


class Difference:
    def __init__(self, page: ft.Page):
        self.page = page
        self._original_image_path: Optional[str] = None
        self._stego_image_path: Optional[str] = None
        self.information = "Choose both Original and Stego Images to calculate the differences."

        self.response_message = ft.Text("", color=ft.colors.GREEN_ACCENT_700)
        self.psnr = ft.Text("PSNR: N/A", color=ft.colors.WHITE)
        self.mse = ft.Text("MSE: N/A", color=ft.colors.WHITE)
        self.ssim = ft.Text("SSIM: N/A", color=ft.colors.WHITE)

    def difference_panel(self) -> ft.Container:
        def handle_calculate_event(e):
            if not self._original_image_path or not self._stego_image_path:
                self.show_response("Both images must be selected.", is_error=True)
                return

            try:
                original = self._load_image(self._original_image_path)
                stego = self._load_image(self._stego_image_path)

                if original.shape != stego.shape:
                    raise ValueError("Images must have identical dimensions.")

                psnr_value = DifferenceStego.calculatePSNR(original, stego)
                mse_value = DifferenceStego.calculateMSE(original, stego)
                ssim_value = DifferenceStego.calculateSSIM(original, stego)

                self._update_metrics(psnr_value, mse_value, ssim_value)
                self._generate_and_display_graphs_external(original, stego, psnr_value, mse_value, ssim_value)

            except Exception as err:
                self.show_response(f"Analysis Error: {str(err)}", is_error=True)
                self._reset_metrics()

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
        image = cv2.imread(path)
        if image is None:
            raise ValueError(f"Failed to load image from path: {path}")
        return image

    def _on_original_selected(self, e: ft.FilePickerResultEvent):
        if e.files:
            self._original_image_path = e.files[0].path
            self.show_response("Original image selected", is_error=False)

    def _on_stego_selected(self, e: ft.FilePickerResultEvent):
        if e.files:
            self._stego_image_path = e.files[0].path
            self.show_response("Stego image selected", is_error=False)

    def show_response(self, message: str, is_error: bool = False):
        self.response_message.value = message
        self.response_message.color = ft.colors.RED_ACCENT_700 if is_error else ft.colors.GREEN_ACCENT_700
        self.response_message.update()

    def _update_metrics(self, psnr_value: float, mse_value: float, ssim_value: float):
        self.psnr.value = f"PSNR: {psnr_value:.2f}"
        self.mse.value = f"MSE: {mse_value:.4f}"
        self.ssim.value = f"SSIM: {ssim_value:.4f}"

        self.psnr.update()
        self.mse.update()
        self.ssim.update()

        self.show_response("Difference calculated successfully!", is_error=False)

    def _reset_metrics(self):
        self.psnr.value = "PSNR: N/A"
        self.mse.value = "MSE: N/A"
        self.ssim.value = "SSIM: N/A"

        self.psnr.update()
        self.mse.update()
        self.ssim.update()

    def _generate_and_display_graphs_external(self, original, stego, psnr_value, mse_value, ssim_value):
        try:
            plt.close('all')

            fig, axes = plt.subplots(4, 3, figsize=(20, 24))
            plt.subplots_adjust(hspace=0.5, wspace=0.5)

            # Original and Stego Images
            axes[0, 0].imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
            axes[0, 0].set_title("Original Image")
            axes[0, 0].axis('off')

            axes[0, 1].imshow(cv2.cvtColor(stego, cv2.COLOR_BGR2RGB))
            axes[0, 1].set_title("Stego Image")
            axes[0, 1].axis('off')

            # Difference Image
            diff = cv2.absdiff(original, stego)
            axes[0, 2].imshow(cv2.cvtColor(diff, cv2.COLOR_BGR2RGB))
            axes[0, 2].set_title("Difference Image")
            axes[0, 2].axis('off')

            # PSNR, MSE, and SSIM Bar Graphs
            axes[1, 0].barh([0], [psnr_value], color='green')
            axes[1, 0].set_title(f"PSNR: {psnr_value:.2f}")
            axes[1, 0].axis('off')

            axes[1, 1].barh([0], [mse_value], color='blue')
            axes[1, 1].set_title(f"MSE: {mse_value:.4f}")
            axes[1, 1].axis('off')

            axes[1, 2].barh([0], [ssim_value], color='red')
            axes[1, 2].set_title(f"SSIM: {ssim_value:.4f}")
            axes[1, 2].axis('off')

            # Histograms for Original and Stego Images
            for i, color in enumerate(['b', 'g', 'r']):
                axes[2, 0].hist(original[:, :, i].ravel(), bins=256, color=color, alpha=0.5, label=f'Original {color.upper()}')
                axes[2, 1].hist(stego[:, :, i].ravel(), bins=256, color=color, alpha=0.5, label=f'Stego {color.upper()}')

            axes[2, 0].set_title("Original Image Histogram")
            axes[2, 0].legend()
            axes[2, 1].set_title("Stego Image Histogram")
            axes[2, 1].legend()

            # Heatmap of Pixel-Wise Differences
            diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            axes[2, 2].imshow(diff_gray, cmap='hot', interpolation='nearest')
            axes[2, 2].set_title("Difference Heatmap")
            axes[2, 2].axis('off')

            # Average Pixel Intensities Line Graphs
            avg_original = np.mean(original, axis=(0, 1))
            avg_stego = np.mean(stego, axis=(0, 1))

            axes[3, 0].plot(avg_original, label="Original Avg Intensity", color='blue', marker='o')
            axes[3, 0].plot(avg_stego, label="Stego Avg Intensity", color='red', marker='x')
            axes[3, 0].set_title("Average Pixel Intensity Comparison")
            axes[3, 0].legend()

            # Combined Histogram Comparison
            axes[3, 1].hist(original.ravel(), bins=256, color='blue', alpha=0.5, label='Original')
            axes[3, 1].hist(stego.ravel(), bins=256, color='red', alpha=0.5, label='Stego')
            axes[3, 1].set_title("Combined Histogram")
            axes[3, 1].legend()

            # Text Summary of Metrics
            summary_text = f"""
            Summary:
            PSNR: {psnr_value:.2f}
            MSE: {mse_value:.4f}
            SSIM: {ssim_value:.4f}
            """
            axes[3, 2].text(0.5, 0.5, summary_text, fontsize=12, ha='center', va='center')
            axes[3, 2].set_title("Metrics Summary")
            axes[3, 2].axis('off')

            # Display Graphs in Tkinter Window
            root = tk.Tk()
            root.title("Graph Visualization")

            canvas = FigureCanvasTkAgg(fig, master=root)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            root.mainloop()

        except Exception as e:
            self.show_response(f"Graph generation failed: {str(e)}", is_error=True)
