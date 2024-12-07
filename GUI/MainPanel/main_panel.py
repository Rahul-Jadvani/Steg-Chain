from flet import *
import time
from typing import Optional, Callable
from GUI.Screens import HomeScreen, GenerateKey, Encryption, Decryption, Difference

class MainPanel:
    def __init__(self):
        self.current_page: str = "HOME"

    def main(self, page: Page):
        # Configure page settings
        page.title = "Image Steganography"
        page.horizontal_alignment = "center"
        page.vertical_alignment = "center"

        # Screen handling methods
        def handle_screen_change(screen_name: str, screen_generator: Callable):
            """
            Generic screen change handler with error handling
            """
            try:
                self.current_page = screen_name
                wrapper[1] = screen_generator()
                page.update()
            except Exception as e:
                print(f"Error changing to {screen_name} screen: {e}")

        # Specific screen handlers using generic method
        def handle_home_screen(e):
            handle_screen_change("HOME", HomeScreen().home_screen)

        def handle_comparison_screen(e):
            handle_screen_change("COMPARISON", lambda: Difference(page).difference_panel())

        def handle_key_generation_screen(e):
            handle_screen_change("GENERATEKEY", GenerateKey().generate_key)

        def handle_encryption_screen(e):
            handle_screen_change("ENCRYPTION", lambda: Encryption(page).encryption())

        def handle_decryption_screen(e):
            handle_screen_change("DECRYPTION", lambda: Decryption(page).decryption())

        # User data display method with type hints and improved docstring
        def user_data(self, initials: str, name: str, description: str) -> Container:
            """
            Create a user data container with initials, name, and description
            
            Args:
                initials (str): Short user/app identifier
                name (str): Main display name
                description (str): Subtitle or brief description
            
            Returns:
                Container: Styled user data display
            """
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
                                Text(
                                    value=name,
                                    size=15,
                                    weight="bold",
                                ),
                                Text(
                                    value=description,
                                    size=13,
                                    weight="w400",
                                    color="white54",
                                ),
                            ],
                        ),
                    ]
                )
            )

        # Improved contained icon method with type hints
        def contained_icon(self, icon_name: str, text: str) -> Container:
            """
            Create a container with an icon and text
            
            Args:
                icon_name (str): Name of the icon
                text (str): Text to display next to icon
            
            Returns:
                Container: Styled icon and text container
            """
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
                                shape={
                                    "": RoundedRectangleBorder(radius=7),
                                },
                                overlay_color={"": "transparent"},
                            ),
                        ),
                        Text(
                            value=text,
                            color="white54",
                            size=15,
                        ),
                    ],
                ),
            )

        # Navigation sidebar
        build = Container(
            width=200,
            height=580,
            alignment=alignment.center,
            content=Column(
                alignment=MainAxisAlignment.START,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    user_data(self, "IS", "IS", "Image Steganography"),
                    Divider(height=5, color="white24"),
                    
                    # Consolidated navigation items
                    *[
                        GestureDetector(
                            on_tap=handler,
                            content=contained_icon(self, icon, label)
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

        # Wrapper for sidebar and main content
        wrapper = [
            Container(
                width=200,
                height=580,
                animate=animation.Animation(500, "decelerate"),
                border_radius=10,
                padding=10,
                content=build,
            ),
            HomeScreen().home_screen(),
        ]

        # Navbar animation with improved structure
        def animated_navBar(e):
            """
            Animate navigation bar expansion/collapse
            """
            navbar = page.controls[0]
            is_expanded = navbar.width != 62

            if not is_expanded:
                # Collapse logic
                _collapse_navbar(navbar)
            else:
                # Expand logic
                _expand_navbar(navbar)

        def _collapse_navbar(navbar):
            """Helper to collapse navbar"""
            for item in navbar.content.controls[0].content.controls[0].content.controls[1].controls[:]:
                item.opacity = 0
                item.update()

            for item in navbar.content.controls[0].content.controls[3:]:
                if isinstance(item, Container):
                    item.content.controls[1].opacity = 0
                    item.content.update()

            time.sleep(0.2)
            navbar.width = 62
            navbar.update()

        def _expand_navbar(navbar):
            """Helper to expand navbar"""
            navbar.width = 200
            navbar.update()

            time.sleep(0.2)

            for item in navbar.content.controls[0].content.controls[0].content.controls[1].controls[:]:
                item.opacity = 1
                item.update()

            for item in navbar.content.controls[0].content.controls[3:]:
                if isinstance(item, Container):
                    item.content.controls[1].opacity = 1
                    item.content.update()

        # Add content to page
        page.add(
            Row(wrapper, alignment=alignment.center),
        )
        page.update()