import pygame as pg

def init_audio_state(ctx: dict) -> None:
    """Inicializa la seccion de audio en el contexto si no existe.

    Crea ctx['audio'] con las claves:
        - enabled (bool): si el audio esta activo.
        - volume (float): volumen de 0.0 a 1.0.
        - current_music (str | None): ruta de la musica actualmente reproducida.

    Args:
        ctx (dict): Contexto general del juego.

    Returns:
        None
    """
    if "audio" not in ctx:
        ctx["audio"] = {
            "enabled": True,
            "volume": 0.5,
            "current_music": None
        }


def play_music(ctx: dict, path: str, volume: float = 0.3, loop: int = -1) -> None:
    """Reproduce musica de fondo usando el estado de audio del contexto.

    Si la musica ya se estaba reproduciendo, ajusta el volumen sin recargarla.

    Args:
        ctx (dict): Contexto general del juego.
        path (str): Ruta del archivo de musica a reproducir.
        volume (float, optional): Nuevo volumen de 0.0 a 1.0. Si es None, se mantiene el actual.
        loop (int, optional): Numero de repeticiones (-1 para loop infinito). Por defecto -1.

    Returns:
        None
    """
    init_audio_state(ctx)
    audio = ctx["audio"]

    if not audio["enabled"]:
        return

    if volume is not None:
        audio["volume"] = volume

    if audio["current_music"] == path:
        pg.mixer.music.set_volume(audio["volume"])
        return

    pg.mixer.music.load(path)
    pg.mixer.music.set_volume(audio["volume"])
    pg.mixer.music.play(loop)
    audio["current_music"] = path


def stop_music(ctx: dict) -> None:
    """Detiene la musica actual y marca el estado de audio como sin musica cargada.

    Args:
        ctx (dict): Contexto general del juego.

    Returns:
        None
    """
    init_audio_state(ctx)
    pg.mixer.music.stop()
    ctx["audio"]["current_music"] = None


def set_music_volume(ctx: dict, vol: float) -> None:
    """Establece el volumen de la musica de fondo en rango 0.0 – 1.0.

    Args:
        ctx (dict): Contexto general del juego.
        vol (float): Volumen deseado de 0.0 a 1.0.

    Returns:
        None
    """
    init_audio_state(ctx)
    ctx["audio"]["volume"] = vol
    pg.mixer.music.set_volume(vol)


def music_on(ctx: dict) -> None:
    """Activa el audio y reproduce la musica previamente cargada si existe.

    Args:
        ctx (dict): Contexto general del juego.

    Returns:
        None
    """
    init_audio_state(ctx)
    ctx["audio"]["enabled"] = True

    if ctx["audio"]["current_music"]:
        pg.mixer.music.set_volume(ctx["audio"]["volume"])
        pg.mixer.music.play(-1)


def music_off(ctx: dict) -> None:
    """Desactiva el audio y detiene la musica de fondo.

    Args:
        ctx (dict): Contexto general del juego.

    Returns:
        None
    """
    init_audio_state(ctx)
    ctx["audio"]["enabled"] = False
    pg.mixer.music.stop()


def get_volume_0_100(ctx: dict) -> int:
    """Devuelve el volumen actual de la musica en escala 0 a 100.

    Args:
        ctx (dict): Contexto general del juego.

    Returns:
        int: Volumen actual en porcentaje (0–100).
    """
    init_audio_state(ctx)
    return int(ctx["audio"]["volume"] * 100)


def set_volume_0_100(ctx: dict, vol: int) -> None:
    """Establece el volumen de la musica usando una escala de 0 a 100.

    Args:
        ctx (dict): Contexto general del juego.
        vol (int): Volumen deseado (recortado a 1–100).

    Returns:
        None
    """
    if vol < 1:
        vol = 1
    if vol > 100:
        vol = 100
    set_music_volume(ctx, vol / 100)


def play_sfx(path: str, volume: float = 1.0) -> None:
    """Reproduce un efecto de sonido sin usar caché ni manejo de errores.

    Args:
        path (str): Ruta del archivo de efecto de sonido.
        volume (float, optional): Volumen de 0.0 a 1.0. Por defecto 1.0.

    Returns:
        None
    """
    sound = pg.mixer.Sound(path)
    sound.set_volume(0.2)
    sound.play()
