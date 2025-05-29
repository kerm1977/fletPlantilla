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
from db import init_db # Importamos la función de inicialización de la DB

# --- ¡IMPORTAMOS LAS VISTAS! ---
from login import LoginView
from register import RegisterView


def main(page: ft.Page):
    init_db() # Aseguramos que la DB esté inicializada al inicio de la app

    page.title = "La Tribu App" # Título general de la ventana/tab
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    page.theme = app_theme()
    page.bgcolor = page_background_style()["bgcolor"]

    # --- Función para cambiar de vista basada en la ruta ---
    def route_change(route):
        page.views.clear() # Limpia las vistas actuales
        
        # Vista de inicio (Home) - Ruta: /
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
                                # Botón para ir al login desde el Home
                                ft.IconButton(
                                    icon=ft.Icons.LOGIN,
                                    tooltip="Ir a Iniciar Sesión",
                                    icon_color=ft.Colors.WHITE,
                                    on_click=lambda e: page.go("/login"),
                                ),
                            ]
                        ),
                        # Contenido de la página principal
                        ft.Column(
                            [
                                ft.Text("¡Bienvenido a La Tribu!", style=heading_large_style()),
                                ft.Text("Esta es la página de inicio. Te has logueado con éxito.", style=body_text_style()),
                                ft.Text("Aquí irá el contenido principal de tu aplicación.", style=caption_text_style()),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=15,
                            expand=True,
                        )
                    ],
                    bgcolor=page_background_style()["bgcolor"],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        # Vista de Login - Ruta: /login
        elif page.route == "/login":
            page.views.append(LoginView(page))

        # Vista de Registro - Ruta: /register
        elif page.route == "/register":
            page.views.append(RegisterView(page))

        page.update()

    # --- Función para manejar el cierre de vistas (navegación hacia atrás) ---
    def view_pop(view):
        page.views.pop() # Elimina la vista actual de la pila
        if page.views: # Asegura que hay vistas en la pila
            top_view = page.views[-1] # Obtiene la vista anterior
            page.go(top_view.route) # Navega a la ruta de la vista anterior
        else: # Si no hay más vistas, cierra la aplicación o va a una vista predeterminada
            page.go("/login") # Por ejemplo, si se cierra el home, vuelve al login


    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # Inicia la aplicación en la ruta de login por defecto
    page.go("/login")


if __name__ == "__main__":
    ft.app(target=main)