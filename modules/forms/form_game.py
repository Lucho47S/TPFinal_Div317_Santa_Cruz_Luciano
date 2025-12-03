import pygame as pg
import random
import modules.variables as var
import modules.auxiliar as aux
import modules.sonido as so
import modules.gameplay as gp

def iniciar(ctx: dict) -> None:
    """Inicializa el form de combate (pantalla de juego).

    Configura:
        - Contexto de combate en ctx["forms"]["combat"].
        - Puntaje inicial.
        - Indices y cartas actuales.
        - Fuentes para labels grandes y pequeños.
        - Fondo de la pantalla.
        - Timer de la partida.
        - Labels de puntaje y stats de jugador y rival.
        - Estados de comodines (heal y shield).
        - Botones de mazo y botones de acción.
        - Inicialización de mazos y stats promedio.

    Args:
        ctx (dict): Contexto global del juego con todos los forms.
    """
    ctx["forms"]["combat"] = {}
    data = ctx["forms"]["combat"]

    data["puntaje"] = 0
    data["turno_actual"] = 0
    
    gp.iniciar_puntaje(ctx)
    
    data["mazo_index_player"] = 0
    data["mazo_index_rival"] = 0

    data["carta_player_actual"] = None
    data["carta_rival_actual"] = None

    # Fuentes
    data["font_big"] = pg.font.Font(var.ALT_FONT_PATH, 26)
    data["font_small"] = pg.font.Font(var.ALT_FONT_PATH, 20)

    # Fondo
    data["fondo"] = pg.transform.scale(pg.image.load(var.FONDO_STAGE), var.ASPECT_RATIO)

    # Timer
    data["timer_max"] = var.STAGE_TIMER
    data["timer_actual"] = var.STAGE_TIMER

    # Label puntaje
    data["puntaje_label"] = aux.create_label(
        text="Puntaje: 0", font=data["font_big"], color=var.COLORS["white"], x=20, y=20
    )

    # Stats jugador y rival
    data["stats_jugador"] = [
        aux.create_label("HP: 0", data["font_small"], var.COLORS["white"], 85, 425),
        aux.create_label("ATK: 0", data["font_small"], var.COLORS["white"], 85, 445),
        aux.create_label("DEF: 0", data["font_small"], var.COLORS["white"], 85, 465)
    ]
    data["stats_rival"] = [
        aux.create_label("HP: 0", data["font_small"], var.COLORS["white"], 85, 150),
        aux.create_label("ATK: 0", data["font_small"], var.COLORS["white"], 85, 170),
        aux.create_label("DEF: 0", data["font_small"], var.COLORS["white"], 85, 190)
    ]

    # Estados de comodines
    data["heal_usado"] = False
    data["shield_usado"] = False
    data["shield_activo"] = False
    data["hp_inicial_player"] = 0 

    # Botones de mazo
    data["mazo_botones"] = [
        aux.create_image_button("assets/img/decks/black_deck_expansion_1/reverse.png", 300, 100, 130, 180),
        aux.create_image_button("assets/img/decks/black_deck_expansion_1/reverse.png", 300, 380, 130, 180),
    ]

    # Botones de accion (robar carta, heal, shield)
    data["accion"] = [
        aux.create_image_button(var.PLAY_HAND, 887, 295, 100, 45),
        aux.create_image_button(var.WISH_HEAL, 890, 460, 100, 35),
        aux.create_image_button(var.WISH_SHIELD, 890, 500, 100, 35)
    ]
    for b in data["accion"]:
        if "visible" not in b:
            b["visible"] = True

    iniciar_mazos(data)
    data["hp_inicial_player"] = data["stats_p"]["hp"]


def iniciar_mazos(data: dict) -> None:
    """Inicializa los mazos de jugador y rival y calcula sus stats promedio.

    Args:
        data (dict): Diccionario de datos del form de combate.
    """
    todas = gp.load_cards(var.JSON_CARDS)
    por_serie = gp.filter_cards_by_series(todas)

    data["mazo_player"] = gp.generate_random_deck(por_serie, var.DISTRIBUCION_MAZO)
    data["mazo_rival"]  = gp.generate_random_deck(por_serie, var.DISTRIBUCION_MAZO)

    random.shuffle(data["mazo_player"])
    random.shuffle(data["mazo_rival"])

    # Stats promedio
    data["stats_p"] = gp.calculate_average_stats(data["mazo_player"])
    data["stats_r"] = gp.calculate_average_stats(data["mazo_rival"])

    # Mano inicial
    data["mano_player"] = None
    data["mano_rival"] = None

    # Mazo reverso
    data["mazo_reverso_rival"]  = gp.load_rev(data["mazo_rival"])
    data["mazo_reverso_player"] = gp.load_rev(data["mazo_player"])


def handle_event(ctx: dict, event: pg.event.Event) -> None:
    """Gestiona eventos de mouse en la pantalla de combate.

    - Detecta clic en botones de acción: robar carta, heal y shield.
    - Actualiza el estado del juego tras cada acción.

    Args:
        ctx (dict): Contexto del juego con forms.
        event (pg.event.Event): Evento de Pygame.
    """
    data = ctx["forms"]["combat"]

    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        mouse = event.pos

        # Robar carta
        btn_play = data["accion"][0]
        if btn_play.get("visible", True) and btn_play["rect"].collidepoint(mouse):
            gp.robar_carta(ctx, player=True)
            gp.resolver_mano(ctx)
            gp.check_fin_partida(ctx)
            aux.update_label(data["puntaje_label"], f"Puntaje: {data['puntaje']}")
            return

        # Heal
        btn_heal = data["accion"][1]
        if btn_heal.get("visible", True) and btn_heal["rect"].collidepoint(mouse) and not data["heal_usado"]:
            gp.activar_heal(ctx)
            return

        # Shield
        btn_shield = data["accion"][2]
        if btn_shield.get("visible", True) and btn_shield["rect"].collidepoint(mouse) and not data["shield_usado"]:
            gp.activar_shield(ctx)
            return


def update(ctx: dict) -> None:
    """Actualiza la lógica de juego en la pantalla de combate.

    - Decrementa el timer.
    - Revisa si la partida terminó.

    Args:
        ctx (dict): Contexto del juego con forms.
    """
    data = ctx["forms"]["combat"]
    dt = ctx["clock"].get_time()
    data["timer_actual"] -= dt
    if data["timer_actual"] < 0:
        data["timer_actual"] = 0
    gp.check_fin_partida(ctx)


def draw(ctx: dict) -> None:
    """Dibuja la pantalla de combate en el Pygame screen.

    - Fondo, labels de puntaje y stats.
    - Timer de la partida.
    - Mazo y botones visibles.
    - Cartas actuales de jugador y rival.

    Args:
        ctx (dict): Contexto del juego con forms.
    """
    screen = ctx["screen"]
    data = ctx["forms"]["combat"]

    screen.blit(data["fondo"], (0, 0))
    aux.draw_label(screen, data["puntaje_label"])

    # Timer
    timer_text = data["font_big"].render(
        f"Tiempo: {data['timer_actual'] // 1000}", True, var.COLORS["white"]
    )
    screen.blit(timer_text, (430, 20))

    # Stats
    for s in data["stats_jugador"]:
        aux.draw_label(screen, s)
    for s in data["stats_rival"]:
        aux.draw_label(screen, s)

    aux.update_label(data["stats_jugador"][0], f"HP: {data['stats_p']['hp']}")
    aux.update_label(data["stats_jugador"][1], f"ATK: {data['stats_p']['atk']}")
    aux.update_label(data["stats_jugador"][2], f"DEF: {data['stats_p']['def']}")

    aux.update_label(data["stats_rival"][0], f"HP: {data['stats_r']['hp']}")
    aux.update_label(data["stats_rival"][1], f"ATK: {data['stats_r']['atk']}")
    aux.update_label(data["stats_rival"][2], f"DEF: {data['stats_r']['def']}")

    if data["mazo_reverso_rival"]:
        data["mazo_botones"][0]["image"] = data["mazo_reverso_rival"]
    if data["mazo_reverso_player"]:
        data["mazo_botones"][1]["image"] = data["mazo_reverso_player"]

    # Dibujar mazo y botones
    for b in data["mazo_botones"]:
        aux.draw_image_button(screen, b)
    for b in data["accion"]:
        if b.get("visible", True):
            aux.draw_image_button(screen, b)
    
    # Cartas actuales
    if data["carta_player_actual"]:
        img = pg.image.load(data["carta_player_actual"]["ruta_frente"])
        img = pg.transform.scale(img, (150, 210))
        screen.blit(img, (450, 365))
    if data["carta_rival_actual"]:
        img = pg.image.load(data["carta_rival_actual"]["ruta_frente"])
        img = pg.transform.scale(img, (150, 210))
        screen.blit(img, (450, 90))


