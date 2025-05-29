# main.py (Este es el archivo que tú llamas app.py)

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
from db import init_db, find_user_by_username 

# --- ¡IMPORTAMOS LAS VISTAS! ---
from login import LoginView
from register import RegisterView
from profile import ProfileView # ¡NUEVA IMPORTACIÓN DE PROFILEVIEW!


def main(page: ft.Page):
    init_db() 

    page.title = "La Tribu App" 
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    page.theme = app_theme()
    page.bgcolor = page_background_style()["bgcolor"]

    page.logged_in_user = None 

    def logout(e):
        page.client_storage.remove("current_user_session_id")
        page.logged_in_user = None 
        page.snack_bar = ft.SnackBar(
            ft.Text("Sesión cerrada correctamente.", color=ft.Colors.WHITE),
            bgcolor=ft.Colors.GREEN_700,
        )
        page.snack_bar.open = True
        page.update()
        page.go("/login")

    def check_session_on_start():
        session_username = page.client_storage.get("current_user_session_id")
        if session_username:
            user_data = find_user_by_username(session_username)
            if user_data:
                page.logged_in_user = {
                    "username": user_data[3],
                    "id": user_data[0], 
                    "nombre": user_data[1]
                }
                print(f"DEBUG: Sesión restaurada para usuario: {page.logged_in_user['username']}")
                page.go("/")
            else:
                page.client_storage.remove("current_user_session_id")
                page.logged_in_user = None
                print("DEBUG: Sesión inválida detectada y eliminada.")
        else:
            print("DEBUG: No hay sesión persistente guardada.")
        
        route_change(page.route)


    def route_change(route):
        page.views.clear()
        
        home_appbar_actions = []
        home_content = []

        if page.logged_in_user:
            home_appbar_actions.append(
                ft.IconButton(
                    icon=ft.Icons.ACCOUNT_CIRCLE,
                    tooltip=f"Mi Perfil ({page.logged_in_user['nombre']})", 
                    icon_color=ft.Colors.WHITE,
                    on_click=lambda e: page.go("/profile") # ¡ESTE ES EL CAMBIO CLAVE EN EL ON_CLICK!
                )
            )
            home_appbar_actions.append(
                ft.IconButton(
                    icon=ft.Icons.LOGOUT,
                    tooltip="Cerrar Sesión",
                    icon_color=ft.Colors.WHITE,
                    on_click=logout,
                )
            )
            home_content.extend([
                ft.Text(f"¡Hola, {page.logged_in_user['nombre']}!", style=heading_large_style()),
                ft.Text("Estás logueado.", style=body_text_style()),
                ft.Text("Desde aquí puedes gestionar tu cuenta.", style=caption_text_style()),
            ])
        else:
            home_appbar_actions.append(
                ft.IconButton(
                    icon=ft.Icons.PERSON_OUTLINE,
                    tooltip="Iniciar Sesión",
                    icon_color=ft.Colors.WHITE,
                    on_click=lambda e: page.go("/login"),
                )
            )
            home_content.extend([
                ft.Text("¡Bienvenido a La Tribu!", style=heading_large_style()),
                ft.Text("Esta es la página de inicio.", style=body_text_style()),
                ft.Text("Desde aquí puedes iniciar sesión o registrarte.", style=caption_text_style()),
            ])
        
        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.AppBar(
                            bgcolor=PRIMARY_COLOR, 
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
                            actions=home_appbar_actions
                        ),
                        ft.Column(
                            home_content,
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
        elif page.route == "/login":
            page.views.append(LoginView(page))

        elif page.route == "/register":
            page.views.append(RegisterView(page))
        
        # ¡NUEVA RUTA para el perfil del usuario!
        elif page.route == "/profile":
            if page.logged_in_user: 
                page.views.append(ProfileView(page))
            else:
                page.go("/login") 
        
        page.update()

    def view_pop(view):
        page.views.pop()
        if page.views:
            top_view = page.views[-1]
            page.go(top_view.route)
        else:
            page.go("/")

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.add(ft.Text("Cargando...", visible=False)) 
    check_session_on_start()


if __name__ == "__main__":
    ft.app(target=main)