import pygame as pg
import modules.variables as var
import modules.auxiliar as aux
import modules.sonido as audio
import modules.form_controller as fc

def iniciar(ctx: dict) -> None:
    """Inicializa el form de Ajustes del juego.

    Configura:
        - Estado de audio global si no existe.
        - Variables locales para musica habilitada y volumen.
        - Fuentes principales y secundarias.
        - Fondo escalado.
        - Botones para apagar/prender musica.
        - Botones para subir/bajar volumen y label del volumen actual.
        - Boton para volver al menu principal.

    Args:
        ctx (dict): Contexto general del juego con todos los forms y audio.

    Returns:
        None
    """
    ctx["forms"]["settings"] = {}
    data = ctx["forms"]["settings"]

    # --- INICIALIZAR AUDIO GLOBAL SI FALTA ---
    audio.init_audio_state(ctx)

    # --- LEER EL ESTADO REAL DE AUDIO ---
    data["music_enabled"] = ctx["audio"]["enabled"]
    data["volume"] = audio.get_volume_0_100(ctx)

    # --- Fuentes ---
    data["font"] = pg.font.Font(var.FONT_PATH, 35)
    data["alt_font"] = pg.font.Font(var.ALT_FONT_PATH, 36)

    # --- Fondo ---
    fondo = pg.image.load(var.FONDO_OPTIONS)
    data["fondo"] = pg.transform.scale(fondo, (var.ASPECT_RATIO))

    # --- Botones Musica ---
    data["btn_music_off"] = aux.create_button(
        "Apagar Musica", data["font"], var.COLORS["white"], var.COLORS["bg"],
        x=360, y=55, w=280, h=50,
        hover_color=var.COLORS["hover"]
    )
    data["btn_music_on"] = aux.create_button(
        "Prender Musica", data["font"], var.COLORS["white"], var.COLORS["bg"],
        x=360, y=125, w=280, h=50,
        hover_color=var.COLORS["hover"]
    )

    # --- Controles de Volumen ---
    data["btn_vol_down"] = aux.create_button(
        "-", data["alt_font"], var.COLORS["white"], var.COLORS["bg"],
        x=330, y=260, w=60, h=60,
        hover_color=var.COLORS["hover"]
    )
    data["btn_vol_up"] = aux.create_button(
        "+", data["alt_font"], var.COLORS["white"], var.COLORS["bg"],
        x=617, y=260, w=60, h=60,
        hover_color=var.COLORS["hover"]
    )

    # Label del numero de volumen
    data["lbl_volumen"] = aux.create_label(
        str(data["volume"]), data["alt_font"], (255,255,255), x=485, y=280
    )

    # --- Boton Volver ---
    data["btn_volver"] = aux.create_button(
        "Volver", data["font"], var.COLORS["white"], var.COLORS["bg"],
        x=400, y=500, w=200, h=50,
        hover_color=var.COLORS["red"]
    )


def handle_event(ctx: dict, event: pg.event.Event) -> None:
    """Gestiona eventos de la pantalla de Ajustes.

    - Detecta clics en botones para apagar/prender musica.
    - Detecta clics en botones de volumen y ajusta volumen global y label.
    - Detecta clic en boton Volver para regresar al menu principal.

    Args:
        ctx (dict): Contexto general del juego con forms y audio.
        event (pg.event.Event): Evento de pygame a procesar.

    Returns:
        None
    """
    data = ctx["forms"]["settings"]
    if event.type != pg.MOUSEBUTTONDOWN:
        return

    mouse_pos = pg.mouse.get_pos()
    press = pg.mouse.get_pressed()

    # Volver al menu
    if aux.button_is_clicked(data["btn_volver"], mouse_pos, press):
        fc.cambiar_form(ctx, "menu")
        return

    # Apagar musica
    if aux.button_is_clicked(data["btn_music_off"], mouse_pos, press):
        audio.music_off(ctx)
        data["music_enabled"] = False

    # Prender musica
    if aux.button_is_clicked(data["btn_music_on"], mouse_pos, press):
        audio.music_on(ctx)
        data["music_enabled"] = True

    # Bajar volumen
    if aux.button_is_clicked(data["btn_vol_down"], mouse_pos, press):
        data["volume"] = max(1, data["volume"] - 5)
        audio.set_volume_0_100(ctx, data["volume"])
        data["lbl_volumen"]["text"] = str(data["volume"])
        data["lbl_volumen"]["surface"] = data["lbl_volumen"]["font"].render(
            data["lbl_volumen"]["text"], True, data["lbl_volumen"]["color"]
        )

    # Subir volumen
    if aux.button_is_clicked(data["btn_vol_up"], mouse_pos, press):
        data["volume"] = min(100, data["volume"] + 5)
        audio.set_volume_0_100(ctx, data["volume"])
        data["lbl_volumen"]["text"] = str(data["volume"])
        data["lbl_volumen"]["surface"] = data["lbl_volumen"]["font"].render(
            data["lbl_volumen"]["text"], True, data["lbl_volumen"]["color"]
        )


def update(ctx: dict) -> None:
    """Actualiza la logica de la pantalla de Ajustes.

    Actualmente no realiza acciones adicionales.

    Args:
        ctx (dict): Contexto general del juego con forms y audio.

    Returns:
        None
    """
    pass


def draw(ctx: dict) -> None:
    """Dibuja la pantalla de Ajustes en pantalla.

    - Fondo de la pantalla.
    - Label de volumen actual.
    - Botones con efecto hover.

    Args:
        ctx (dict): Contexto general del juego con forms y audio.

    Returns:
        None
    """
    screen = ctx["screen"]
    data = ctx["forms"]["settings"]

    screen.blit(data["fondo"], (0,0))
    aux.draw_label(screen, data["lbl_volumen"])

    mouse_pos = pg.mouse.get_pos()
    for key in ["btn_music_off", "btn_music_on", "btn_vol_down", "btn_vol_up", "btn_volver"]:
        aux.update_button_hover(data[key], mouse_pos)
        aux.draw_button(screen, data[key])
