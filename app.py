# main.py

import flet as ft
from styles import button_style, text_heading_style, container_card_style, app_theme

def main(page: ft.Page):
    page.title = "Mi App con Estilos Separados"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Aplicar tema si lo definiste
    page.theme = app_theme()

    page.add(
        ft.Text(
            "¡Hola, Flet!",
            style=text_heading_style(), # Aplicando un estilo de texto
        ),
        ft.ElevatedButton(
            "Haz clic",
            style=button_style(),  # Aplicando un estilo de botón
            on_click=lambda e: print("Botón clickeado"),
        ),
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Contenido de la tarjeta", size=16),
                    ft.ElevatedButton("Más info"),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            **container_card_style(), # Usando el operador ** para desempaquetar el diccionario
        )
    )

if __name__ == "__main__":
    ft.app(target=main)