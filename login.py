# login.py
import flet as ft
from styles import (
    heading_large_style,
    heading_medium_style, 
    body_text_style,
    caption_text_style, # <--- ¡ASEGÚRATE QUE ESTÉ AQUÍ!
    primary_button_style,
    text_button_style,
    text_input_style,
    page_background_style,
    PRIMARY_COLOR,
    ACCENT_COLOR
)

from db import connect_db, get_all_users

def LoginView(page: ft.Page):
    """
    Define la vista (página) de inicio de sesión.
    """
    
    # Campo de nombre de usuario
    username_field = ft.TextField(
        label="Nombre de Usuario",
        **text_input_style(),
        width=300,
        prefix_icon=ft.Icons.PERSON,
    )

    # Campo de contraseña
    password_field = ft.TextField(
        label="Contraseña",
        **text_input_style(),
        password=True,
        can_reveal_password=True,
        width=300,
        prefix_icon=ft.Icons.LOCK,
    )

    def on_login_button_click(e):
        print(f"Intento de inicio de sesión con: Usuario='{username_field.value}', Contraseña='{password_field.value}'")
        
        # Lógica de verificación en la base de datos (placeholder)
        if username_field.value == "admin" and password_field.value == "password":
            page.snack_bar = ft.SnackBar(
                ft.Text("Inicio de sesión exitoso!", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN_700,
            )
            page.snack_bar.open = True
            page.update()
            page.go("/")
        else:
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
        "/login",
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
                    # <--- Línea donde se usa caption_text_style()
                    ft.Text("Usuarios en DB (Solo para prueba):", style=caption_text_style()), 
                    ft.Column([ft.Text(f"- {u[1]} ({u[2]})") for u in get_all_users()]),
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