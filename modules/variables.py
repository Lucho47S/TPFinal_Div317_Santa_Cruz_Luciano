import pygame as pg
import modules.auxiliar as aux
########## Configs Juego ##########
ASPECT_RATIO = (1000, 600)
GAME_TITLE = 'Yu Gi Ball\nCard Trading Game'
FPS = 30
STAGE_TIMER = 200000
JSON_CARDS = 'modules/decks/cartas.json'
GAME_ICON = pg.image.load("assets/img/icons/pog.png")

########## Img Botones ##########
WISH_HEAL = "assets/img/buttons_image/heal.png"
WISH_SHIELD = "assets/img/buttons_image/shield.png"
PLAY_HAND = "assets/img/buttons_image/btn_play_hand.png"

########## Fuentes ##########
FONT_PATH = "assets/fonts/Saiyan-Sans.ttf"
ALT_FONT_PATH = "assets/fonts/alagard.ttf"

########## Fondos de formularios ##########
FONDO_MENU = "assets/img/forms/form_main_menu.png"
FONDO_SCORE = "assets/img/forms/form_ranking.png"
FONDO_OPTIONS = "assets/img/forms/form_options.png"
FONDO_STAGE = "assets/img/background_cards_simple.png"
FONDO_NAME = "assets/img/forms/form_stage_select.png"
FONDO_VICTORIA = "assets/img/forms/form_enter_name_1.png"
FONDO_DERROTA = "assets/img/forms/form_enter_name_0.png"

########## Archivos ##########
RANKING_CSV = 'puntajes.csv'

COLORS = {
    "grey": (70,70,70),
    "white": (255, 255, 255),
    "red": (150,50,50),
    "hover": (219, 135, 70),
    "bg": (79, 28, 8),
}

DISTRIBUCION_MAZO = {
    "platinum": 1,
    "black": 2,
    "golden": 1,

    "silver": 3,
    "purple": 4,
    "red": 6,

    "blue": 8,
    "green": 15
}

########## Rutas Musica ##########
MUSICA_RANKING = 'assets/audio/music/ost_ranked.ogg'
MUSICA_MENU = 'assets/audio/music/ost_main_menu.ogg'
MUSICA_OPTIONS = 'assets/audio/music/ost_options.ogg'
MUSICA_PAUSE = 'assets/audio/music/ost_main_menu.ogg'
MUSICA_STAGE = 'assets/audio/music/ost_battle_music.ogg'
MUSICA_LASTSTAND = 'assets/audio/music/ost_last_stand.ogg'
MUSICA_RESULTS = 'assets/audio/music/ost_results.ogg'

########## Rutas SFX ##########
HEAL_SFX = "assets/audio/sounds/heal_activated.ogg"
HIT_SFX = "assets/audio/sounds/hit_01.ogg"
CLICK_SFX = "assets/audio/sounds/click_scouter.ogg"
DANGER_SFX = "assets/audio/sounds/ssj_effect.ogg"
WIN_SFX = "assets/audio/sounds/item.mp3"
SHIELD_SFX = "assets/audio/sounds/shield_activated.ogg"
SHIELD_BROKEN_SFX = "assets/audio/sounds/shield_deactivated.ogg"