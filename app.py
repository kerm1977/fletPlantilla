# main.py

import flet as ft
from styles import (
    app_theme,
    page_background_style,
    heading_large_style,
    heading_medium_style,
    body_text_style,
    caption_text_style,
    primary_button_style,
    outline_button_style,
    text_button_style,
    card_container_style,
    text_input_style,
    image_card_container_style,
    ACCENT_COLOR,
    PRIMARY_COLOR
)
# --- ¡CAMBIO AQUÍ! Importamos la función de inicialización de la DB ---
from db import init_db

def main(page: ft.Page):
    # --- ¡CAMBIO AQUÍ! Llamamos a init_db al inicio ---
    init_db() 
    # ^^^ Esto asegurará que la base de datos y la tabla 'usuarios' se creen si no existen.
    # Se ejecutará cada vez que inicie la aplicación, pero solo creará la tabla si no está.

    page.title = "App Móvil Vistosa con Flet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    page.theme = app_theme()
    page.update()
    
    page.bgcolor = page_background_style()["bgcolor"]

    page.appbar = ft.AppBar(
        bgcolor=ft.Colors.ORANGE_700,
        toolbar_height=50,
        elevation=2,
        
        leading=ft.Container(
            content=ft.Row(
                [
                    ft.Text(
                        "La Tribu",
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
        actions=[
            # Contenido de la derecha (actualmente vacío)
        ]
    )

    page.add(
        ft.Column(
            [
                # Contenido de la página (actualmente vacío)
                ft.Text("La base de datos está conectada y lista.", style=body_text_style()),
                ft.Text("Verifica la consola para mensajes de DB.", style=caption_text_style()),
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    )

    page.update()

if __name__ == "__main__":
    ft.app(target=main)