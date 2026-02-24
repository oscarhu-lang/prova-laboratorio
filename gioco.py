import arcade
import random
import math
# 测试修改：这是我的第一次改动
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Babbo Natale"

DISTANZA_MINIMA = 100


class BabboNatale(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.babbo = None
        self.lista_babbo = arcade.SpriteList()
        self.lista_cookie = arcade.SpriteList()

        self.sfondo = arcade.load_texture("cookie.png")
        self.suono_munch = arcade.load_sound("munch.mp3")
        self.audio_attivo = True

        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        self.velocita = 4

        self.biscotti_mangiati = 0
        self.cookie_per_volta = 1

        self.setup()

    def setup(self):
        self.babbo = arcade.Sprite("cookie.png")
        self.babbo.center_x = 300
        self.babbo.center_y = 100
        self.lista_babbo.append(self.babbo)

        self.crea_cookie()

    def distanza_da_babbo(self, x, y):
        return math.dist((x, y), (self.babbo.center_x, self.babbo.center_y))

    def crea_cookie(self):
        for _ in range(self.cookie_per_volta):
            cookie = arcade.Sprite(".cookie.png", scale=0.2)

            while True:
                x = random.randint(50, SCREEN_WIDTH - 50)
                y = random.randint(50, SCREEN_HEIGHT - 50)
                if self.distanza_da_babbo(x, y) >= DISTANZA_MINIMA:
                    break

            cookie.center_x = x
            cookie.center_y = y
            self.lista_cookie.append(cookie)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            self.sfondo
        )

        self.lista_cookie.draw()
        self.lista_babbo.draw()

        arcade.draw_text(
            f"Biscotti: {self.biscotti_mangiati}",
            10,
            SCREEN_HEIGHT - 30,
            arcade.color.WHITE,
            20
        )

    def on_update(self, delta_time):
        change_x = 0
        change_y = 0

        if self.up_pressed:
            change_y += self.velocita
        if self.down_pressed:
            change_y -= self.velocita
        if self.left_pressed:
            change_x -= self.velocita
        if self.right_pressed:
            change_x += self.velocita

        self.babbo.center_x += change_x
        self.babbo.center_y += change_y

        self.babbo.center_x = max(0, min(self.width, self.babbo.center_x))
        self.babbo.center_y = max(0, min(self.height, self.babbo.center_y))

        collisioni = arcade.check_for_collision_with_list(
            self.babbo, self.lista_cookie
        )

        if collisioni:
            if self.audio_attivo:
                arcade.play_sound(self.suono_munch)

            for cookie in collisioni:
                cookie.remove_from_sprite_lists()
                self.biscotti_mangiati += 1

            if self.biscotti_mangiati % 5 == 0:
                self.cookie_per_volta += 1

            self.crea_cookie()

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.W):
            self.up_pressed = True
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = True
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = True
        elif key == arcade.key.M:
            self.audio_attivo = not self.audio_attivo

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.W):
            self.up_pressed = False
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = False
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = False
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = False


def main():
    gioco = BabboNatale()
    arcade.run()


if __name__ == "__main__":
    main()

