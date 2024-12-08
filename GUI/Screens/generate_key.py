import flet as ft
import Cryptography
from GUI.Constants import TextStyle

class GenerateKey:
    def __init__(self):
        self.information = "Enter Key File Name and Value to generate an encrypted key file."
        self.response_message = ft.Text("", color=ft.colors.GREEN_ACCENT)
        self.key_file_name_box = ft.TextField(
            label="Key File Name",
            hint_text="Enter Key File Name",
            width=500.0,
        )
        self.key_value_box = ft.TextField(
            label="Key Value",
            hint_text="Enter Key Value",
            width=500.0,
            multiline=True,
            min_lines=1,
            max_lines=3,
        )
        self.generated_key = None  # Store the generated key here

    def generate_key(self):
        def handle_create_key_generation(e):
            if not self.key_file_name_box.value.strip() or not self.key_value_box.value.strip():
                self.show_response("Both fields are required.", is_error=True)
                return

            try:
                file_path = fr"c:\Users\Ray04\Desktop\coding\UNI\StegChain\Key_file\{self.key_file_name_box.value.strip()}"
                
                # Create the key and print it
                key = self.key_value_box.value.strip()
                if Cryptography.KeyGeneration.createkeyfile(file_path, key):
                    # Print the key and store it in self.generated_key
                    self.generated_key = key
                    print(f"Generated Key: {key}")
                    self.show_response("Key generated successfully!", is_error=False)
                else:
                    self.show_response("Failed to generate key.", is_error=True)

            except Exception as err:
                self.show_response(f"Error: {str(err)}", is_error=True)

        return ft.Container(
            expand=True,
            content=ft.Column(
                [
                    ft.Text("Generate Key", size=TextStyle.HEADERFONTSIZE),
                    ft.Text(self.information, width=500.0),
                    self.key_file_name_box,
                    self.key_value_box,
                    ft.FilledButton("Generate", on_click=handle_create_key_generation),
                    self.response_message,
                ],
            ),
            alignment=ft.alignment.center,
        )

    def show_response(self, message, is_error=False):
        self.response_message.value = message
        self.response_message.color = ft.colors.RED_ACCENT if is_error else ft.colors.GREEN_ACCENT
        self.response_message.update()

    def get_generated_key(self):
        return self.generated_key  # Method to retrieve the generated key
