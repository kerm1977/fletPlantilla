# login.py
import flet as ft
import bcrypt

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

    # Checkbox para recordar nombre de usuario
    remember_me_checkbox = ft.Checkbox(
        label="Recordarme",
        value=False, # Estado inicial
        adaptive=True,
    )

    # Pre-carga del nombre de usuario y estado del checkbox al inicializar la vista
    # Esto asegura que el campo se rellene ANTES de que la vista sea completamente renderizada
    remembered_username = page.client_storage.get("remembered_username")
    if remembered_username:
        username_field.value = remembered_username
        remember_me_checkbox.value = True

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

        user_data = find_user_by_username(username)

        if user_data:
            stored_password_hash = user_data[2] # El hash de la contraseña está en user_data[2]
            
            try:
                # Comprobar la contraseña
                if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                    page.snack_bar = ft.SnackBar(
                        ft.Text("Inicio de sesión exitoso!", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.GREEN_700,
                    )
                    page.snack_bar.open = True
                    
                    # Nuevo: Guardar/Borrar nombre de usuario si "Recordarme" está marcado/desmarcado
                    if remember_me_checkbox.value:
                        page.client_storage.set("remembered_username", username)
                        # Nuevo: Guardar el nombre de usuario como indicador de sesión activa
                        page.client_storage.set("current_user_session_id", username) 
                        print(f"DEBUG: Sesión y nombre de usuario '{username}' guardados en client_storage.")
                    else:
                        page.client_storage.remove("remembered_username")
                        page.client_storage.remove("current_user_session_id") # Asegúrate de limpiar la sesión si desmarcan
                        print("DEBUG: Sesión y nombre de usuario eliminados de client_storage.")
                    
                    # Actualizar el estado global del usuario logueado en la página
                    # Asume user_data es (id, nombre, password_hash, username, email, telefono)
                    page.logged_in_user = {"username": user_data[3], "id": user_data[0], "nombre": user_data[1]}

                    page.update() # Actualizar la UI antes de la navegación
                    page.go("/") # Redirige a la página principal (Home)

                else:
                    page.snack_bar = ft.SnackBar(
                        ft.Text("Nombre de usuario o contraseña incorrectos.", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.RED_700,
                    )
                    page.snack_bar.open = True
                    page.update()
            except ValueError as ve:
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
                page.snack_bar.duration = 5000
                page.update()
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
                    ft.Container(
                        content=remember_me_checkbox,
                        width=300,
                        alignment=ft.alignment.center_left,
                    ),
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
                    # Para depuración
                    ft.Divider(height=30),
                    ft.Text("Usuarios en DB (Solo para prueba):", style=caption_text_style()),
                    ft.Column(
                        [
                            ft.Text(f"- {u[3]} ({u[4]})") 
                            for u in get_all_users()
                        ],
                        scroll=ft.ScrollMode.ADAPTIVE,
                        height=100,
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