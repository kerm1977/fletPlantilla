# register.py
import flet as ft
from styles import (
    heading_large_style,
    heading_medium_style,
    body_text_style,
    caption_text_style, # Asegúrate de que esté importado para mensajes si se usan
    primary_button_style,
    text_button_style,
    text_input_style,
    page_background_style,
    PRIMARY_COLOR
)
from db import insert_user # Importamos la función para insertar usuarios

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
        autofocus=True, # Para que el primer campo tenga el foco al cargar
    )
    lastname1_field = ft.TextField(
        label="Primer Apellido",
        **text_input_style(),
        width=300,
        prefix_icon=ft.Icons.PERSON_OUTLINE,
    )
    lastname2_field = ft.TextField(
        label="Segundo Apellido",
        **text_input_style(),
        width=300,
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        # Este campo podría ser opcional si el usuario lo desea
    )
    username_field = ft.TextField(
        label="Nombre de Usuario",
        **text_input_style(),
        width=300,
        prefix_icon=ft.Icons.ACCOUNT_CIRCLE,
    )
    phone_field = ft.TextField(
        label="Teléfono",
        **text_input_style(),
        width=300,
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]"), # Solo números
        max_length=10, # Limitar longitud si se desea
        prefix_icon=ft.Icons.PHONE,
    )
    email_field = ft.TextField(
        label="Email",
        **text_input_style(),
        width=300,
        keyboard_type=ft.KeyboardType.EMAIL,
        prefix_icon=ft.Icons.EMAIL,
    )
    password_field = ft.TextField(
        label="Contraseña",
        **text_input_style(),
        password=True,
        can_reveal_password=True,
        width=300,
        prefix_icon=ft.Icons.LOCK,
    )
    confirm_password_field = ft.TextField(
        label="Confirmar Contraseña",
        **text_input_style(),
        password=True,
        can_reveal_password=True,
        width=300,
        prefix_icon=ft.Icons.LOCK_OUTLINE,
    )

    # --- Función para manejar el registro ---
    def on_register_button_click(e):
        # Reiniciar errores visuales
        name_field.error_text = None
        lastname1_field.error_text = None
        username_field.error_text = None
        email_field.error_text = None
        password_field.error_text = None
        confirm_password_field.error_text = None
        page.update()

        # Validación de campos vacíos (obligatorios)
        errors = False
        if not name_field.value:
            name_field.error_text = "El nombre es obligatorio"
            errors = True
        if not lastname1_field.value:
            lastname1_field.error_text = "El primer apellido es obligatorio"
            errors = True
        if not username_field.value:
            username_field.error_text = "El nombre de usuario es obligatorio"
            errors = True
        if not email_field.value:
            email_field.error_text = "El email es obligatorio"
            errors = True
        if not password_field.value:
            password_field.error_text = "La contraseña es obligatoria"
            errors = True
        if not confirm_password_field.value:
            confirm_password_field.error_text = "Confirmar contraseña es obligatorio"
            errors = True

        if errors:
            page.snack_bar = ft.SnackBar(
                ft.Text("Por favor, rellena todos los campos obligatorios.", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
            )
            page.snack_bar.open = True
            page.update()
            return

        # Validación de contraseñas
        if password_field.value != confirm_password_field.value:
            password_field.error_text = "Las contraseñas no coinciden"
            confirm_password_field.error_text = "Las contraseñas no coinciden"
            page.snack_bar = ft.SnackBar(
                ft.Text("Las contraseñas no coinciden. Por favor, inténtalo de nuevo.", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
            )
            page.snack_bar.open = True
            page.update()
            return
        
        # Validación básica de email (podrías usar regex más compleja)
        if "@" not in email_field.value or "." not in email_field.value:
            email_field.error_text = "Formato de email inválido"
            page.snack_bar = ft.SnackBar(
                ft.Text("Por favor, ingresa un email válido.", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
            )
            page.snack_bar.open = True
            page.update()
            return


        # --- Lógica para guardar en la base de datos ---
        # Por ahora, estamos guardando solo nombre y email en la tabla 'usuarios'.
        # Puedes expandir la tabla 'usuarios' en db.py para guardar todos estos campos.
        # Por ejemplo, puedes crear una tabla 'registros' con todos los campos.

        # Adaptación para la tabla 'usuarios' actual:
        # Aquí combinaremos nombre + apellido para el campo 'nombre' y usaremos 'email'.
        # Idealmente, deberías modificar db.py y la tabla 'usuarios' para
        # tener campos como 'nombre', 'apellido1', 'apellido2', 'username', 'telefono', etc.

        # Si decides expandir la tabla 'usuarios' o crear una nueva tabla 'registros':
        # En db.py, modifica init_db para crear la tabla con los campos necesarios.
        # Y crea una nueva función en db.py como register_new_user(nombre, apellido1, ..., password_hashed).

        # Usaremos la función insert_user actual para demostrar la conexión a la DB
        # Esto es solo un ejemplo, la tabla actual solo tiene 'nombre' y 'email'
        full_name = f"{name_field.value} {lastname1_field.value} {lastname2_field.value}".strip()
        
        # Hash de la contraseña antes de guardar (¡MUY IMPORTANTE PARA SEGURIDAD!)
        # Para simplificar, no lo haremos aquí, pero DEBES usar un hashing robusto (ej. bcrypt)
        # password_hashed = hash_password(password_field.value)
        
        success = insert_user(full_name, email_field.value) # Solo nombre y email por ahora en db.py

        if success:
            page.snack_bar = ft.SnackBar(
                ft.Text("Registro exitoso! Ya puedes iniciar sesión.", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN_700,
            )
            page.snack_bar.open = True
            page.update()
            page.go("/login") # Ir al login después del registro exitoso
        else:
            # Esto se manejaría si el email ya existe (IntegrityError en db.py)
            page.snack_bar = ft.SnackBar(
                ft.Text("Error al registrar. El email podría ya estar en uso.", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
            )
            page.snack_bar.open = True
            page.update()
        
        # Limpiar campos después de un intento (exitoso o fallido de envío)
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
                                "Registro de Usuario", # Título de la página de registro
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
                    # Agrupamos los campos para mejor presentación si la pantalla es ancha
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
                        spacing=15, # Espacio entre columnas/filas
                        run_spacing=15, # Espacio cuando los elementos saltan de línea
                    ),
                    ft.Divider(height=30),
                    ft.ElevatedButton(
                        "Registrarse",
                        style=primary_button_style(),
                        on_click=on_register_button_click,
                        width=300 # Ocupa el ancho completo si es una sola columna
                    ),
                    ft.TextButton(
                        content=ft.Text(
                            "¿Ya tienes una cuenta? Inicia sesión aquí.",
                            color=PRIMARY_COLOR, # Un color diferente para el enlace de regreso
                            size=14,
                        ),
                        on_click=on_back_to_login_click,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.START, # Empieza desde arriba para ver todos los campos
                spacing=15,
                scroll=ft.ScrollMode.ADAPTIVE, # Permite scroll si hay muchos campos
                expand=True,
            ),
        ],
        bgcolor=page_background_style()["bgcolor"],
        vertical_alignment=ft.MainAxisAlignment.START, # Alineación superior para el contenido
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )