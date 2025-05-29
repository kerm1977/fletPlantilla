# profile.py
import flet as ft
import time

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
from db import get_user_by_id, update_user, delete_user

def ProfileView(page: ft.Page):
    """
    Define la vista para mostrar y editar el perfil del usuario.
    """
    user_id = page.logged_in_user["id"]
    user_data = get_user_by_id(user_id)

    if not user_data:
        page.snack_bar = ft.SnackBar(
            ft.Text("Error al cargar el perfil. Por favor, inicia sesión de nuevo.", color=ft.Colors.WHITE),
            bgcolor=ft.Colors.RED_700,
        )
        page.snack_bar.open = True
        page.update()
        page.go("/login")
        return

    # Extraer los datos del usuario. Asumiendo que user_data tiene 8 elementos.
    current_id, current_name, current_lastname1, current_lastname2, \
    current_username, current_email, current_phone, current_password_hash = user_data

    # Campos de texto para mostrar/editar la información del usuario
    # Inicialmente, haremos los campos de solo lectura y el botón de editar los habilitará.
    name_field = ft.TextField(
        label="Nombre",
        **text_input_style(),
        value=current_name,
        width=300,
        prefix_icon=ft.Icons.PERSON,
        read_only=True, # Inicia como solo lectura
        on_change=lambda e: on_field_change(e),
    )
    lastname1_field = ft.TextField(
        label="Primer Apellido",
        **text_input_style(),
        value=current_lastname1,
        width=300,
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        read_only=True, # Inicia como solo lectura
        on_change=lambda e: on_field_change(e),
    )
    lastname2_field = ft.TextField(
        label="Segundo Apellido (Opcional)",
        **text_input_style(),
        value=current_lastname2,
        width=300,
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        read_only=True, # Inicia como solo lectura
        on_change=lambda e: on_field_change(e),
    )
    username_field = ft.TextField(
        label="Nombre de Usuario",
        **text_input_style(),
        value=current_username,
        width=300,
        prefix_icon=ft.Icons.ACCOUNT_CIRCLE,
        read_only=True, # Inicia como solo lectura
        on_change=lambda e: on_field_change(e),
    )
    email_field = ft.TextField(
        label="Email",
        **text_input_style(),
        value=current_email,
        width=300,
        prefix_icon=ft.Icons.EMAIL,
        keyboard_type=ft.KeyboardType.EMAIL,
        read_only=True, # Inicia como solo lectura
        on_change=lambda e: on_field_change(e),
    )
    phone_field = ft.TextField(
        label="Teléfono (Opcional)",
        **text_input_style(),
        value=current_phone,
        width=300,
        prefix_icon=ft.Icons.PHONE,
        keyboard_type=ft.KeyboardType.PHONE,
        read_only=True, # Inicia como solo lectura
        on_change=lambda e: on_field_change(e),
    )

    save_button = ft.ElevatedButton(
        "Guardar Cambios",
        style=primary_button_style(),
        on_click=None, # Se asignará más abajo
        visible=False, # Inicia oculto, se muestra al editar
        disabled=True, # Deshabilitado hasta que haya cambios al editar
    )

    cancel_button = ft.OutlinedButton(
        "Cancelar",
        style=text_button_style(),
        on_click=None, # Se asignará más abajo
        visible=False, # Inicia oculto, se muestra al editar
        disabled=True, # Deshabilitado hasta que haya cambios al editar
    )

    # Definir los botones aquí para poder referenciarlos en toggle_edit_mode
    edit_button = ft.IconButton(
        icon=ft.Icons.EDIT,
        tooltip="Editar Perfil",
        on_click=None, # Se asignará más abajo
        icon_color=ft.Colors.WHITE
    )

    delete_button = ft.IconButton(
        icon=ft.Icons.DELETE,
        tooltip="Eliminar Cuenta",
        on_click=None, # Se asignará más abajo
        icon_color=ft.Colors.RED_300
    )

    # --- Funciones de Eventos (Definidas ANTES de que se creen los controles que las usan) ---

    def toggle_edit_mode(enable: bool):
        # Habilita o deshabilita los campos de texto
        name_field.read_only = not enable
        lastname1_field.read_only = not enable
        lastname2_field.read_only = not enable
        username_field.read_only = not enable
        email_field.read_only = not enable
        phone_field.read_only = not enable

        # Muestra/oculta los botones de guardar/cancelar
        save_button.visible = enable
        cancel_button.visible = enable
        
        # Oculta el botón de editar cuando se está editando
        edit_button.visible = not enable
        
        # Asegúrate de que los botones de guardar/cancelar estén deshabilitados al iniciar el modo edición
        # o cuando se sale de él (si no hay cambios)
        save_button.disabled = not enable 
        cancel_button.disabled = not enable

        page.update()
        
        # Si se está habilitando el modo edición, enfoca el primer campo
        if enable:
            name_field.focus()


    def on_field_change(e):
        # Esta función ahora solo necesita habilitar/deshabilitar los botones si están visibles
        if save_button.visible: # Solo chequea si están visibles (i.e., en modo edición)
            has_changes = False
            if (name_field.value != current_name or
                lastname1_field.value != current_lastname1 or
                lastname2_field.value != current_lastname2 or
                username_field.value != current_username or
                email_field.value != current_email or
                phone_field.value != current_phone):
                has_changes = True

            save_button.disabled = not has_changes
            cancel_button.disabled = not has_changes
            page.update()

    def on_save_button_click(e):
        # Validaciones
        if not name_field.value:
            page.snack_bar = ft.SnackBar(
                ft.Text("El nombre es obligatorio.", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
            )
            page.snack_bar.open = True
            page.update()
            return

        if not lastname1_field.value:
            page.snack_bar = ft.SnackBar(
                ft.Text("El primer apellido es obligatorio.", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
            )
            page.snack_bar.open = True
            page.update()
            return

        if not username_field.value:
            page.snack_bar = ft.SnackBar(
                ft.Text("El nombre de usuario es obligatorio.", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
            )
            page.snack_bar.open = True
            page.update()
            return

        if not email_field.value:
            page.snack_bar = ft.SnackBar(
                ft.Text("El email es obligatorio.", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
            )
            page.snack_bar.open = True
            page.update()
            return

        # Validación de formato de email
        import re
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email_field.value):
            page.snack_bar = ft.SnackBar(
                ft.Text("Formato de email inválido.", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
            )
            page.snack_bar.open = True
            page.update()
            return

        # Validación de formato de teléfono (solo números, mínimo 8 dígitos si está presente)
        if phone_field.value:
            if not re.match(r"^[0-9]{8,}$", phone_field.value):
                page.snack_bar = ft.SnackBar(
                    ft.Text("Formato de teléfono inválido (solo números, mínimo 8 dígitos).", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.RED_700,
                )
                page.snack_bar.open = True
                page.update()
                return

        updated_success = update_user(
            user_id,
            name_field.value,
            lastname1_field.value,
            lastname2_field.value,
            username_field.value,
            email_field.value,
            phone_field.value,
        )

        if updated_success:
            # Actualizar los datos originales para que on_field_change funcione correctamente
            nonlocal current_name, current_lastname1, current_lastname2, current_username, current_email, current_phone
            current_name = name_field.value
            current_lastname1 = lastname1_field.value
            current_lastname2 = lastname2_field.value
            current_username = username_field.value
            current_email = email_field.value
            current_phone = phone_field.value

            page.snack_bar = ft.SnackBar(
                ft.Text("¡Perfil actualizado con éxito!", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN_700,
            )
            page.snack_bar.open = True 

            # Actualizar el nombre de usuario en la barra de navegación si existe
            if page.logged_in_user:
                page.logged_in_user["username"] = username_field.value

            # Volver a modo de solo lectura y ocultar botones de guardar/cancelar
            toggle_edit_mode(False) # Deshabilita el modo edición
            
            # Redirigir al home (como lo solicitaste previamente)
            page.views.clear()
            page.go("/")
            page.update() # Importante actualizar la página después de go()

        else:
            page.snack_bar = ft.SnackBar(
                ft.Text("Error al actualizar el perfil. El nombre de usuario o email podrían estar en uso.", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
            )
            page.snack_bar.open = True
            page.update()

    def on_cancel_button_click(e):
        # Restablecer los campos a los valores originales
        name_field.value = current_name
        lastname1_field.value = current_lastname1
        lastname2_field.value = current_lastname2
        username_field.value = current_username
        email_field.value = current_email
        phone_field.value = current_phone

        # Deshabilitar botones y volver a modo de solo lectura
        toggle_edit_mode(False)
        page.update()


    # --- Diálogo de Confirmación de Eliminación ---
    def delete_confirmation_dialog_result(e: ft.ControlEvent):
        page.dialog.open = False
        if e.control.text == "Sí, eliminar":
            perform_delete_action()
        page.update()

    def perform_delete_action():
        """Función para ejecutar la eliminación real si se confirma."""
        if delete_user(user_id):
            page.snack_bar = ft.SnackBar(
                ft.Text("¡Cuenta eliminada con éxito! Redirigiendo...", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN_700,
            )
            page.snack_bar.open = True
            page.update()
            # Cerrar sesión y redirigir al inicio
            page.go("/")
            page.logged_in_user = None # Limpiar la sesión localmente
            page.update()
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text("Error al eliminar la cuenta. Inténtalo de nuevo.", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
            )
            page.snack_bar.open = True
            page.update()

    def on_delete_account_click(e):
        # Crear el diálogo de confirmación
        print("Botón de eliminar clickeado, mostrando diálogo.") # Para depuración
        page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Eliminación de Cuenta"),
            content=ft.Text("¿Estás seguro de que quieres eliminar tu cuenta? Esta acción es irreversible."),
            actions=[
                ft.TextButton("Sí, eliminar", on_click=delete_confirmation_dialog_result, style=ft.ButtonStyle(color=ft.Colors.RED_700)),
                ft.ElevatedButton("Cancelar", on_click=delete_confirmation_dialog_result),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog.open = True
        page.update()

    # --- Asignar on_click a los botones después de que todas las funciones estén definidas ---
    save_button.on_click = on_save_button_click
    cancel_button.on_click = on_cancel_button_click
    edit_button.on_click = lambda e: toggle_edit_mode(True) # Ahora la función existe
    delete_button.on_click = on_delete_account_click # Ahora la función existe

    return ft.View(
        "/profile",
        [
            ft.AppBar(
                title=ft.Text("Mi Perfil", style=heading_medium_style()),
                bgcolor=PRIMARY_COLOR,
                actions=[
                    edit_button,   # Botón de editar (ya creado con su on_click)
                    delete_button, # Botón de eliminar (ya creado con su on_click)
                ],
            ),
            ft.Column(
                [
                    ft.Text("Tu información de perfil", style=body_text_style()),
                    ft.ResponsiveRow(
                        [
                            ft.Column([name_field], col={"sm": 12, "md": 6, "lg": 4}),
                            ft.Column([lastname1_field], col={"sm": 12, "md": 6, "lg": 4}),
                            ft.Column([lastname2_field], col={"sm": 12, "md": 6, "lg": 4}),
                            ft.Column([username_field], col={"sm": 12, "md": 6, "lg": 6}),
                            ft.Column([email_field], col={"sm": 12, "md": 6, "lg": 6}),
                            ft.Column([phone_field], col={"sm": 12, "md": 12, "lg": 12}),
                        ],
                        spacing=15,
                        run_spacing=15,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Divider(height=30),
                    ft.Row(
                        [save_button, cancel_button],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
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