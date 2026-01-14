import arcade
import os
# from arcade import *

class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.sprite = None
        self.playerSpriteList = arcade.SpriteList()

        self.setup()

    def setup(self):
        
        self.sprite = arcade.Sprite("qipang.jpg")

        self.sprite.center_x = 300
        self.sprite.center_y = 300
        self.sprite.scale_x = 0.43
        self.sprite.scale_y = 0.43

        self.playerSpriteList.append(self.sprite)

        

    def on_draw(self):
        self.playerSpriteList.draw()
        
    def on_update(self, deltaTime):
        self.sprite.center_x += 0




def main():
    game = MyGame(
        600, 600, "Il mio giochino"
    )
    arcade.run()


if __name__ == "__main__":
    main()