# styles.py

import flet as ft

def button_style():
    return ft.ButtonStyle(
        color={
            # ¡Corregido! Usar ft.ControlState en lugar de ft.MaterialState
            ft.ControlState.HOVERED: ft.Colors.WHITE,
            ft.ControlState.FOCUSED: ft.Colors.BLUE_GREY_100,
            ft.ControlState.DEFAULT: ft.Colors.BLUE_GREY_900,
        },
        bgcolor={
            # ¡Corregido! Usar ft.ControlState en lugar de ft.MaterialState
            ft.ControlState.HOVERED: ft.Colors.GREEN_600,
            ft.ControlState.FOCUSED: ft.Colors.GREEN_700,
            ft.ControlState.DEFAULT: ft.Colors.GREEN_500,
        },
        padding=10,
        shape=ft.RoundedRectangleBorder(radius=5),
    )

def text_heading_style():
    return ft.TextStyle(
        size=24,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.DEEP_PURPLE_700,
    )

def container_card_style():
    return {
        "width": 300,
        "padding": 20,
        "border_radius": 10,
        "bgcolor": ft.Colors.BLUE_GREY_50,
        "shadow": ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.BLUE_GREY_300,
            offset=ft.Offset(0, 0),
            blur_style=ft.ShadowBlurStyle.OUTER,
        ),
    }

def app_theme():
    return ft.Theme(
        color_scheme_seed=ft.Colors.GREEN,
        use_material3=True,
    )