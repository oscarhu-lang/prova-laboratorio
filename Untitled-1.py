import arcade
import os
import math

BOARD_SIZE = 15
ASSETS_DIR = "assets"

BLACK_PIECE_IMAGE = os.path.join(ASSETS_DIR, "black_stone.png")
WHITE_PIECE_IMAGE = os.path.join(ASSETS_DIR, "white_stone.png")


class GomokuGame(arcade.Window):
    def __init__(self):
        super().__init__(600, 600, "Wuziqi")

        self.margin = 50
        self.cell_size = (600 - 2 * self.margin) / (BOARD_SIZE - 1)

        self.pieces = arcade.SpriteList()
        self.board_state = {}
        self.current_player = "black"

        self.piece_scale = self.cell_size / 256 * 0.9
        arcade.set_background_color(arcade.color.BISQUE)

    def on_draw(self):
        self.clear()

        # griglia
        for i in range(BOARD_SIZE):
            x = self.margin + i * self.cell_size
            y = self.margin + i * self.cell_size

            arcade.draw_line(self.margin, y, 600 - self.margin, y, arcade.color.BLACK, 1)
            arcade.draw_line(x, self.margin, x, 600 - self.margin, arcade.color.BLACK, 1)

        self.pieces.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        row, col = self.get_nearest_intersection(x, y)

        if row is None or (row, col) in self.board_state:
            return

        px, py = self.grid_to_pixel(row, col)

        if self.current_player == "black":
            piece = arcade.Sprite(BLACK_PIECE_IMAGE, self.piece_scale)
            self.board_state[(row, col)] = "black"
            self.current_player = "white"
        else:
            piece = arcade.Sprite(WHITE_PIECE_IMAGE, self.piece_scale)
            self.board_state[(row, col)] = "white"
            self.current_player = "black"

        piece.center_x = px
        piece.center_y = py
        self.pieces.append(piece)

    def grid_to_pixel(self, row, col):
        return (
            self.margin + col * self.cell_size,
            self.margin + row * self.cell_size
        )

    def get_nearest_intersection(self, x, y):
        col = round((x - self.margin) / self.cell_size)
        row = round((y - self.margin) / self.cell_size)

        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return row, col
        return None, None


if __name__ == "__main__":
    game = GomokuGame()
    arcade.run()
