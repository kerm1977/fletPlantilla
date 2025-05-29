# styles.py

import flet as ft

# Colores primarios y de acento para usar en el tema y otros componentes
PRIMARY_COLOR = ft.Colors.ORANGE_700
ACCENT_COLOR = ft.Colors.BLUE_700

def app_theme():
    """
    Define el tema general de la aplicación.
    """
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=PRIMARY_COLOR,
            primary_container=ft.Colors.ORANGE_100,
            on_primary=ft.Colors.WHITE,
            secondary=ACCENT_COLOR,
            secondary_container=ft.Colors.BLUE_100,
            on_secondary=ft.Colors.WHITE,
            surface=ft.Colors.WHITE,
            on_surface=ft.Colors.BLACK,
            background=ft.Colors.WHITE,
            on_background=ft.Colors.BLACK,
            error=ft.Colors.RED_700,
            on_error=ft.Colors.WHITE,
        ),
    )

def page_background_style():
    """
    Define el estilo del fondo de la página.
    Devuelve un diccionario porque es usado como **kwargs.
    """
    return {"bgcolor": ft.Colors.BLUE_GREY_50}

# --- Estilos de Texto ---
def heading_large_style():
    """
    Estilo para títulos grandes.
    Devuelve un objeto ft.TextStyle.
    """
    return ft.TextStyle(size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900)

def heading_medium_style():
    """
    Estilo para títulos medianos.
    Devuelve un objeto ft.TextStyle.
    """
    return ft.TextStyle(size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900)

def body_text_style():
    """
    Estilo para texto de cuerpo general.
    Devuelve un objeto ft.TextStyle.
    """
    return ft.TextStyle(size=16, color=ft.Colors.BLUE_GREY_700)

def caption_text_style():
    """
    Estilo para texto de subtítulos o descripciones pequeñas.
    Devuelve un objeto ft.TextStyle.
    """
    return ft.TextStyle(size=12, color=ft.Colors.BLUE_GREY_500)

# --- Estilos de Botones ---
def primary_button_style():
    """
    Estilo para botones de acción principal.
    Devuelve un objeto ft.ButtonStyle.
    """
    return ft.ButtonStyle(
        color={
            # ¡CAMBIADO a ft.ControlState.HOVERED!
            ft.ControlState.HOVERED: ft.Colors.WHITE,
            ft.ControlState.FOCUSED: ft.Colors.WHITE,
            ft.ControlState.DEFAULT: ft.Colors.WHITE,
        },
        bgcolor=PRIMARY_COLOR,
        padding=ft.padding.all(15),
        shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(8)),
    )

def outline_button_style():
    """
    Estilo para botones con contorno.
    Devuelve un objeto ft.ButtonStyle.
    """
    return ft.ButtonStyle(
        color=PRIMARY_COLOR,
        bgcolor=ft.Colors.TRANSPARENT,
        side=ft.BorderSide(2, PRIMARY_COLOR),
        padding=ft.padding.all(15),
        shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(8)),
    )

def text_button_style():
    """
    Estilo para botones de texto (enlaces).
    Devuelve un objeto ft.ButtonStyle.
    """
    return ft.ButtonStyle(
        color=ACCENT_COLOR,
        padding=ft.padding.all(10),
    )

# --- Estilos de Contenedores y Entradas de Texto ---
def card_container_style():
    """
    Estilo para contenedores tipo tarjeta.
    Devuelve un diccionario porque es usado como **kwargs.
    """
    return {
        "padding": ft.padding.all(15),
        "border_radius": ft.border_radius.all(10),
        "bgcolor": ft.Colors.WHITE,
        "elevation": 3,
    }

def text_input_style():
    """
    Estilo base para campos de entrada de texto.
    Devuelve un diccionario porque es usado como **kwargs.
    """
    return {
        "border_radius": ft.border_radius.all(8),
        "filled": True,
        "fill_color": ft.Colors.WHITE,
        "border_color": ft.Colors.GREY_300,
        "focused_border_color": PRIMARY_COLOR,
        "label_style": ft.TextStyle(color=ft.Colors.GREY_600),
        "cursor_color": PRIMARY_COLOR,
        "hint_style": ft.TextStyle(color=ft.Colors.GREY_400),
    }

def image_card_container_style():
    """
    Estilo para contenedores de tarjetas de imagen.
    Devuelve un diccionario porque es usado como **kwargs.
    """
    return {
        "width": 150,
        "height": 150,
        "border_radius": ft.border_radius.all(10),
        "clip_behavior": ft.ClipBehavior.ANTI_ALIAS,
    }