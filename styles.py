import flet as ft

# --- Paleta de Colores Vistosos ---
PRIMARY_COLOR = ft.Colors.BLUE_ACCENT_700
PRIMARY_COLOR_LIGHT = ft.Colors.BLUE_ACCENT_100
ACCENT_COLOR = ft.Colors.CYAN_700
BACKGROUND_COLOR = ft.Colors.WHITE
SURFACE_COLOR = ft.Colors.GREY_50
TEXT_COLOR_DARK = ft.Colors.BLUE_GREY_900
TEXT_COLOR_LIGHT = ft.Colors.BLUE_GREY_400
ERROR_COLOR = ft.Colors.RED_ACCENT_700

# --- Estilos de Texto ---
def heading_large_style():
    return ft.TextStyle(
        size=28,
        weight=ft.FontWeight.BOLD,
        color=TEXT_COLOR_DARK,
    )

def heading_medium_style():
    return ft.TextStyle(
        size=22,
        weight=ft.FontWeight.W_600,
        color=TEXT_COLOR_DARK,
    )

def body_text_style():
    return ft.TextStyle(
        size=16,
        color=TEXT_COLOR_DARK,
    )

def caption_text_style():
    return ft.TextStyle(
        size=12,
        color=TEXT_COLOR_LIGHT,
    )

# --- Estilos de Botones ---
def primary_button_style():
    return ft.ButtonStyle(
        color={
            ft.ControlState.HOVERED: ft.Colors.WHITE,
            ft.ControlState.FOCUSED: ft.Colors.WHITE,
            ft.ControlState.DEFAULT: ft.Colors.WHITE,
        },
        bgcolor={
            ft.ControlState.HOVERED: ft.Colors.BLUE_ACCENT_400,
            ft.ControlState.FOCUSED: PRIMARY_COLOR,
            ft.ControlState.DEFAULT: PRIMARY_COLOR,
        },
        padding=ft.padding.symmetric(horizontal=25, vertical=15),
        shape=ft.RoundedRectangleBorder(radius=10),
        animation_duration=300,
    )

def outline_button_style():
    return ft.ButtonStyle(
        color=PRIMARY_COLOR,
        bgcolor=ft.Colors.TRANSPARENT,
        side=ft.BorderSide(2, PRIMARY_COLOR),
        padding=ft.padding.symmetric(horizontal=25, vertical=15),
        shape=ft.RoundedRectangleBorder(radius=10),
        animation_duration=300,
    )

def text_button_style():
    return ft.ButtonStyle(
        color=ACCENT_COLOR,
        bgcolor=ft.Colors.TRANSPARENT,
        # Corregido: Usa ft.Colors.with_opacity(opacity, color_base)
        overlay_color=ft.Colors.with_opacity(0.1, ft.Colors.CYAN),
        padding=ft.padding.symmetric(horizontal=15, vertical=10),
        shape=ft.RoundedRectangleBorder(radius=8),
    )

# --- Estilos de Contenedores y Tarjetas (Cards) ---
def card_container_style():
    return {
        "padding": 20,
        "border_radius": 15,
        "bgcolor": SURFACE_COLOR,
        "shadow": ft.BoxShadow(
            spread_radius=2,
            blur_radius=15,
            # ¡Corregido! Usa ft.Colors.with_opacity(opacity, color_base)
            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
            offset=ft.Offset(0, 5),
            blur_style=ft.ShadowBlurStyle.NORMAL,
        ),
    }

def image_card_container_style():
    return {
        "padding": 10,
        "border_radius": 15,
        "bgcolor": SURFACE_COLOR,
        "clip_behavior": ft.ClipBehavior.ANTI_ALIAS,
        "shadow": ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            # ¡Corregido! Usa ft.Colors.with_opacity(opacity, color_base)
            color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
            offset=ft.Offset(0, 3),
            blur_style=ft.ShadowBlurStyle.NORMAL,
        ),
    }

# --- Estilos de Campos de Texto (Input) ---
def text_input_style():
    return {
        "border_radius": 10,
        "border_color": ft.Colors.BLUE_GREY_200,
        "focused_border_color": PRIMARY_COLOR,
        "filled": True,
        "fill_color": ft.Colors.GREY_100,
        "content_padding": 12,
        "cursor_color": PRIMARY_COLOR,
        "label_style": body_text_style(),
    }

# --- Tema General de la Aplicación ---
def app_theme():
    return ft.Theme(
        color_scheme_seed=PRIMARY_COLOR,
        use_material3=True,
    )

# --- Estilos de la Página (Opcional, para el fondo) ---
def page_background_style():
    return {
        "bgcolor": BACKGROUND_COLOR,
    }