import pygame as pg
import modules.variables as var
import modules.auxiliar as aux
import modules.form_controller as fc

def iniciar(event: dict) -> None:
    """Inicializa la pantalla de ranking (Score).

    Crea y configura:
        - Fuentes de letra.
        - Fondo.
        - Label del titulo "Puntajes".
        - Lista de puntajes leida desde CSV y ordenada descendente.
        - Labels de los 10 mejores puntajes.
        - Boton "Volver" al menu principal.

    Args:
        event (dict): Contexto general del juego con todos los forms.

    Returns:
        None
    """
    event["forms"]["score"] = {}
    data = event["forms"]["score"]

    # fuentes
    data["font_title"] = pg.font.Font(var.FONT_PATH, 48)
    data["font_button"] = pg.font.Font(var.FONT_PATH, 36)
    data["font"] = pg.font.Font(var.ALT_FONT_PATH, 28)

    # fondo
    fondo = pg.image.load(var.FONDO_SCORE)
    data["fondo"] = pg.transform.scale(fondo, (var.ASPECT_RATIO))

    # título
    data["titulo"] = aux.create_label(
        "Puntajes", data["font_title"], var.COLORS["white"], 420, 60
    )

    # cargar puntajes desde CSV
    lista = aux.read_scores_csv(var.RANKING_CSV)

    # ordenar por puntaje descendente
    lista = aux.selection_sort_scores(lista)

    # top 10
    lista = lista[:10]

    # generar labels
    labels = []
    y = 140
    for nombre, puntaje in lista:
        texto = f"{nombre}  -  {puntaje}"
        label = aux.create_label(texto, data["font"], (255, 255, 255), 400, y)
        labels.append(label)
        y += 32
    data["labels_scores"] = labels

    # boton volver
    data["btn_volver"] = aux.create_button(
        "Volver", data["font_button"], var.COLORS["white"], var.COLORS["bg"],
        x=401, y=485, w=200, h=50,
        hover_color=var.COLORS["red"]
    )


def handle_event(event: dict, ctx: pg.event.Event) -> None:
    """Gestiona eventos de la pantalla Score.

    Detecta clics en el boton "Volver" y cambia el form a menu.

    Args:
        event (dict): Contexto general del juego.
        ctx (pygame.event.Event): Evento de pygame a procesar.

    Returns:
        None
    """
    data = event["forms"]["score"]

    if ctx.type == pg.MOUSEBUTTONDOWN:
        mouse_pos = pg.mouse.get_pos()
        mouse_pr = pg.mouse.get_pressed()

        if aux.button_is_clicked(data["btn_volver"], mouse_pos, mouse_pr):
            fc.cambiar_form(event, "menu")


def update(event: dict) -> None:
    """Actualiza la logica de la pantalla Score.

    Por ahora no realiza acciones adicionales.

    Args:
        event (dict): Contexto general del juego.

    Returns:
        None
    """
    pass


def draw(event: dict) -> None:
    """Dibuja la pantalla Score en pantalla.

    Se dibuja:
        - Fondo.
        - Titulo.
        - Lista de puntajes.
        - Boton "Volver" con efecto hover.

    Args:
        event (dict): Contexto general del juego.

    Returns:
        None
    """
    screen = event["screen"]
    data = event["forms"]["score"]

    # fondo
    screen.blit(data["fondo"], (0, 0))

    # título
    aux.draw_label(screen, data["titulo"])

    # lista
    for lbl in data["labels_scores"]:
        aux.draw_label(screen, lbl)
    
    # hover + boton
    mouse_pos = pg.mouse.get_pos()
    aux.update_button_hover(data["btn_volver"], mouse_pos)
    aux.draw_button(screen, data["btn_volver"])
