# register.py
import flet as ft
from styles import (
    heading_large_style,
    heading_medium_style, 
    body_text_style,
    caption_text_style, # <--- ¡ASEGÚRATE QUE ESTÉ AQUÍ!
    primary_button_style,
    text_button_style,
    page_background_style,
    PRIMARY_COLOR
)

def RegisterView(page: ft.Page):
    """
    Define la vista (página) de registro.
    """

    def on_back_to_login_click(e):
        page.go("/login")
        page.update()

    return ft.View(
        "/register",
        [
            ft.AppBar(
                bgcolor=ft.Colors.ORANGE_700,
                toolbar_height=50,
                elevation=2,
                leading=ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(
                                "Registro",
                                style=ft.TextStyle(
                                    size=18,
                                    weight=heading_medium_style().weight, 
                                    color=ft.Colors.WHITE,
                                ),
                                no_wrap=True,
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.only(left=20, right=5),
                    alignment=ft.alignment.center_left,
                ),
            ),
            ft.Column(
                [
                    ft.Text("Página de Registro", style=heading_large_style()),
                    ft.Text("Aquí irá tu formulario de registro.", style=body_text_style()),
                    ft.ElevatedButton(
                        "Volver al Login",
                        style=primary_button_style(),
                        on_click=on_back_to_login_click,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
        ],
        bgcolor=page_background_style()["bgcolor"],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )