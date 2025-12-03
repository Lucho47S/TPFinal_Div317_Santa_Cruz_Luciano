import pygame as pg
import modules.variables as var
import modules.auxiliar as aux
import modules.gameplay as gp
import modules.form_controller as fc

def iniciar(ctx: dict) -> None:
    """Inicializa el form de resultados de la partida.

    Configura:
        - Fuentes grandes y pequeñas.
        - Fondo escalado.
        - Labels: titulo, puntaje y instruccion para ingresar nombre.
        - Campo de texto para que el jugador escriba su nombre.
        - Botones disponibles (por ejemplo: 'Guardar y Volver').

    Args:
        ctx (dict): Contexto general del juego con todos los forms.

    Returns:
        None
    """
    ctx["forms"]["resultados"] = {}
    data = ctx["forms"]["resultados"]

    # Fuente
    data["font_big"] = pg.font.Font(var.FONT_PATH, 40)
    data["font_small"] = pg.font.Font(var.ALT_FONT_PATH, 28)

    # Fondo
    if ctx["forms"]["combat"].get("victoria", True):
        fondo = pg.image.load(var.FONDO_VICTORIA)
    else:
        fondo = pg.image.load(var.FONDO_DERROTA)
    data["fondo"] = pg.transform.scale(fondo, var.ASPECT_RATIO)


    # Labels
    data["titulo"] = aux.create_label(
        text="¡Partida Finalizada!", font=data["font_big"], color=var.COLORS["white"], x=355, y=80
    )
    data["puntaje_label"] = aux.create_label(
        text=f"Puntaje: {ctx['forms']['combat'].get('puntaje', 0)}",
        font=data["font_small"], color=var.COLORS["white"], x=400, y=200
    )
    data["instruccion"] = aux.create_label(
        text="Ingresa tu nombre:", font=data["font_small"], color=var.COLORS["white"], x=370, y=270
    )

    # Campo de texto
    data["nombre_input"] = {
        "rect": pg.Rect(345, 320, 300, 40),
        "color": var.COLORS["white"],
        "text": "",
        "active": False,
        "font": data["font_small"]
    }

    # Botones
    data["botones"] = [
        aux.create_button(
            text="Guardar y Volver",
            font=data["font_small"],
            txt_color=var.COLORS["white"],
            bg_color=var.COLORS["bg"],
            x=345, y=460, w=300, h=45,
            hover_color=var.COLORS["hover"]
        ),
    ]


def handle_event(ctx: dict, event: pg.event.Event) -> None:
    """Gestiona eventos de la pantalla de resultados.

    - Detecta clic en el campo de texto para activarlo.
    - Maneja escritura de texto con teclado.
    - Detecta clic en los botones y ejecuta acciones (guardar puntaje y volver al menu).
    - Valida que el nombre ingresado sea valido antes de guardar.

    Args:
        ctx (dict): Contexto general del juego con forms.
        event (pg.event.Event): Evento de pygame a procesar.

    Returns:
        None
    """
    data = ctx["forms"]["resultados"]

    if event.type == pg.MOUSEBUTTONDOWN:
        mouse_pos = pg.mouse.get_pos()

        # Activar campo de texto si se clickea
        if data["nombre_input"]["rect"].collidepoint(mouse_pos):
            data["nombre_input"]["active"] = True
        else:
            data["nombre_input"]["active"] = False

        # Botones
        pressed = pg.mouse.get_pressed()
        for b in data["botones"]:
            if aux.button_is_clicked(b, mouse_pos, pressed):
                if b["text"] == "Guardar y Volver":
                    nombre = data["nombre_input"]["text"].strip()
                    if nombre:
                        if aux.nombre_valido(nombre):
                            puntaje = ctx['forms']['combat'].get('puntaje', 0)
                            aux.guardar_puntaje_csv("puntajes.csv", nombre, puntaje)
                            fc.cambiar_form(ctx, "menu")
                        else:
                            print("Nombre Invalido")
                elif b["text"] == "Salir":
                    exit()

    elif event.type == pg.KEYDOWN and data["nombre_input"]["active"]:
        # Manejar escritura de texto
        if event.key == pg.K_BACKSPACE:
            data["nombre_input"]["text"] = data["nombre_input"]["text"][:-1]
        else:
            if len(data["nombre_input"]["text"]) < 15:  # limite de caracteres
                data["nombre_input"]["text"] += event.unicode


def update(ctx: dict) -> None:
    """Actualiza la logica de la pantalla de resultados.

    Actualmente no realiza acciones adicionales.

    Args:
        ctx (dict): Contexto general del juego con forms.

    Returns:
        None
    """
    pass


def draw(ctx: dict) -> None:
    """Dibuja la pantalla de resultados en pantalla.

    Se dibuja:
        - Fondo de la pantalla.
        - Labels: titulo, puntaje y instruccion.
        - Campo de texto con borde y texto ingresado.
        - Botones con efecto hover.

    Args:
        ctx (dict): Contexto general del juego con forms.

    Returns:
        None
    """
    screen = ctx["screen"]
    data = ctx["forms"]["resultados"]

    # Fondo
    screen.blit(data["fondo"], (0, 0))

    # Labels
    aux.draw_label(screen, data["titulo"])
    aux.draw_label(screen, data["instruccion"])

    puntaje_total = ctx["forms"]["combat"].get("puntaje", 0)
    aux.update_label(data["puntaje_label"], f"Puntaje: {puntaje_total}")
    aux.draw_label(screen, data["puntaje_label"])

    # Campo de texto
    rect = data["nombre_input"]["rect"]
    pg.draw.rect(screen, data["nombre_input"]["color"], rect, 2)
    txt_surf = data["nombre_input"]["font"].render(data["nombre_input"]["text"], True, var.COLORS["white"])
    screen.blit(txt_surf, (rect.x+5, rect.y+5))

    # Botones
    mouse_pos = pg.mouse.get_pos()
    for b in data["botones"]:
        aux.update_button_hover(b, mouse_pos)
        aux.draw_button(screen, b)
