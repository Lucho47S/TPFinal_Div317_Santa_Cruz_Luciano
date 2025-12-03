import pygame as pg
import modules.variables as var
import modules.auxiliar as aux
import modules.forms.form_menu as fmenu
import modules.forms.form_game as fgame
import modules.forms.form_score as fscore
import modules.forms.form_options as foptions
import modules.forms.form_results as fresults
import modules.sonido as son

def cambiar_form(ctx: dict, nuevo_form: str) -> None:
    """Cambia el form actual del juego y ejecuta la inicializacion correspondiente,
    incluyendo la reproduccion de la musica de fondo.

    Args:
        ctx (dict): Diccionario de contexto del juego que contiene el estado actual.
        nuevo_form (str): Nombre del form al que se desea cambiar. Ejemplos: "menu", "juego", "score", etc.
    """
    ctx["form"] = nuevo_form

    match nuevo_form:
        case "menu":
            fmenu.iniciar(ctx)
            son.play_music(ctx, var.MUSICA_MENU)

        case "juego":
            fgame.iniciar(ctx)
            son.play_music(ctx, var.MUSICA_STAGE)

        case "score":
            fscore.iniciar(ctx)
            son.play_music(ctx, var.MUSICA_RANKING)

        case "options":
            foptions.iniciar(ctx)
            son.play_music(ctx, var.MUSICA_OPTIONS)
        
        case "results":
            fresults.iniciar(ctx)
            son.play_music(ctx, var.MUSICA_RESULTS)


def main() -> None:
    """Funcion principal del juego que inicializa pygame, el contexto de forms y ejecuta
    el bucle principal de contextos, actualizacion y dibujo del juego.

    Args:
        None
    """

    pg.init()
    pg.font.init()
    pg.mixer.init()
    pg.display.set_icon(var.GAME_ICON)
    screen = pg.display.set_mode((var.ASPECT_RATIO))
    clock = pg.time.Clock()

    ctx = {
        "screen": screen,
        "clock": clock,
        "form": "menu",

        "forms": {
            "menu": {...},
            "settings": {...},
            "game": {...},
            "pause": {...},
            "score": {...},
            "options": {...},
        }
    }

    cambiar_form(ctx, "menu")

    running = True
    while running:

        # Captura de contextos
        for i in pg.event.get():
            if i.type == pg.QUIT:
                running = False

            match ctx["form"]:
                case "menu":
                    fmenu.handle_event(ctx, i)
                case "juego":
                    fgame.handle_event(ctx, i)
                case "score":
                    fscore.handle_event(ctx, i)
                case "options":
                    foptions.handle_event(ctx, i)
                case "results":
                    fresults.handle_event(ctx, i)

        # Actualizacion del form actual
        match ctx["form"]:
            case "menu":
                fmenu.update(ctx)
            case "juego":
                fgame.update(ctx)
            case "score":
                fscore.update(ctx)
            case "options":
                foptions.update(ctx)
            case "results":
                fresults.update(ctx)

        # Dibujo del form actual
        match ctx["form"]:
            case "menu":
                fmenu.draw(ctx)
            case "juego":
                fgame.draw(ctx)
            case "score":
                fscore.draw(ctx)
            case "options":
                foptions.draw(ctx)
            case "results":
                fresults.draw(ctx)

        pg.display.flip()
        clock.tick(60)

    pg.quit()
