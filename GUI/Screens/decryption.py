import flet as ft
import base64
import os
from GUI.Constants import TextStyle
from Cryptography import Decrypter
from Steganography import Decoding  # Assuming `Decoding` handles steganography decoding logic

class Decryption:
    def __init__(self, page, generated_key=None, image_file_path=""):
        self.page = page
        self.image_file_path = image_file_path
        self.generated_key = generated_key
        self.information = "Choose the Stego Image and Key File to decrypt and extract hidden data."
        
        self.key_file_name = ft.TextField(
            label="Key File Name",
            hint_text="Enter Key File Name",
            width=500.0,
            border_color=ft.colors.INDIGO_200,
        )
        self.key_data = ft.TextField(
            label="Key Value",
            hint_text="Enter Key Value",
            width=500.0,
            multiline=True,
            border_color=ft.colors.INDIGO_200,
            min_lines=1,
            max_lines=5,
        )
        self.output_window = ft.TextField(
            label="Decrypted Message",
            read_only=True,
            width=500.0,
            multiline=True,
            border_color=ft.colors.INDIGO_200,
            min_lines=5,
            max_lines=5,
        )
        self.response_message = ft.Text("", color=ft.colors.GREEN_ACCENT)

        # Auto-fill the key field with the generated key if available
        if self.generated_key:
            self.key_data.value = self.generated_key
            self.key_data.update()

    def decryption(self):
        def handle_decrypt_text(e):
            if not self.image_file_path:
                self.show_response("Please choose a Stego Image.", is_error=True)
                return

            if not self.key_file_name.value.strip():
                self.show_response("Key File Name is required.", is_error=True)
                return

            # Path to the encrypted key file
            key_file_path = fr"c:\Users\Ray04\Desktop\coding\UNI\StegChain\Key_file\{self.key_file_name.value}.txt.enc"
            if not os.path.exists(key_file_path):
                self.show_response("Key File not found! Please generate it first.", is_error=True)
                return

            try:
                # Decrypt the key
                decrypter = Decrypter("")  # Create decrypter with empty key for file decryption
                decrypted_key = decrypter.decrypt_file(key_file_path).decode("utf-8")

                # Ensure key is valid for AES (16, 24, 32 bytes)
                if len(decrypted_key) not in [16, 24, 32]:
                    raise ValueError("Invalid key length. Key must be 16, 24, or 32 bytes.")

                # Autofill the key field with the decrypted key
                self.key_data.value = decrypted_key
                self.key_data.update()

                # Decode the stego image
                encoded_data = Decoding.decode(self.image_file_path)

                # Decrypt the extracted data
                actual_decrypter = Decrypter(decrypted_key.encode("utf-8"))
                plain_text = actual_decrypter.decrypt(base64.b64decode(encoded_data))

                # Update the output window
                self.output_window.value = plain_text.decode("utf-8")
                self.output_window.update()

                # Display success message
                self.show_response("Decryption successful!", is_error=False)

            except Exception as err:
                self.show_response(f"Error during decryption: {str(err)}", is_error=True)

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

    def show_response(self, message, is_error=False):
        self.response_message.value = message
        self.response_message.color = ft.colors.RED_ACCENT if is_error else ft.colors.GREEN_ACCENT
        self.response_message.update()
