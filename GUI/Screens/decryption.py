import flet as ft
import Cryptography
import Steganography
from GUI.Constants import TextStyle
import os
import base64

class Decryption:
    def __init__(self, page, generated_key=None):
        self.page = page
        self.image_file_path = ""
        self.generated_key = generated_key  # Store the generated key passed from GenerateKey
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

            # Update this path to the correct key file directory
            key_file_path = fr"c:\Users\Ray04\Desktop\coding\UNI\StegChain\Key_file\{self.key_file_name.value}.txt.enc"
            
            # Debugging print to check the key file path
            print(f"Key file path: {key_file_path}")

            # Check existence of key file using os.path.exists()
            if not os.path.exists(key_file_path):
                print("Key file does not exist!")  # Debugging print
                self.show_response("Key File not found! Please generate it first.", is_error=True)
                return

            try:
                # Decrypt the key
                decrypted_key = Cryptography.Decrypter("").decrypt_file(key_file_path).decode("utf-8")
                
                # Ensure key is of the correct length (16, 24, or 32 bytes)
                if len(decrypted_key) not in [16, 24, 32]:
                    decrypted_key = decrypted_key[:32]  # Truncate or pad if needed to 32 bytes

                # Autofill the key field with the decrypted key
                self.key_data.value = decrypted_key
                self.key_data.update()

                # Check if the provided key matches the decrypted key
                if decrypted_key != self.key_data.value.strip():
                    self.show_response("Incorrect Key Value.", is_error=True)
                    return

                # Decode the stego image
                encoded_data = Steganography.Decoding.decode(self.image_file_path)

                # Decrypt the extracted data
                plain_text = Cryptography.Decrypter("").decrypt(base64.b64decode(encoded_data))

                # Update the output window with the decrypted message
                self.output_window.value = plain_text.decode("utf-8")
                self.output_window.update()

                # Display success message
                self.show_response("Decryption successful!", is_error=False)

            except Exception as err:
                # Catch any errors and display the message
                self.show_response(f"Error during decryption: {str(err)}", is_error=True)

        def on_file_selected(e: ft.FilePickerResultEvent):
            if e.files:
                self.image_file_path = e.files[0].path

        # File picker for selecting the image
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
