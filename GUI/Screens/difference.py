import flet as ft
import cv2
from Steganography import DifferenceStego
from GUI.Constants import TextStyle

class Difference:
    def __init__(self, page):
        self.page = page
        self.original_image_path = ""
        self.stego_image_path = ""
        self.information = "Choose both Original and Stego Images to calculate the differences."
        self.response_message = ft.Text("", color=ft.colors.GREEN_ACCENT)
        self.psnr = ft.Text("", color=ft.colors.WHITE)
        self.mse = ft.Text("", color=ft.colors.WHITE)
        self.ssim = ft.Text("", color=ft.colors.WHITE)

    def difference_panel(self):
        def handle_calculate_event(e):
            if not self.original_image_path or not self.stego_image_path:
                self.show_response("Both images must be selected.", is_error=True)
                return

            try:
                original = cv2.imread(self.original_image_path)
                stego = cv2.imread(self.stego_image_path)
                if original is None or stego is None:
                    raise ValueError("Failed to load one or both images.")

                self.psnr.value = f"PSNR: {DifferenceStego.calculatePSNR(original, stego)}"
                self.mse.value = f"MSE: {DifferenceStego.calculateMSE(original, stego)}"
                self.ssim.value = f"SSIM: {DifferenceStego.calculateSSIM(original, stego)}"

                self.psnr.update()
                self.mse.update()
                self.ssim.update()
                self.show_response("Difference calculated successfully!", is_error=False)

            except Exception as err:
                self.show_response(f"Error: {str(err)}", is_error=True)

        def on_original_selected(e: ft.FilePickerResultEvent):
            if e.files:
                self.original_image_path = e.files[0].path

        def on_stego_selected(e: ft.FilePickerResultEvent):
            if e.files:
                self.stego_image_path = e.files[0].path

        original_picker = ft.FilePicker(on_result=on_original_selected)
        stego_picker = ft.FilePicker(on_result=on_stego_selected)
        self.page.overlay.extend([original_picker, stego_picker])

        return ft.Container(
            expand=True,
            content=ft.Column(
                [
                    ft.Text("Compare Images", size=TextStyle.HEADERFONTSIZE),
                    ft.Text(self.information, width=500.0),
                    ft.ElevatedButton("Select Original Image", on_click=lambda _: original_picker.pick_files()),
                    ft.ElevatedButton("Select Stego Image", on_click=lambda _: stego_picker.pick_files()),
                    ft.FilledButton("Calculate", on_click=handle_calculate_event),
                    self.response_message,
                    self.psnr,
                    self.mse,
                    self.ssim,
                ],
            ),
            alignment=ft.alignment.center,
        )

    def show_response(self, message, is_error=False):
        self.response_message.value = message
        self.response_message.color = ft.colors.RED_ACCENT if is_error else ft.colors.GREEN_ACCENT
        self.response_message.update()
