# login.py
import flet as ft
import bcrypt # Necesario para verificar contraseñas hasheadas

from styles import (
    heading_large_style,
    heading_medium_style,
    body_text_style,
    caption_text_style,
    primary_button_style,
    text_button_style,
    text_input_style,
    page_background_style,
    PRIMARY_COLOR,
    ACCENT_COLOR
)

# Importamos las funciones de la base de datos necesarias para login
from db import find_user_by_username, get_all_users

def LoginView(page: ft.Page):
    """
    Define la vista (página) de inicio de sesión.
    """
    
    username_field = ft.TextField(
        label="Nombre de Usuario",
        **text_input_style(),
        width=300,
        prefix_icon=ft.Icons.PERSON,
    )

    password_field = ft.TextField(
        label="Contraseña",
        **text_input_style(),
        password=True,
        can_reveal_password=True,
        width=300,
        prefix_icon=ft.Icons.LOCK,
    )

    def on_login_button_click(e):
        username = username_field.value
        password = password_field.value

        if not username or not password:
            page.snack_bar = ft.SnackBar(
                ft.Text("Por favor, ingresa tu nombre de usuario y contraseña.", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
            )
            page.snack_bar.open = True
            page.update()
            return

        print(f"DEBUG: Intento de inicio de sesión con: Usuario='{username}', Contraseña='{password}'")

        user_data = find_user_by_username(username)
        print(f"DEBUG: Datos del usuario recuperados de DB: {user_data}")

        if user_data:
            # user_data es una tupla: (id, username, password_hash)
            stored_password_hash = user_data[2]
            print(f"DEBUG: Contraseña hasheada almacenada: {stored_password_hash}")
            
            # Verificar la contraseña usando bcrypt
            try:
                # bcrypt.checkpw toma bytes, por eso .encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                    print("DEBUG: ¡bcrypt.checkpw DEVOLVIÓ TRUE! Inicio de sesión exitoso.")
                    page.snack_bar = ft.SnackBar(
                        ft.Text("Inicio de sesión exitoso!", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.GREEN_700,
                    )
                    page.snack_bar.open = True
                    page.update()
                    
                    # --- ¡REDIRECCIÓN A LA PÁGINA HOME! ---
                    page.go("/") # Navega a la ruta raíz (home)
                    
                else:
                    print("DEBUG: ¡bcrypt.checkpw DEVOLVIÓ FALSE! Contraseña incorrecta.")
                    page.snack_bar = ft.SnackBar(
                        ft.Text("Nombre de usuario o contraseña incorrectos.", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.RED_700,
                    )
                    page.snack_bar.open = True
                    page.update()
            except ValueError as ve: # Esto puede ocurrir si el hash no es válido (ej. corrupto)
                 print(f"DEBUG: ERROR: ValueError en bcrypt.checkpw: {ve}")
                 page.snack_bar = ft.SnackBar(
                    ft.Text(f"Error de autenticación (hash inválido). Contacta al soporte.", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.RED_700,
                )
                 page.snack_bar.open = True
                 page.update()
            except Exception as ex:
                print(f"DEBUG: ERROR: Excepción inesperada durante la autenticación: {ex}")
                page.snack_bar = ft.SnackBar(
                    ft.Text("Ocurrió un error al intentar iniciar sesión. Inténtalo de nuevo.", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.RED_700,
                )
                page.snack_bar.open = True
                page.snack_bar.duration = 5000 # Para que el usuario tenga tiempo de leer
                page.update()
        else:
            print("DEBUG: Usuario no encontrado en la base de datos.")
            page.snack_bar = ft.SnackBar(
                ft.Text("Nombre de usuario o contraseña incorrectos.", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
            )
            page.snack_bar.open = True
            page.update()

    def on_register_link_click(e):
        page.go("/register")
        page.update()

    return ft.View(
        "/login", # Ruta para esta vista
        [
            ft.AppBar(
                bgcolor=ft.Colors.ORANGE_700,
                toolbar_height=50,
                elevation=2,
                leading=ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(
                                "Iniciar Sesión",
                                style=ft.TextStyle(
                                    size=18,
                                    weight=heading_medium_style().weight, # Usa .weight
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
                    ft.Text("Bienvenido", style=heading_large_style()),
                    ft.Text("Inicia sesión en tu cuenta", style=body_text_style()),
                    ft.Divider(height=30),
                    username_field,
                    password_field,
                    ft.ElevatedButton(
                        "Iniciar Sesión",
                        style=primary_button_style(),
                        on_click=on_login_button_click,
                        width=300
                    ),
                    ft.TextButton(
                        content=ft.Text(
                            "¿No tienes una cuenta? Regístrate aquí.",
                            color=ACCENT_COLOR,
                            size=14,
                        ),
                        on_click=on_register_link_click,
                    ),
                    ft.Divider(height=30),
                    ft.Text("Usuarios en DB (Solo para prueba):", style=caption_text_style()),
                    ft.Column(
                        [
                            # Muestra username y email de cada usuario
                            ft.Text(f"- {u[3]} ({u[4]})") 
                            for u in get_all_users()
                        ],
                        scroll=ft.ScrollMode.ADAPTIVE,
                        height=100, # Limita la altura de la lista para no desbordar
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.START,
                spacing=15,
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True,
            ),
        ],
        bgcolor=page_background_style()["bgcolor"],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )