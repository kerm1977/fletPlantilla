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

# --- ¡NUEVAS IMPORTACIONES DE VISTAS (asegúrate de que login.py y register.py existan)! ---
from login import LoginView
from register import RegisterView # Asegúrate de tener este archivo aunque sea un placeholder


def main(page: ft.Page):
    # --- ¡CAMBIO AQUÍ! Llamamos a init_db al inicio ---
    init_db()
    # ^^^ Esto asegurará que la base de datos y la tabla 'usuarios' se creen si no existen.
    # Se ejecutará cada vez que inicie la aplicación, pero solo creará la tabla si no está.

    page.title = "La Tribu App" # Título general de la ventana/tab
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    page.theme = app_theme()
    # page.update() # No es necesario aquí si se llama al final o en route_change
    
    page.bgcolor = page_background_style()["bgcolor"]

    # --- Función para manejar el cambio de rutas ---
    def route_change(route):
        page.views.clear() # Limpia la pila de vistas

        # Vista de inicio (Home)
        if page.route == "/":
            page.views.append(
                ft.View(
                    "/", # La ruta de esta vista
                    [
                        ft.AppBar(
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
                                # --- ¡CAMBIO AQUÍ! Botón para ir al login ---
                                ft.IconButton(
                                    icon=ft.Icons.LOGIN,
                                    tooltip="Ir a Iniciar Sesión",
                                    icon_color=ft.Colors.WHITE,
                                    on_click=lambda e: page.go("/login"), # Navega a la ruta /login
                                ),
                            ]
                        ),
                        # Contenido de la página de inicio
                        ft.Column(
                            [
                                ft.Text("¡Bienvenido a La Tribu!", style=heading_large_style()),
                                ft.Text("Esta es la página de inicio.", style=body_text_style()),
                                ft.Text("Presiona el icono de login en la AppBar para ir a Iniciar Sesión.", style=caption_text_style()),
                            ],
                            scroll=ft.ScrollMode.ADAPTIVE,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                            expand=True
                        )
                    ],
                    bgcolor=page_background_style()["bgcolor"],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        # Vista de Login
        elif page.route == "/login":
            page.views.append(LoginView(page)) # Llama a la función LoginView de login.py

        # Vista de Registro
        elif page.route == "/register":
            page.views.append(RegisterView(page)) # Llama a la función RegisterView de register.py

        page.update() # Muy importante para que los cambios se vean

    # --- Función para manejar el cierre de vistas (navegación hacia atrás) ---
    def view_pop(view):
        page.views.pop() # Elimina la vista actual de la pila
        top_view = page.views[-1] # Obtiene la vista anterior
        page.go(top_view.route) # Navega a la ruta de la vista anterior

    page.on_route_change = route_change
    page.on_view_pop = view_pop # Asigna la función para manejar el pop de vistas

    # Inicia la aplicación en la ruta raíz (Home)
    page.go("/")


if __name__ == "__main__":
    ft.app(target=main)