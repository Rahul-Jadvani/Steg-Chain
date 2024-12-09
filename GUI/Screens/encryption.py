import flet as ft
import os
import base64
from Cryptography import KeyGeneration, Encrypter
from Steganography import Encoding
from GUI.Constants import TextStyle
from config import CONFIG


class Encryption:

    def __init__(self, page):
        self.page = page
        super().__init__()

    information = "Choose an image file and key to encrypt the data and generate a stego image..."
    image_path = ""
    image_file_name = ""
    key_file_name = ft.TextField(
        label="Key File Name",
        hint_text="Enter Key File Name",
        width=500.0,
        border_color=ft.colors.INDIGO_200,
    )

    key_data = ft.TextField(
        label="Enter Data",
        hint_text="Enter Your Message Here",
        width=500.0,
        multiline=True,
        border_color=ft.colors.INDIGO_200,
        min_lines=5,
        max_lines=5,
    )
    
    response_message = ft.Text(
        "",
        color=ft.colors.GREEN_ACCENT,
    )

    def encryption(self):
        def handle_encrypt_event(e):
            if self.image_path == "":
                self.response_message.value = "Please choose an image..."
                self.response_message.color = ft.colors.RED_ACCENT
                self.response_message.update()
                return

            if len(self.key_file_name.value) == 0:
                self.response_message.value = "Key file is required..."
                self.response_message.color = ft.colors.RED_ACCENT
                self.response_message.update()
                return

            if len(self.key_data.value) == 0:
                self.response_message.value = "Data is required..."
                self.response_message.color = ft.colors.RED_ACCENT
                self.response_message.update()
                return

            # Key file path
            key_file_path = fr"c:\Users\Ray04\Desktop\coding\UNI\StegChain\Key_file\{self.key_file_name.value}.txt.enc"

            # Debugging print to check the key file path
            print(f"Key file path: {key_file_path}")

            # Check existence of key file using os.path.exists()
            if not os.path.exists(key_file_path):
                print("Key file does not exist!")  # Debugging print
                self.response_message.value = (
                    "Key file not found! If not generated, please generate it."
                )
                self.response_message.color = ft.colors.RED_ACCENT
                self.response_message.update()
                return

            try:
                # Read the encryption key
                with open(key_file_path, "rb") as key_file:
                    key = key_file.read()

                CONFIG['global_message'] = self.key_data.value

                # Encrypt the provided data
                data_to_encrypt = CONFIG['global_message'].encode()
                encrypter = Encrypter(key)
                encrypted_data = encrypter.encrypt(data_to_encrypt)

                # Encode the encrypted data to base64 for steganography
                encoded_data = base64.b64encode(encrypted_data).decode()

                # Define destination path for the stego image
                destination_image_path = fr"c:\Users\Ray04\Desktop\coding\UNI\StegChain\EncImg\{self.image_file_name}"

                # Use Steganography to encode the encrypted data into the image
                Encoding.encode(self.image_path, encoded_data, destination_image_path)

                global_message = self.key_data.value

                print(global_message)

                self.response_message.value = "Encrypted image saved successfully!"
                self.response_message.color = ft.colors.GREEN_ACCENT
                self.response_message.update()

            except Exception as ex:
                self.response_message.value = f"Error during encryption: {str(ex)}"
                self.response_message.color = ft.colors.RED_ACCENT
                self.response_message.update()

        def on_dialog_result(e: ft.FilePickerResultEvent):
            if e.files:
                self.image_path = e.files[0].path
                self.image_file_name = e.files[0].name

        # File picker
        my_pick = ft.FilePicker(on_result=on_dialog_result)
        self.page.overlay.append(my_pick)

        # Build UI components
        return ft.Container(
            expand=True,
            content=ft.Column(
                [
                    ft.Text(
                        "Encryption",
                        size=TextStyle.HEADERFONTSIZE
                    ),
                    ft.Container(height=10.0, width=10.0),
                    ft.Container(
                        width=500.0,
                        content=ft.Row(
                            [
                                ft.Icon(
                                    name=ft.icons.INFO_ROUNDED,
                                    color=ft.colors.INDIGO_200
                                ),
                                ft.Text(self.information, width=480.0),
                            ],
                        ),
                    ),
                    ft.Container(
                        width=500.0,
                        content=ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Pick Image File",
                                    icon=ft.icons.UPLOAD_FILE,
                                    on_click=lambda _: my_pick.pick_files(),
                                ),
                            ],
                        ),
                    ),
                    self.key_file_name,
                    self.key_data,
                    ft.FilledButton(text="Encrypt Image", on_click=handle_encrypt_event),
                    self.response_message,
                ],
                alignment=ft.alignment.top_left,
                expand=True,
            ),
            alignment=ft.alignment.center,
        )
