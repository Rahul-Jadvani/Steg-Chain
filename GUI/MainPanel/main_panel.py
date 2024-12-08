from flet import *
import time
import traceback
from typing import Callable
from GUI.Screens import HomeScreen, GenerateKey, Encryption, Decryption, Difference


class MainPanel:
    def __init__(self):
        self.current_page: str = "HOME"

    def main(self, page: Page):
        # Configure page settings
        page.title = "Image Steganography"
        page.horizontal_alignment = "center"
        page.vertical_alignment = "center"

        # Wrapper for sidebar and main content
        wrapper = [
            Container(
                width=200,
                height=580,
                animate=animation.Animation(500, "decelerate"),
                border_radius=10,
                padding=10,
                content=None,  # Placeholder; this will be set to the sidebar
            ),
            HomeScreen().home_screen(),  # Initial content
        ]

        # Function to update the screen
        def update_screen(screen_name: str, screen_generator: Callable):
            """
            Update the screen dynamically and handle errors gracefully.

            Args:
                screen_name (str): Name of the screen to switch to.
                screen_generator (Callable): Function to generate the screen's UI.
            """
            try:
                # Set the current screen and update the main content
                self.current_page = screen_name
                new_screen = screen_generator()

                # Debugging: Show the type of the returned component
                print(f"Debug: Screen Generator for {screen_name} returned a component of type {type(new_screen)}")

                # Check if the returned component is a valid Flet control
                if not isinstance(new_screen, Control):
                    raise TypeError(
                        f"The screen generator for {screen_name} did not return a valid Flet component."
                    )

                # Update the main content of the wrapper
                wrapper[1] = new_screen
                page.controls.clear()  # Clear previous controls
                page.add(Row(wrapper, alignment=alignment.center))
                page.update()

            except Exception as e:
                error_message = f"Error while changing to {screen_name} screen: {e}"
                print(error_message)
                traceback.print_exc()

                # Optional: Show an error message on the page
                wrapper[1] = Container(
                    content=Column(
                        controls=[
                            Text(
                                value=f"Unable to load the {screen_name} screen.",
                                color="red",
                                size=18,
                                weight="bold",
                            ),
                            Text(
                                value=str(e),
                                color="white54",
                                size=14,
                            ),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                    )
                )
                page.controls.clear()
                page.add(Row(wrapper, alignment=alignment.center))
                page.update()

        # Screen handlers
        def handle_home_screen(e):
            update_screen("HOME", HomeScreen().home_screen)

        def handle_comparison_screen(e):
            update_screen("COMPARISON", lambda: Difference(page).difference_panel())

        def handle_key_generation_screen(e):
            update_screen("GENERATEKEY", GenerateKey().generate_key)

        def handle_encryption_screen(e):
            update_screen("ENCRYPTION", lambda: Encryption(page).encryption())

        def handle_decryption_screen(e):
            update_screen("DECRYPTION", lambda: Decryption(page).decryption())

        # Sidebar content
        def user_data(initials: str, name: str, description: str) -> Container:
            return Container(
                content=Row(
                    controls=[
                        Container(
                            width=42,
                            height=42,
                            border_radius=8,
                            bgcolor="bluegrey900",
                            alignment=alignment.center,
                            content=Text(
                                value=initials,
                                size=20,
                                weight="bold",
                            ),
                        ),
                        Column(
                            spacing=1,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                Text(value=name, size=15, weight="bold"),
                                Text(value=description, size=13, weight="w400", color="white54"),
                            ],
                        ),
                    ]
                )
            )

        def contained_icon(icon_name: str, text: str) -> Container:
            return Container(
                width=180,
                height=45,
                border_radius=10,
                ink=True,
                content=Row(
                    controls=[
                        IconButton(
                            icon=icon_name,
                            icon_size=25,
                            icon_color="white54",
                            style=ButtonStyle(
                                shape={"": RoundedRectangleBorder(radius=7)},
                                overlay_color={"": "transparent"},
                            ),
                        ),
                        Text(value=text, color="white54", size=15),
                    ],
                ),
            )

        # Build the sidebar
        sidebar = Container(
            width=200,
            height=580,
            alignment=alignment.center,
            content=Column(
                alignment=MainAxisAlignment.START,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    user_data("IS", "IS", "Image Steganography"),
                    Divider(height=5, color="white24"),
                    *[
                        GestureDetector(
                            on_tap=handler,
                            content=contained_icon(icon, label)
                        )
                        for handler, icon, label in [
                            (handle_home_screen, icons.HOME_ROUNDED, "Home"),
                            (handle_key_generation_screen, icons.KEY_ROUNDED, "Generate Key"),
                            (handle_encryption_screen, icons.LOCK_ROUNDED, "Encryption"),
                            (handle_decryption_screen, icons.LOCK_OPEN_ROUNDED, "Decryption"),
                            (handle_comparison_screen, icons.CODE_ROUNDED, "Comparison"),
                        ]
                    ],
                    Divider(height=5, color="white24"),
                ],
            ),
        )

        wrapper[0].content = sidebar

        # Add content to page
        page.add(Row(wrapper, alignment=alignment.center))
        page.update()
