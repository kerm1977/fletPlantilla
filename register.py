# register.py
import flet as ft

from styles import (
    heading_large_style,
    heading_medium_style,
    body_text_style,
    caption_text_style,
    primary_button_style,
    text_button_style,
    text_input_style,
    page_background_style,
    PRIMARY_COLOR
)
from db import register_user

def RegisterView(page: ft.Page):
    """
    Define la vista (página) de registro con el formulario completo.
    """

    # --- Campos del formulario ---
    name_field = ft.TextField(
        label="Nombre",
        **text_input_style(),
        width=300,
        prefix_icon=ft.Icons.PERSON,
        autofocus=True,
        # REQUIRED REMOVED: Ya no se usa required=True/False aquí
    )
    lastname1_field = ft.TextField(
        label="Primer Apellido",
        **text_input_style(),
        width=300,
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        # REQUIRED REMOVED
    )
    lastname2_field = ft.TextField(
        label="Segundo Apellido (Opcional)",
        **text_input_style(),
        width=300,
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        # REQUIRED REMOVED: Ya no se usa required=True/False aquí
    )
    username_field = ft.TextField(
        label="Nombre de Usuario",
        **text_input_style(),
        width=300,
        prefix_icon=ft.Icons.ACCOUNT_CIRCLE,
        # REQUIRED REMOVED
    )
    phone_field = ft.TextField(
        label="Teléfono (Opcional)",
        **text_input_style(),
        width=300,
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]"), # Solo números
        max_length=15,
        prefix_icon=ft.Icons.PHONE,
        # REQUIRED REMOVED: Ya no se usa required=True/False aquí
    )
    email_field = ft.TextField(
        label="Email",
        **text_input_style(),
        width=300,
        keyboard_type=ft.KeyboardType.EMAIL,
        prefix_icon=ft.Icons.EMAIL,
        # REQUIRED REMOVED
    )
    password_field = ft.TextField(
        label="Contraseña",
        **text_input_style(),
        password=True,
        can_reveal_password=True,
        width=300,
        prefix_icon=ft.Icons.LOCK,
        # REQUIRED REMOVED
    )
    confirm_password_field = ft.TextField(
        label="Confirmar Contraseña",
        **text_input_style(),
        password=True,
        can_reveal_password=True,
        width=300,
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        # REQUIRED REMOVED
    )

    # --- Función para manejar el registro ---
    def on_register_button_click(e):
        # Limpiar mensajes de error previos en los campos
        name_field.error_text = None
        lastname1_field.error_text = None
        username_field.error_text = None
        email_field.error_text = None
        password_field.error_text = None
        confirm_password_field.error_text = None
        
        # Validaciones de campos obligatorios y formato
        errors = False
        if not name_field.value:
            name_field.error_text = "El nombre es obligatorio."
            errors = True
        if not lastname1_field.value:
            lastname1_field.error_text = "El primer apellido es obligatorio."
            errors = True
        if not username_field.value:
            username_field.error_text = "El nombre de usuario es obligatorio."
            errors = True
        if not email_field.value:
            email_field.error_text = "El email es obligatorio."
            errors = True
        elif "@" not in email_field.value or "." not in email_field.value:
            email_field.error_text = "Formato de email inválido."
            errors = True
        if not password_field.value:
            password_field.error_text = "La contraseña es obligatoria."
            errors = True
        if not confirm_password_field.value:
            confirm_password_field.error_text = "Confirmar contraseña es obligatorio."
            errors = True
        
        if password_field.value != confirm_password_field.value:
            password_field.error_text = "Las contraseñas no coinciden."
            confirm_password_field.error_text = "Las contraseñas no coinciden."
            errors = True
        
        # Actualizar la UI con los errores visuales antes de continuar
        page.update()

        if errors:
            page.snack_bar = ft.SnackBar(
                ft.Text("Por favor, corrige los errores en el formulario.", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
            )
            page.snack_bar.open = True
            page.update()
            return
        
        # Si no hay errores de validación de campos, procede a registrar
        result = register_user(
            name_field.value,
            lastname1_field.value,
            lastname2_field.value, # Pasa el valor, puede ser cadena vacía
            username_field.value,
            phone_field.value,     # Pasa el valor, puede ser cadena vacía
            email_field.value,
            password_field.value   # Pasa la contraseña en texto plano, la función register_user la hashea
        )

        if result is True:
            page.snack_bar = ft.SnackBar(
                ft.Text("Registro exitoso! Ya puedes iniciar sesión.", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN_700,
            )
            page.snack_bar.open = True
            page.update()
            page.go("/login") # Redirige al login después de un registro exitoso
        elif result == "email_exists":
            email_field.error_text = "Este email ya está registrado."
            page.snack_bar = ft.SnackBar(
                ft.Text("Error: El email ya está registrado.", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
            )
            page.snack_bar.open = True
            page.update()
        elif result == "username_exists":
            username_field.error_text = "Este nombre de usuario ya está en uso."
            page.snack_bar = ft.SnackBar(
                ft.Text("Error: El nombre de usuario ya existe.", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
            )
            page.snack_bar.open = True
            page.update()
        else: # Otros errores genéricos de DB
            page.snack_bar = ft.SnackBar(
                ft.Text("Error desconocido al registrar usuario. Inténtalo de nuevo.", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
            )
            page.snack_bar.open = True
            page.update()
        
        # Opcional: Limpiar campos del formulario después del intento de registro (si se desea)
        # name_field.value = ""
        # lastname1_field.value = ""
        # lastname2_field.value = ""
        # username_field.value = ""
        # phone_field.value = ""
        # email_field.value = ""
        # password_field.value = ""
        # confirm_password_field.value = ""
        # page.update()


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
                                "Registro de Usuario",
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
                    ft.Text("Crea tu cuenta", style=heading_large_style()),
                    ft.Text("Rellena el formulario para registrarte", style=body_text_style()),
                    ft.Divider(height=30),
                    # Usamos ResponsiveRow para mejor layout en diferentes tamaños de pantalla
                    ft.ResponsiveRow(
                        [
                            ft.Column([name_field], col={"sm": 12, "md": 6, "lg": 4}),
                            ft.Column([lastname1_field], col={"sm": 12, "md": 6, "lg": 4}),
                            ft.Column([lastname2_field], col={"sm": 12, "md": 6, "lg": 4}),
                            ft.Column([username_field], col={"sm": 12, "md": 6, "lg": 6}),
                            ft.Column([phone_field], col={"sm": 12, "md": 6, "lg": 6}),
                            ft.Column([email_field], col={"sm": 12, "md": 12, "lg": 12}), # Email a ancho completo
                            ft.Column([password_field], col={"sm": 12, "md": 6, "lg": 6}),
                            ft.Column([confirm_password_field], col={"sm": 12, "md": 6, "lg": 6}),
                        ],
                        spacing=15, # Espacio horizontal entre columnas
                        run_spacing=15, # Espacio vertical cuando las columnas saltan de línea
                        alignment=ft.MainAxisAlignment.CENTER # Centrar las columnas dentro de la fila
                    ),
                    ft.Divider(height=30),
                    ft.ElevatedButton(
                        "Registrarse",
                        style=primary_button_style(),
                        on_click=on_register_button_click,
                        width=300
                    ),
                    ft.TextButton(
                        content=ft.Text(
                            "¿Ya tienes una cuenta? Inicia sesión aquí.",
                            color=PRIMARY_COLOR,
                            size=14,
                        ),
                        on_click=on_back_to_login_click,
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
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )