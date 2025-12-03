import json
import random
import pygame as pg
import modules.sonido as so
import modules.variables as var 
import modules.form_controller as fc

def load_cards(path: str) -> list:
    """Carga un archivo JSON con cartas y devuelve la lista de cartas.

    Args:
        path (str): Ruta del archivo JSON.

    Returns:
        list: Lista de cartas (diccionarios).
    """
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def filter_cards_by_series(cards: list) -> dict:
    """Organiza las cartas por serie.

    Args:
        cards (list): Lista de cartas.

    Returns:
        dict: Diccionario con series como keys y listas de cartas como valores.
    """
    series_dict = {}

    for c in cards:
        serie = c["serie"]
        if serie not in series_dict:
            series_dict[serie] = []
        series_dict[serie].append(c)

    return series_dict


def generate_random_deck(series_dict: dict, distribution: dict) -> list:
    """Genera un mazo aleatorio cumpliendo la distribucion de series.

    Args:
        series_dict (dict): Diccionario de series con sus cartas.
        distribution (dict): Distribucion de cartas por serie, ejemplo {"platinum":1, "black":3}

    Returns:
        list: Mazo aleatorio como lista de cartas.
    """
    deck = []

    for serie, cantidad in distribution.items():
        if serie not in series_dict:
            print(f"Serie no encontrada en cartas: {serie}")
            continue

        cartas_serie = series_dict[serie]
        cantidad_real = min(cantidad, len(cartas_serie))
        seleccionadas = random.sample(cartas_serie, cantidad_real)

        deck.extend(seleccionadas)

    return deck


def robar_carta(ctx: dict, player: bool = True) -> None:
    """Roba la siguiente carta del mazo para el jugador o rival y actualiza el reverso.

    Args:
        ctx (dict): Contexto del juego con forms.
        player (bool, optional): True para jugador, False para rival. Defaults to True.
    """
    data = ctx["forms"]["combat"]

    if player:
        mazo = data["mazo_player"]
        idx = data["mazo_index_player"]

        if idx >= len(mazo):
            data["carta_player_actual"] = None
            data["mazo_reverso_player"] = None
            return

        carta = mazo[idx]
        data["carta_player_actual"] = carta
        data["mazo_index_player"] += 1

        siguiente = obtener_reverso_siguiente(mazo, data["mazo_index_player"])
        if siguiente:
            data["mazo_reverso_player"] = pg.transform.scale(
                pg.image.load(siguiente).convert_alpha(),
                (130, 180)
            )
        else:
            data["mazo_reverso_player"] = None

        robar_carta(ctx, player=False)

    else:
        mazo = data["mazo_rival"]
        idx = data["mazo_index_rival"]

        if idx >= len(mazo):
            data["carta_rival_actual"] = None
            data["mazo_reverso_rival"] = None
            return

        carta = mazo[idx]
        data["carta_rival_actual"] = carta
        data["mazo_index_rival"] += 1

        siguiente = obtener_reverso_siguiente(mazo, data["mazo_index_rival"])
        if siguiente:
            data["mazo_reverso_rival"] = pg.transform.scale(
                pg.image.load(siguiente).convert_alpha(),
                (130, 180)
            )
        else:
            data["mazo_reverso_rival"] = None


def load_rev(mazo: list):
    """Carga el reverso de la primera carta del mazo escalado a 130x180.

    Args:
        mazo (list): Lista de cartas.

    Returns:
        pg.Surface|None: Imagen escalada del reverso o None si mazo vacio.
    """
    if len(mazo) == 0: 
        return None
    return pg.transform.scale(
        pg.image.load(mazo[0]["ruta_reverso"]).convert_alpha(),
        (130, 180)
    )


def obtener_reverso_siguiente(mazo: list, index: int):
    """Devuelve la ruta de la imagen del reverso de la siguiente carta.

    Args:
        mazo (list): Lista de cartas.
        index (int): Indice de la siguiente carta.

    Returns:
        str|None: Ruta de la imagen del reverso o None si no quedan cartas.
    """
    if index >= len(mazo):
        return None
    return mazo[index]["ruta_reverso"]


def calculate_average_stats(deck: list) -> dict:
    """Calcula el promedio de HP, ATK y DEF de un mazo.

    Args:
        deck (list): Lista de cartas.

    Returns:
        dict: Promedios de stats {"hp": ..., "atk": ..., "def": ...}
    """
    if len(deck) == 0:
        return {"hp": 0, "atk": 0, "def": 0}

    get_hp  = lambda c: int(c["hp"])
    get_atk = lambda c: int(c["atk"])
    get_def = lambda c: int(c["def"])

    lista_hp  = [get_hp(carta) for carta in deck]
    lista_atk = [get_atk(carta) for carta in deck]
    lista_def = [get_def(carta) for carta in deck]

    n = len(deck)

    def sumar(lista):
        total = 0
        for x in lista:
            total += x
        return total

    return {
        "hp":  sumar(lista_hp * 15) // n,
        "atk": sumar(lista_atk) // n,
        "def": sumar(lista_def) // n
    }



def calcular_ataque_total(carta: dict) -> float:
    """Calcula el ataque total de una carta sumando su bonus.

    Args:
        carta (dict): Carta a evaluar.

    Returns:
        float: Valor total de ataque.
    """
    return int(carta["atk"]) + float(carta["bonus"])


def calcular_daño(carta: dict) -> int:
    """Calcula el daño total de una carta sumando hp, atk, def y bonus.

    Args:
        carta (dict): Carta a evaluar.

    Returns:
        int: Daño total como entero.
    """
    bonus = float(carta["bonus"])
    hp  = float(carta["hp"])  + bonus
    atk = float(carta["atk"]) + bonus
    defn = float(carta["def"]) + bonus
    total = hp + atk + defn

    return int(total)


def resolver_mano(ctx: dict) -> None:
    """Resuelve una ronda de combate entre jugador y rival, aplica daños y sfx.

    Args:
        ctx (dict): Contexto del juego con forms.
    """
    data = ctx["forms"]["combat"]
    carta_p = data["carta_player_actual"]
    carta_r = data["carta_rival_actual"]

    #añadir turno
    if data["carta_player_actual"] and data["carta_rival_actual"]:
        data["turno_actual"] += 1
    
    #si no hay carta
    if carta_p is None or carta_r is None:
        return

    atk_p = calcular_ataque_total(carta_p)
    atk_r = calcular_ataque_total(carta_r)

    #empate
    if atk_p == atk_r:
        return

    # Jugador pierde
    if atk_p < atk_r:
        #Shield
        if data.get("shield_activo", False):
            daño_reflejado = calcular_daño(carta_r)
            daño_reflejado -= int(data["stats_r"]["def"])
            daño_reflejado = max(1, daño_reflejado)
            data["stats_r"]["hp"] -= daño_reflejado
            data["stats_r"]["hp"] = max(0, data["stats_r"]["hp"])
            data["shield_activo"] = False
            so.play_sfx(var.SHIELD_BROKEN_SFX)
            agregar_puntaje(ctx, 500)
            return
        
        #no shield
        daño = calcular_daño(carta_p)
        daño -= int(data["stats_p"]["def"])
        daño = max(1, daño)
        data["stats_p"]["hp"] -= daño
        data["stats_p"]["hp"] = max(0, data["stats_p"]["hp"])
        so.play_sfx(var.HIT_SFX)

        hp_inicial = data.get("hp_inicial_player", data["stats_p"]["hp"])
        if not data.get("music_danger_on", False) and data["stats_p"]["hp"] < hp_inicial * 0.5:
            so.play_sfx(var.DANGER_SFX)
            so.play_music(ctx, var.MUSICA_LASTSTAND)
            data["music_danger_on"] = True
            agregar_puntaje(ctx, 500)
        return

    # Rival pierde
    else:
        daño = calcular_daño(carta_r)
        daño -= int(data["stats_r"]["def"])
        daño = max(1, daño)
        data["stats_r"]["hp"] -= daño
        data["stats_r"]["hp"] = max(0, data["stats_r"]["hp"])
        so.play_sfx(var.WIN_SFX)
        agregar_puntaje(ctx, 100)

def check_fin_partida(ctx: dict) -> bool:
    """Verifica si la partida ha terminado por tiempo, HP o cartas.

    Args:
        ctx (dict): Contexto del juego.

    Returns:
        bool: True si la partida termino, False en caso contrario.
    """
    data = ctx["forms"]["combat"]

    if data["timer_actual"] <= 0:
        hp_p = data["stats_p"]["hp"]
        hp_r = data["stats_r"]["hp"]

        if hp_p < hp_r:
            terminar_partida(ctx, ganador="rival")
            return True
        elif hp_r < hp_p:
            terminar_partida(ctx, ganador="player")
            agregar_puntaje(ctx, 1000)
            return True
        else:
            terminar_partida(ctx, ganador="empate")
            agregar_puntaje(ctx, 500)
            return True

    if data["stats_p"]["hp"] <= 0:
        terminar_partida(ctx, ganador="rival")
        return True

    if data["stats_r"]["hp"] <= 0:
        terminar_partida(ctx, ganador="player")
        agregar_puntaje(ctx, 1000)
        return True

    if data["mazo_index_player"] >= len(data["mazo_player"]):
        if data["stats_p"]["hp"] < data["stats_r"]["hp"]:
            terminar_partida(ctx, ganador="rival")
        else:
            terminar_partida(ctx, ganador="player")
            agregar_puntaje(ctx, 1000)
        return True

    return False


def terminar_partida(ctx: dict, ganador: str) -> bool:
    """Finaliza la partida, reproduce sfx y cambia al form de resultados.

    Args:
        ctx (dict): Contexto del juego.
        ganador (str): "player", "rival" o "empate".

    Returns:
        bool: Siempre True.
    """
    data = ctx["forms"]["combat"]
    
    if ganador == "player":
        #puntos por victoria
        max_turnos = 40
        turnos = data.get("turno_actual", 0)
        bonus = max(0, (max_turnos - turnos) * 100)
        agregar_puntaje(ctx, 1500 + bonus)
    else:
        data["victoria"] = False
        agregar_puntaje(ctx, 0)
    
    if ganador == "player":
        so.play_sfx(var.WIN_SFX)
    elif ganador == "rival":
        so.play_sfx(var.HIT_SFX)
    else:
        so.play_sfx(var.SHIELD_BROKEN_SFX)

    fc.cambiar_form(ctx, "results")
    return True


def iniciar_puntaje(ctx: dict):
    """Inicializa el puntaje en 0 al comenzar una partida.

    Args:
        ctx (dict): Contexto del juego.
    """
    data = ctx["forms"]["combat"]
    data["puntaje"] = 0


def agregar_puntaje(ctx: dict, puntos: int):
    """Suma puntos al puntaje actual.

    Args:
        ctx (dict): Contexto del juego.
        puntos (int): Puntos a agregar.
    """
    data = ctx["forms"]["combat"]
    if "puntaje" not in data:
        data["puntaje"] = 0
    data["puntaje"] += puntos

def activar_heal(ctx: dict) -> None:
    """Activa el comodín de curación del jugador.

    Suma un 25% de la vida inicial, sin superar la vida máxima.
    Marca el comodín como usado y oculta el botón correspondiente.

    Args:
        ctx (dict): Contexto del juego con forms.
    """
    data = ctx["forms"]["combat"]

    if data["heal_usado"]:
        return

    # Calcula nueva vida, sin superar la vida inicial
    nueva_hp = data["stats_p"]["hp"] + data["hp_inicial_player"] * 0.25
    data["stats_p"]["hp"] = min(nueva_hp, data["hp_inicial_player"])

    data["heal_usado"] = True
    data["accion"][1]["visible"] = False
    so.play_sfx(var.HEAL_SFX)

def activar_shield(ctx: dict) -> None:
    """Activa el comodín de shield del jugador.

    Marca el shield como activo, usado y oculta el botón correspondiente.

    Args:
        ctx (dict): Contexto del juego con forms.
    """
    data = ctx["forms"]["combat"]

    if data["shield_usado"]:
        return

    data["shield_activo"] = True
    data["shield_usado"] = True
    data["accion"][2]["visible"] = False
    so.play_sfx(var.SHIELD_SFX)
