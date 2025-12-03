import pygame as pg
import modules.variables as var
import modules.sonido as so
import os

def create_label(text: str, font: pg.font.Font, color: tuple, x: int, y: int) -> dict:
    """Crea una label con el texto y color dados en las coordenadas indicadas.

    Args:
        text (str): Texto que mostrará la label.
        font (pg.font.Font): Fuente utilizada para renderizar el texto.
        color (tuple): Color del texto (R, G, B).
        x (int): Posicion horizontal de la label.
        y (int): Posicion vertical de la label.

    Returns:
        dict: Diccionario que representa la label, con su superficie, rect, texto y fuente.
    """
    surf = font.render(text, True, color)
    rect = surf.get_rect(topleft=(x, y))

    return {
        "type": "label",
        "text": text,
        "surface": surf,
        "rect": rect,
        "color": color,
        "font": font,
    }


def draw_label(screen: pg.Surface, label: dict) -> None:
    """Dibuja la label en la pantalla.

    Args:
        screen (pg.Surface): Superficie donde dibujar la label.
        label (dict): Label a dibujar.
    """
    label["surface"] = label["font"].render(label["text"], True, label["color"])
    screen.blit(label["surface"], label["rect"])


def update_label(label: dict, texto: str) -> None:
    """Actualiza el texto de una label y su superficie.

    Args:
        label (dict): Label a actualizar.
        texto (str): Nuevo texto
    """
    label["text"] = texto
    label["surface"] = label["font"].render(label["text"], True, label["color"])



def create_button(text: str, font: pg.font.Font, txt_color: tuple, bg_color: tuple, x: int, y: int, w: int, h: int, hover_color: tuple) -> dict:
    """Crea un boton con texto y colores dados

    Args:
        text (str): Texto del boton.
        font (pg.font.Font): Fuente del texto.
        txt_color (tuple): Color del texto.
        bg_color (tuple): Color de fondo normal.
        x (int): Posicion horizontal.
        y (int): Posicion vertical.
        w (int): Ancho del boton.
        h (int): Alto del boton.
        hover_color (tuple): Color de fondo al pasar el mouse.

    Returns:
        dict: Diccionario que representa el boton
    """
    rect = pg.Rect(x, y, w, h)
    surf_text = font.render(text, True, txt_color)
    text_rect = surf_text.get_rect(center=rect.center)

    return {
        "type": "button",
        "rect": rect,
        "text": text,
        "text_surface": surf_text,
        "text_rect": text_rect,
        "bg_color": bg_color,
        "hover_color": hover_color,
        "current_color": bg_color,
        "text_color": txt_color,
    }


def update_button_hover(button: dict, mouse_pos: tuple) -> None:
    """Actualiza el color del boton si el mouse está sobre él.

    Args:
        button (dict): boton a actualizar.
        mouse_pos (tuple): Posicion actual del mouse.
    """
    if button["rect"].collidepoint(mouse_pos):
        button["current_color"] = button["hover_color"]
    else:
        button["current_color"] = button["bg_color"]


def draw_button(screen: pg.Surface, button: dict):
    """Dibuja un boton en la pantalla.

    Args:
        screen (pg.Surface): Superficie donde dibujar el boton.
        button (dict): boton a dibujar.
    """
    pg.draw.rect(screen, button["current_color"], button["rect"], border_radius=10)
    screen.blit(button["text_surface"], button["text_rect"])


def button_is_clicked(button: dict, mouse_pos: tuple, mouse_pressed: tuple) -> bool:
    """Devuelve True si el boton fue clickeado.

    Args:
        button (dict): boton a verificar.
        mouse_pos (tuple): Posicion del mouse.
        mouse_pressed (tuple): Estado de los botones del mouse.

    Returns:
        bool: True si fue clickeado, False en caso contrario.
    """
    if button["rect"].collidepoint(mouse_pos) and mouse_pressed[0]:
        so.play_sfx(var.CLICK_SFX)
        return True
    return False


def create_image_button(img_path: str, x: int, y: int, w: int, h: int) -> dict:
    """Crea un boton basado en imagen escalada.

    Args:
        img_path (str): Ruta de la imagen.
        x (int): posicion horizontal.
        y (int): posicion vertical.
        w (int): Ancho de la imagen.
        h (int): Alto de la imagen.

    Returns:
        dict: Diccionario que representa el boton de imagen
    """
    image = pg.image.load(img_path)
    image = pg.transform.scale(image, (w, h))
    rect = image.get_rect(topleft=(x, y))

    return {
        "type": "image_button",
        "image": image,
        "rect": rect
    }


def draw_image_button(screen: pg.Surface, button: dict) -> None:
    """Dibuja un boton de imagen en la pantalla

    Args:
        screen (pg.Surface): Superficie donde dibujar
        button (dict): Boton de imagen a dibujar
    """
    screen.blit(button["image"], button["rect"])



def image_button_is_clicked(button: dict, mouse_pos: tuple, mouse_press: tuple) -> bool:
    """Verifica si el boton de imagen fue clickeado

    Args:
        button (dict): Boton de imagen a verificar.
        mouse_pos (tuple): Posicion del mouse.
        mouse_press (tuple): Estado de los botones del mouse.

    Returns:
        bool: True si fue clickeado, False en caso contrario.
    """
    if button["rect"].collidepoint(mouse_pos) and mouse_press[0]:
        return True
    return False


def read_scores_csv(path: str) -> list:
    """Lee un CSV de puntajes y devuelve una lista de tuplas (nombre, puntaje).

    Args:
        path (str): Ruta del archivo CSV.

    Returns:
        list: Lista de tuplas (nombre:str, puntaje:int)
    """
    lista = []
    archivo = open(path, "r", encoding="utf-8")

    for linea in archivo:
        linea = linea.strip()  # limpia saltos de linea
        if linea != "":
            partes = linea.split(",")

            nombre = partes[0].strip()
            puntaje_str = partes[1].strip()

            puntaje = 0
            es_numero = True

            for c in puntaje_str:
                if c < "0" or c > "9":
                    es_numero = False
                    break

            if es_numero:
                puntaje = int(puntaje_str)

            lista.append((nombre, puntaje))

    archivo.close()
    return lista



def selection_sort_scores(lista: list) -> list:
    """Ordena la lista de tuplas (nombre, puntaje) por puntaje descendente usando Selection Sort.

    Args:
        lista (list): Lista de tuplas (nombre, puntaje).

    Returns:
        list: Lista ordenada por puntaje descendente.
    """
    n = len(lista)

    for i in range(n - 1):
        max_index = i
        for j in range(i + 1, n):
            if lista[j][1] > lista[max_index][1]:
                max_index = j
        # swap
        temp = lista[i]
        lista[i] = lista[max_index]
        lista[max_index] = temp

    return lista

def guardar_puntaje_csv(path: str, nombre: str, puntaje: int) -> None:
    """Agrega un nuevo puntaje al CSV, creando el archivo si no existe.

    Args:
        path (str): Ruta del archivo CSV.
        nombre (str): Nombre del jugador.
        puntaje (int): Puntaje obtenido.
    """
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("Nombre,Puntaje\n")

    with open(path, "a", encoding="utf-8") as f:
        f.write(f"{nombre},{puntaje}\n")


def nombre_valido(nombre: str) -> bool:
    """Devuelve True si el nombre contiene solo letras y espacios y no está vacio.

    Args:
        nombre (str): Nombre a validar.

    Returns:
        bool: True si es valido, False en caso contrario.
    """
    nombre = nombre.strip()
    if not nombre:
        return False

    for c in nombre:
        if not (c.isalpha() or c == " "):
            return False
    return True