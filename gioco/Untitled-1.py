import arcade
import os

SCREEN_WIDTH = 1248
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Pixel Adventure - Golden Coins!"

TILE_SIZE = 68
MOVE_SPEED = 6


class SpriteAnimato(arcade.Sprite):
    def __init__(self, scala: float = 1.0):
        super().__init__(scale=scala)
        self.animazioni = {}
        self.animazione_corrente = None
        self.animazione_default = None
        self.tempo_frame = 0.0
        self.indice_frame = 0

    def aggiungi_animazione(
        self,
        nome: str,
        percorso: str,
        frame_width: int,
        frame_height: int,
        num_frame: int,
        colonne: int,
        durata: float,
        loop: bool = True,
        default: bool = False,
        riga: int = 0,
    ):
        sheet = arcade.load_spritesheet(percorso)
        offset = riga * colonne
        tutti = sheet.get_texture_grid(
            size=(frame_width, frame_height),
            columns=colonne,
            count=offset + num_frame,
        )
        self._registra(nome, tutti[offset:], durata, loop, default)

    def _registra(self, nome, textures, durata, loop, default=False):
        self.animazioni[nome] = {
            "textures": textures,
            "durata_frame": durata / len(textures),
            "loop": loop,
        }
        if default or self.animazione_default is None:
            self.animazione_default = nome
        if self.animazione_corrente is None:
            self._vai(nome)

    def imposta_animazione(self, nome: str):
        if nome != self.animazione_corrente:
            self._vai(nome)

    def _vai(self, nome: str):
        self.animazione_corrente = nome
        self.indice_frame = 0
        self.tempo_frame = 0.0
        self.texture = self.animazioni[nome]["textures"][0]

    def update_animation(self, delta_time: float = 1 / 60):
        anim = self.animazioni[self.animazione_corrente]
        self.tempo_frame += delta_time
        if self.tempo_frame < anim["durata_frame"]:
            return
        self.tempo_frame -= anim["durata_frame"]
        prossimo = self.indice_frame + 1
        if prossimo < len(anim["textures"]):
            self.indice_frame = prossimo
        elif anim["loop"]:
            self.indice_frame = 0
        else:
            self._vai(self.animazione_default)
            return
        self.texture = anim["textures"][self.indice_frame]


GAME_MAP = [
   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 1, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 0, 0, 0, 3, 3, 1, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 3, 3, 3, 0, 0, 0, 3, 3, 3, 3, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 4, 1, 1, 4, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 3, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 3, 3, 3, 0, 3, 3, 3, 1, 3, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 3, 3, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 3, 3, 3, 3, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 4, 1, 1, 4, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 4, 1],
    [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 3, 3, 3, 3, 3, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 3, 1, 3, 1, 3, 0, 1, 1, 0, 0, 0, 0, 0, 0, 4, 1],
    [1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 3, 1, 3, 1, 3, 0, 1, 1, 0, 0, 0, 0, 0, 0, 4, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 3, 3, 3, 3, 3, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 4, 1, 1, 0, 1, 1, 4, 1, 0, 1, 0, 1, 4, 1, 1, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 4, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 4, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    [1, 4, 1, 1, 0, 1, 1, 4, 1, 1, 4, 1, 1, 0, 1, 1, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    [1, 0, 3, 3, 3, 3, 3, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1],
    [1, 0, 3, 1, 3, 1, 3, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 3, 3, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
    [1, 0, 3, 1, 3, 1, 3, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 4, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 3, 3, 3, 3, 3, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4, 1, 4, 1, 4, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

class Coin(SpriteAnimato):
    def __init__(self, x, y):
        super().__init__(scala=1.0)
        self.center_x = x
        self.center_y = y
        self.aggiungi_animazione(
            nome="spin",
            percorso="../foto/coin.png",
            frame_width=32,
            frame_height=30,
            num_frame=8,
            colonne=8,
            durata=0.8,
            loop=True,
            default=True
        )
    def update_animation(self, delta_time=1/60):
        super().update_animation(delta_time)


class Chest(SpriteAnimato):
    def __init__(self, x, y):
        super().__init__(scala=1.0)
        self.center_x = x
        self.center_y = y
        self.is_opened = False
        self.aggiungi_animazione(
            nome="closed",
            percorso="foto/TX Props with Shadow.png",
            frame_width=64,
            frame_height=64,
            num_frame=1,
            colonne=1,
            durata=1.0,
            loop=False,
            default=True
        )
        self.aggiungi_animazione(
            nome="opening",
            percorso="foto/TX Props with Shadow.png",
            frame_width=64,
            frame_height=64,
            num_frame=4,
            colonne=4,
            durata=0.5,
            loop=False
        )

    def open(self):
        if not self.is_opened:
            self.is_opened = True
            self.imposta_animazione("opening")
            print("宝箱被打开！获得奖励！")
            return True
        return False

    def update_animation(self, delta_time=1/60):
        super().update_animation(delta_time)


class Player(SpriteAnimato):
    def __init__(self, start_grid_x, start_grid_y):
        super().__init__(scala=1.0)
        self.grid_x = start_grid_x
        self.grid_y = start_grid_y
        self.center_x = start_grid_x * TILE_SIZE + TILE_SIZE // 2
        self.center_y = self.convert_grid_y(start_grid_y) * TILE_SIZE + TILE_SIZE // 2
        self.target_x = self.center_x
        self.target_y = self.center_y
        self.is_moving = False
        self.direction = "down"

        self.aggiungi_animazione("idle_down", "../foto/idle_down.png", 96, 80, 8, 8, 1.0, True, True)
        self.aggiungi_animazione("idle_up", "../foto/idle_up.png", 96, 80, 8, 8, 1.0)
        self.aggiungi_animazione("idle_left", "../foto/idle_left.png", 96, 80, 8, 8, 1.0)
        self.aggiungi_animazione("idle_right", "../foto/idle_right.png", 96, 80, 8, 8, 1.0)

        self.aggiungi_animazione("run_down", "../foto/run_down.png", 96, 80, 8, 8, 1.0)
        self.aggiungi_animazione("run_up", "../foto/run_up.png", 96, 80, 8, 8, 1.0)
        self.aggiungi_animazione("run_left", "../foto/run_left.png", 96, 80, 8, 8, 1.0)
        self.aggiungi_animazione("run_right", "../foto/run_right.png", 96, 80, 8, 8, 1.0)

    def convert_grid_y(self, grid_y):
        return len(GAME_MAP) - 1 - grid_y

    def move(self, dx, dy, direction):
        if self.is_moving:
            return
        self.direction = direction
        new_grid_x = self.grid_x + dx
        new_grid_y = self.grid_y + dy
        if 0 <= new_grid_y < len(GAME_MAP) and 0 <= new_grid_x < len(GAME_MAP[0]):
            if GAME_MAP[new_grid_y][new_grid_x] != 1:
                self.grid_x = new_grid_x
                self.grid_y = new_grid_y
                self.target_x = new_grid_x * TILE_SIZE + TILE_SIZE // 2
                self.target_y = self.convert_grid_y(new_grid_y) * TILE_SIZE + TILE_SIZE // 2
                self.is_moving = True

    def update(self, delta_time):
        if self.is_moving:
            if self.center_x < self.target_x:
                self.center_x = min(self.center_x + MOVE_SPEED, self.target_x)
            elif self.center_x > self.target_x:
                self.center_x = max(self.center_x - MOVE_SPEED, self.target_x)
            if self.center_y < self.target_y:
                self.center_y = min(self.center_y + MOVE_SPEED, self.target_y)
            elif self.center_y > self.target_y:
                self.center_y = max(self.center_y - MOVE_SPEED, self.target_y)
            if self.center_x == self.target_x and self.center_y == self.target_y:
                self.is_moving = False
            self.imposta_animazione(f"run_{self.direction}")
        else:
            self.imposta_animazione(f"idle_{self.direction}")

    def update_animation(self, delta_time=1/60):
        super().update_animation(delta_time)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player_list = None
        self.wall_list = None
        self.floor_list = None
        self.goal_list = None
        self.coin_list = None
        self.chest_list = None
        self.player = None
        self.camera : arcade.Camera2D = None
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.tile_texture = None
        self.floor_texture = None
        self.goal_texture = None
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.floor_list = arcade.SpriteList(use_spatial_hash=True)
        self.goal_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList()
        
        try:
            self.tile_texture = arcade.load_texture("../foto/unnamed.jpg")
        except FileNotFoundError:
            self.tile_texture = arcade.make_soft_square_texture(TILE_SIZE, arcade.color.GRAY, outer_alpha=255)
        self.floor_texture = arcade.make_soft_square_texture(TILE_SIZE, arcade.color.DARK_SLATE_GRAY, outer_alpha=255)
        self.goal_texture = arcade.make_soft_square_texture(TILE_SIZE, arcade.color.CYAN, outer_alpha=255)
        
        self.create_map()
        self.player = Player(13, 3)
        self.player_list.append(self.player)
        self.camera = arcade.Camera2D()
    
    def create_map(self):
        map_height = len(GAME_MAP)
        for row_idx, row in enumerate(GAME_MAP):
            for col_idx, cell in enumerate(row):
                x = col_idx * TILE_SIZE + TILE_SIZE // 2
                y = (map_height - 1 - row_idx) * TILE_SIZE + TILE_SIZE // 2
                if cell == 1:
                    wall = arcade.Sprite()
                    wall.texture = self.tile_texture
                    wall.width = TILE_SIZE
                    wall.height = TILE_SIZE
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)
                elif cell == 2:
                    goal = arcade.Sprite()
                    goal.texture = self.goal_texture
                    goal.width = TILE_SIZE
                    goal.height = TILE_SIZE
                    goal.center_x = x
                    goal.center_y = y
                    self.goal_list.append(goal)
                elif cell == 3:
                    coin = Coin(x, y)
                    self.coin_list.append(coin)
    
    def on_draw(self):
        self.clear()
        self.camera.use()
        self.floor_list.draw()
        self.goal_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()
    
    def center_camera_to_player(self):
        map_width_px = len(GAME_MAP[0]) * TILE_SIZE
        map_height_px = len(GAME_MAP) * TILE_SIZE
        cam_x = self.player.center_x - SCREEN_WIDTH / 2
        cam_y = self.player.center_y - SCREEN_HEIGHT / 2
        cam_x = max(0, min(cam_x, map_width_px - SCREEN_WIDTH))
        cam_y = max(0, min(cam_y, map_height_px - SCREEN_HEIGHT))
        self.camera.position = (cam_x, cam_y)
    
    def on_update(self, delta_time):
        if not self.player.is_moving:
            if self.up_pressed:
                self.player.move(0, -1, 'up')
            elif self.down_pressed:
                self.player.move(0, 1, 'down')
            elif self.left_pressed:
                self.player.move(-1, 0, 'left')
            elif self.right_pressed:
                self.player.move(1, 0, 'right')
        
        self.player.update(delta_time)  
        self.coin_list.update_animation(delta_time)  
        
        collided_coins = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in collided_coins:
            coin.remove_from_sprite_lists()
            # 可以在这里加音效 arcade.play_sound(...)
            
        self.center_camera_to_player()
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.ESCAPE:
            arcade.close_window()
    
    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.right_pressed = False


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game = GameView()
    game.setup()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()