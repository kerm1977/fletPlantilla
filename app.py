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
from db import init_db, find_user_by_username # Importamos find_user_by_username para verificar la sesión

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

    # Variable para almacenar el usuario actualmente logueado (puedes almacenar el objeto completo del usuario)
    page.logged_in_user = None # Inicialmente no hay usuario logueado

    # --- Función para cerrar sesión ---
    def logout(e):
        page.client_storage.remove("current_user_session_id") # Elimina el ID de sesión del almacenamiento
        page.logged_in_user = None # Limpia la variable de usuario logueado
        page.snack_bar = ft.SnackBar(
            ft.Text("Sesión cerrada correctamente.", color=ft.Colors.WHITE),
            bgcolor=ft.Colors.GREEN_700,
        )
        page.snack_bar.open = True
        page.update()
        page.go("/login") # Redirige al login

    # --- Función para verificar la sesión al inicio ---
    def check_session_on_start():
        session_username = page.client_storage.get("current_user_session_id")
        if session_username:
            user_data = find_user_by_username(session_username)
            if user_data:
                # Asume user_data es (id, nombre, password_hash, username, email, telefono)
                # Almacena el nombre de usuario para simplificar, o el ID, o un objeto User
                page.logged_in_user = {"username": user_data[3], "id": user_data[0], "nombre": user_data[1]}
                print(f"DEBUG: Sesión restaurada para usuario: {page.logged_in_user['username']}")
                page.go("/") # Ir a Home si hay sesión activa
            else:
                # Usuario no encontrado en DB, limpiar sesión inválida
                page.client_storage.remove("current_user_session_id")
                page.logged_in_user = None
                print("DEBUG: Sesión inválida detectada y eliminada.")
        else:
            print("DEBUG: No hay sesión persistente guardada.")
        
        # Después de verificar la sesión, procesa la ruta inicial
        route_change(page.route)


    # --- Función para cambiar de vista basada en la ruta ---
    def route_change(route):
        page.views.clear() # Limpia las vistas actuales
        
        # Definición de la vista HOME (pública o logueado)
        home_appbar_actions = []
        home_content = []

        if page.logged_in_user:
            # Si hay usuario logueado, mostrar "Mi Perfil" y "Cerrar Sesión"
            home_appbar_actions.append(
                ft.IconButton(
                    icon=ft.Icons.ACCOUNT_CIRCLE,
                    tooltip=f"Bienvenido, {page.logged_in_user['nombre']}",
                    icon_color=ft.Colors.WHITE,
                    on_click=lambda e: print("DEBUG: Ir a Perfil (no implementado aún)") # Implementar vista de perfil
                )
            )
            home_appbar_actions.append(
                ft.IconButton(
                    icon=ft.Icons.LOGOUT,
                    tooltip="Cerrar Sesión",
                    icon_color=ft.Colors.WHITE,
                    on_click=logout, # Llama a la función de cerrar sesión
                )
            )
            home_content.extend([
                ft.Text(f"¡Hola, {page.logged_in_user['nombre']}!", style=heading_large_style()),
                ft.Text("Estás logueado.", style=body_text_style()),
                ft.Text("Desde aquí puedes gestionar tu cuenta.", style=caption_text_style()),
            ])
        else:
            # Si no hay usuario logueado, mostrar botón de "Iniciar Sesión"
            home_appbar_actions.append(
                ft.IconButton(
                    icon=ft.Icons.PERSON_OUTLINE, # O usa ft.Icons.ACCOUNT_CIRCLE, ft.Icons.LOGIN
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
        
        # Vista Home (ruta "/")
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
                            actions=home_appbar_actions # Acciones dinámicas
                        ),
                        # Contenido de la página principal (dinámico)
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
            page.go("/") # Si se cierra el login, vuelve al home

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # Llamar a la función para verificar la sesión al inicio de la aplicación
    # Esta es la primera acción que toma la aplicación en cuanto se carga la página.
    page.add(ft.Text("Cargando...", visible=False)) # Pequeño truco para que page.client_storage esté listo
    check_session_on_start()


if __name__ == "__main__":
    ft.app(target=main)