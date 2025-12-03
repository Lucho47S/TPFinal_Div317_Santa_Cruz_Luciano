import pygame as pg
import modules.variables as var
import modules.auxiliar as aux
from modules import form_controller as fc

def iniciar(ctx: dict) -> None:
    """Inicializa el form del menú principal del juego.

    Configura:
        - Fuente principal.
        - Fondo escalado.
        - Labels de título y subtítulo.
        - Botones: Jugar, Ranking, Opciones y Salir.

    Args:
        ctx (dict): Contexto general del juego con todos los forms.

    Returns:
        None
    """
    ctx["forms"]["menu"] = {}
    data = ctx["forms"]["menu"]

    # Fuente
    data["font"] = pg.font.Font(var.FONT_PATH, 40)

    # Fondo
    fondo = pg.image.load(var.FONDO_MENU)
    data["fondo"] = pg.transform.scale(fondo, var.ASPECT_RATIO)

    # Labels
    data["titulo"] = aux.create_label(
        text="Yu Gi Ball", font=data["font"], color=var.COLORS["white"], x=420, y=80)
    data["subtitulo"] = aux.create_label(
        text="Trading Card Game", font=data["font"], color=var.COLORS["white"], x=370, y=120)

    # Botones
    data["botones"] = [
        aux.create_button(text="Jugar",   
                          font=data["font"], 
                          txt_color=var.COLORS["white"], 
                          bg_color=var.COLORS["bg"], 
                          x=400, y=285, w=200, h=45,
                          hover_color=var.COLORS["hover"]),

        aux.create_button(text="Ranking",  
                          font=data["font"], 
                          txt_color=var.COLORS["white"], 
                          bg_color=var.COLORS["bg"], 
                          x=400, y=345, w=200, h=45,
                          hover_color=var.COLORS["hover"]),

        aux.create_button(text="opciones", 
                          font=data["font"], 
                          txt_color=var.COLORS["white"], 
                          bg_color=var.COLORS["bg"], 
                          x=400, y=405, w=200, h=45,
                          hover_color=var.COLORS["hover"]),

        aux.create_button(text="Salir",
                          font=data["font"], 
                          txt_color=var.COLORS["white"], 
                          bg_color=var.COLORS["bg"],
                          x=400, y=465, w=200, h=45,
                          hover_color=var.COLORS["red"]),
    ]


def handle_event(ctx: dict, event: pg.event.Event) -> None:
    """Gestiona eventos del menú principal.

    - Detecta clics en los botones y cambia de pantalla según corresponda:
        * "Jugar" -> pantalla de juego
        * "Ranking" -> pantalla de puntajes
        * "opciones" -> pantalla de ajustes
        * "Salir" -> cierra el juego

    Args:
        ctx (dict): Contexto general del juego con forms.
        event (pg.event.Event): Evento de pygame a procesar.

    Returns:
        None
    """
    data = ctx["forms"]["menu"]

    if event.type == pg.MOUSEBUTTONDOWN:
        mouse_pos = pg.mouse.get_pos()
        pressed = pg.mouse.get_pressed()

        for b in data["botones"]:
            if aux.button_is_clicked(b, mouse_pos, pressed):
                txt = b["text"]

                match txt:
                    case "Jugar":
                        fc.cambiar_form(ctx, "juego")
                    case "Ranking": 
                        fc.cambiar_form(ctx, "score")
                    case "opciones":
                        fc.cambiar_form(ctx, "options")
                    case "Salir":
                        pg.quit()
                        exit()


def update(ctx: dict) -> None:
    """Actualiza la lógica del menú principal.

    Actualmente no realiza acciones adicionales.

    Args:
        ctx (dict): Contexto general del juego con forms.

    Returns:
        None
    """
    pass


def draw(ctx: dict) -> None:
    """Dibuja la pantalla del menú principal en pantalla.

    - Fondo del menú.
    - Labels de título y subtítulo.
    - Botones con efecto hover.

    Args:
        ctx (dict): Contexto general del juego con forms.

    Returns:
        None
    """
    screen = ctx["screen"]
    data = ctx["forms"]["menu"]

    # Fondo
    screen.blit(data["fondo"], (0, 0))

    # Labels
    aux.draw_label(screen, data["titulo"])
    aux.draw_label(screen, data["subtitulo"])

    # Botones + efecto hover
    mouse_pos = pg.mouse.get_pos()
    for b in data["botones"]:
        aux.update_button_hover(b, mouse_pos)
        aux.draw_button(screen, b)
