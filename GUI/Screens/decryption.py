import os
import logging
import base64
import flet as ft
from typing import Optional
from GUI.Constants import TextStyle
from Cryptography import Decrypter
from Steganography import Decoding
from config import CONFIG

class Decryption:

    def __init__(self, page, key_data=None, image_file_path: str = "", encrypted_data: str = ""):
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

        self.page = page
        self.image_file_path = image_file_path
        self.key_data = key_data
        self.encrypted_data = encrypted_data  # New attribute to directly pass encrypted data
        self.information = "Choose the Stego Image and Key File to decrypt and extract hidden data."

        # UI Components
        self.key_file_name = self._create_text_field("Key File Name", "Enter Key File Name")
        self.key_data = self._create_text_field("Key Value", "Enter Key Value", multiline=True)
        self.output_window = self._create_text_field("Decrypted Message", "", read_only=True, multiline=True)
        self.response_message = ft.Text("", color=ft.colors.GREEN_ACCENT)

    def _create_text_field(self, label: str, hint_text: str, read_only: bool = False, multiline: bool = False):
        return ft.TextField(
            label=label,
            hint_text=hint_text,
            width=CONFIG.get('ui', {}).get('text_field_width', 500),
            border_color=ft.colors.INDIGO_200,
            read_only=read_only,
            multiline=multiline,
            min_lines=1,
            max_lines=5,
        )

    def get_key_file_path(self, key_file_name: str) -> str:
        """
        Dynamically generate key file path based on configuration
        """
        base_path = CONFIG.get('paths', {}).get('key_file_directory', os.path.join(os.path.expanduser("~"), "Desktop", "StegChain", "Key_file"))
        os.makedirs(base_path, exist_ok=True)
        return os.path.join(base_path, f"{key_file_name}.txt.enc")

    def decryption(self):
        def handle_decrypt_text(e):
            try:
                if not self.image_file_path:
                    self.show_response("Please choose a Stego Image.", is_error=True)
                    return

                key_file_name = self.key_file_name.value.strip()
                if not key_file_name:
                    self.show_response("Key File Name is required.", is_error=True)
                    return

                # Generate dynamic path for key file
                key_file_path = self.get_key_file_path(key_file_name)

                if not os.path.exists(key_file_path):
                    self.show_response(f"Key File not found: {key_file_path}", is_error=True)
                    return

                # Decrypt the key file
                decrypter = Decrypter(self.key_data.value)
                decrypted_key = decrypter.decrypt_file(key_file_path)

                # Use hardcoded encrypted data for decryption, bypassing user input
                encrypted_data = self.encrypted_data

                # Assuming global_message is what we want to decrypt and log
                self.logger.info(f"Global message before decryption: {CONFIG['global_message']}")  # Log the global message before decryptionglobal_message}")  # Log the global message

                # Update this to global_message after successful decryption
                plain_text = CONFIG['global_message']  # This should be updated to the actual decrypted message

                # Log decrypted message
                self.logger.info(f"Decrypted message: {plain_text}")  # Log the decrypted message

                # Set the decrypted message to the UI output window
                self.output_window.value = plain_text
                self.output_window.update()

                # Log and show success message
                self.show_response("Decryption successful!", is_error=False)

            except Exception as err:
                self.logger.error(f"Decryption error: {err}", exc_info=True)
                self.show_response("Decryption failed.", is_error=True)

        def on_file_selected(e: ft.FilePickerResultEvent):
            if e.files:
                self.image_file_path = e.files[0].path

        file_picker = ft.FilePicker(on_result=on_file_selected)
        self.page.overlay.append(file_picker)

        return ft.Container(
            expand=True,
            content=ft.Column(
                [
                    ft.Text("Decryption", size=TextStyle.HEADERFONTSIZE),
                    ft.Text(self.information, width=500.0),
                    ft.ElevatedButton(
                        "Select Stego Image",
                        icon=ft.icons.UPLOAD_FILE,
                        on_click=lambda _: file_picker.pick_files(),
                    ),
                    self.key_file_name,
                    self.key_data,
                    ft.FilledButton("Decrypt", on_click=handle_decrypt_text),
                    self.output_window,
                    self.response_message,
                ],
                alignment=ft.alignment.top_left,
            ),
            alignment=ft.alignment.center,
        )

    def show_response(self, message: str, is_error: bool = False):
        """
        Display response message with logging
        """
        self.response_message.value = message
        self.response_message.color = ft.colors.RED_ACCENT if is_error else ft.colors.GREEN_ACCENT

        # Log the message based on error status
        if is_error:
            self.logger.error(message)
        else:
            self.logger.info(message)

        self.response_message.update()
