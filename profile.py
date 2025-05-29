# profile.py
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

    current_id, current_name, current_lastname1, current_lastname2, \
    current_username, current_email, current_phone, current_password_hash = user_data

    # Campos de texto para mostrar/editar la información del usuario
    name_field = ft.TextField(
        label="Nombre",
        value=current_name,
        **text_input_style(),
        read_only=True, 
    )
    lastname1_field = ft.TextField(
        label="Primer Apellido",
        value=current_lastname1,
        **text_input_style(),
        read_only=True,
    )
    lastname2_field = ft.TextField(
        label="Segundo Apellido",
        value=current_lastname2,
        **text_input_style(),
        read_only=True,
    )
    username_field = ft.TextField(
        label="Nombre de Usuario",
        value=current_username,
        **text_input_style(),
        read_only=True,
    )
    email_field = ft.TextField(
        label="Email",
        value=current_email,
        **text_input_style(),
        read_only=True,
    )
    phone_field = ft.TextField(
        label="Teléfono",
        value=current_phone,
        **text_input_style(),
        read_only=True,
    )

    # Botones de acción en la vista (estos son los que estarán en la parte inferior de la vista)
    save_button = ft.ElevatedButton(
        "Guardar Cambios",
        style=primary_button_style(),
        on_click=None, 
        visible=False, 
    )
    cancel_button = ft.OutlinedButton(
        "Cancelar",
        on_click=None, 
        visible=False, 
    )

    # Definir los botones que irán en el AppBar
    back_button_appbar = ft.IconButton( 
        icon=ft.Icons.ARROW_BACK,
        tooltip="Volver",
        icon_color=ft.Colors.WHITE,
        on_click=lambda e: page.go("/"), 
        visible=True,
    )

    edit_button_appbar = ft.IconButton(
        icon=ft.Icons.EDIT,
        tooltip="Editar Perfil",
        icon_color=ft.Colors.WHITE,
        on_click=None, 
        visible=True, 
    )
    delete_button_appbar = ft.IconButton(
        icon=ft.Icons.DELETE,
        tooltip="Eliminar Cuenta",
        icon_color=ft.Colors.RED_200, 
        on_click=None, 
        visible=True, 
    )
    save_button_appbar = ft.IconButton(
        icon=ft.Icons.SAVE,
        tooltip="Guardar Cambios",
        icon_color=ft.Colors.WHITE,
        on_click=None, 
        visible=False, 
    )
    cancel_button_appbar = ft.IconButton(
        icon=ft.Icons.CANCEL,
        tooltip="Cancelar Edición",
        icon_color=ft.Colors.WHITE,
        on_click=None, 
        visible=False, 
    )

    # Crear el AppBar de la vista de perfil
    profile_appbar = ft.AppBar(
        bgcolor=PRIMARY_COLOR,
        toolbar_height=50,
        elevation=2,
        leading=ft.Container(
            content=ft.Row(
                [
                    ft.Text(
                        "Mi Perfil",
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
            back_button_appbar, 
            edit_button_appbar,
            delete_button_appbar,
            save_button_appbar, 
            cancel_button_appbar, 
        ]
    )

    # Funciones de Editar/Guardar/Cancelar/Eliminar
    def toggle_edit_mode(e):
        print("DEBUG: Entrando a toggle_edit_mode")
        is_editing = not name_field.read_only 
        
        name_field.read_only = is_editing
        lastname1_field.read_only = is_editing
        lastname2_field.read_only = is_editing
        username_field.read_only = is_editing 
        email_field.read_only = is_editing
        phone_field.read_only = is_editing

        save_button.visible = not is_editing 
        cancel_button.visible = not is_editing 
        
        edit_button_appbar.visible = is_editing 
        delete_button_appbar.visible = is_editing 
        back_button_appbar.visible = is_editing 
        save_button_appbar.visible = not is_editing 
        cancel_button_appbar.visible = not is_editing 

        page.update() 
        print(f"DEBUG: Modo edición: {not name_field.read_only}")

    def on_save_changes(e):
        print("DEBUG: Botón 'Guardar Cambios' clickeado.")
        print(f"DEBUG: Valores actuales de los campos: "
              f"Nombre={name_field.value}, "
              f"Apellido1={lastname1_field.value}, "
              f"Apellido2={lastname2_field.value}, "
              f"Username={username_field.value}, "
              f"Email={email_field.value}, "
              f"Teléfono={phone_field.value}")

        if not name_field.value or not lastname1_field.value or not username_field.value or not email_field.value:
            print("DEBUG: Falló la validación: Campos obligatorios vacíos.")
            page.snack_bar = ft.SnackBar(
                ft.Text("Nombre, primer apellido, nombre de usuario y email son obligatorios.", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
            )
            page.snack_bar.open = True
            page.update()
            return
        
        if "@" not in email_field.value or "." not in email_field.value:
            print("DEBUG: Falló la validación: Formato de email inválido.")
            page.snack_bar = ft.SnackBar(
                ft.Text("Formato de email inválido.", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
            )
            page.snack_bar.open = True
            page.update()
            return

        print("DEBUG: Validaciones pasadas. Intentando actualizar el usuario en la DB.")
        updated = update_user(
            user_id,
            name_field.value,
            lastname1_field.value,
            lastname2_field.value,
            username_field.value, 
            email_field.value,
            phone_field.value,
        )

        if updated:
            print("DEBUG: Usuario actualizado exitosamente en la DB.")
            # Actualizar la sesión guardada con el nuevo username/nombre si es necesario
            page.logged_in_user["username"] = username_field.value
            page.logged_in_user["nombre"] = name_field.value
            
            page.snack_bar = ft.SnackBar(
                ft.Text("Información actualizada exitosamente!", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN_700,
            )
            page.snack_bar.open = True
            page.update() # Asegurarse de que el SnackBar se muestre
            
            # --- ¡CAMBIO CLAVE AQUÍ: DOBLE REDIRECCIÓN PARA FORZAR LA RECARGA! ---
            print("DEBUG: Realizando doble redirección para forzar la recarga de la vista.")
            # Ir al home y luego inmediatamente al perfil
            page.go("/") 
            page.go("/profile")
            
        else:
            print("DEBUG: Falló la actualización del usuario en la DB (posiblemente username/email duplicado).")
            page.snack_bar = ft.SnackBar(
                ft.Text("Error al actualizar la información. El nombre de usuario o email podrían ya existir.", color=ft.Colors.RED_700),
                bgcolor=ft.Colors.RED_700,
            )
        page.snack_bar.open = True
        page.update()
        print("DEBUG: Finalizando on_save_changes.")


    def on_cancel_edit(e):
        print("DEBUG: Botón 'Cancelar' clickeado.")
        user_data_reloaded = get_user_by_id(user_id)
        if user_data_reloaded:
            name_field.value = user_data_reloaded[1]
            lastname1_field.value = user_data_reloaded[2]
            lastname2_field.value = user_data_reloaded[3]
            username_field.value = user_data_reloaded[4]
            email_field.value = user_data_reloaded[5]
            phone_field.value = user_data_reloaded[6]
        
        toggle_edit_mode(None) 
        page.update()
        print("DEBUG: on_cancel_edit finalizado.")

    def on_delete_user(e):
        print("DEBUG: Botón 'Eliminar Cuenta' clickeado.")
        def confirm_delete(e):
            print(f"DEBUG: Confirmación de eliminación: {e.control.text}")
            if e.control.text == "Sí":
                deleted = delete_user(user_id)
                if deleted:
                    print("DEBUG: Cuenta eliminada exitosamente.")
                    page.client_storage.remove("current_user_session_id")
                    page.logged_in_user = None
                    page.snack_bar = ft.SnackBar(
                        ft.Text("Tu cuenta ha sido eliminada.", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.GREEN_700,
                    )
                    page.snack_bar.open = True
                    page.update()
                    page.go("/login") 
                else:
                    print("DEBUG: Error al eliminar la cuenta.")
                    page.snack_bar = ft.SnackBar(
                        ft.Text("Error al eliminar la cuenta.", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.RED_700,
                    )
                    page.snack_bar.open = True
                    page.update()
            page.close_dialog() 

        page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Eliminación"),
            content=ft.Text("¿Estás seguro de que quieres eliminar tu cuenta? Esta acción es irreversible."),
            actions=[
                ft.TextButton("Sí", on_click=confirm_delete),
                ft.TextButton("No", on_click=confirm_delete),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog.open = True
        page.update()
        print("DEBUG: Diálogo de eliminación abierto.")


    # Asignar los on_click a los botones del AppBar
    edit_button_appbar.on_click = toggle_edit_mode
    delete_button_appbar.on_click = on_delete_user
    save_button_appbar.on_click = on_save_changes
    cancel_button_appbar.on_click = on_cancel_edit

    # Conectar los botones de la vista con sus funciones (botones de la parte inferior)
    save_button.on_click = on_save_changes
    cancel_button.on_click = on_cancel_edit

    return ft.View(
        "/profile", 
        [
            profile_appbar, 
            ft.Column(
                [
                    ft.Text("Detalles de tu Perfil", style=heading_large_style()),
                    ft.Divider(height=30),
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
                    )
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