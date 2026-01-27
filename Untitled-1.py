import arcade
import os
import math

# ================== 基本配置 ==================
BOARD_SIZE = 15  # 15x15 五子棋
ASSETS_DIR = "assets"

BOARD_IMAGE = os.path.join(ASSETS_DIR, "beijing.jpg")
BLACK_PIECE_IMAGE = os.path.join(ASSETS_DIR, "heizi.png")
WHITE_PIECE_IMAGE = os.path.join(ASSETS_DIR, "baizi.png")


class GomokuGame(arcade.Window):
    def __init__(self):
        # 读取棋盘背景，按图片像素开窗口（像素级对齐）
        texture = arcade.load_texture(BOARD_IMAGE)
        self.board_width = texture.width
        self.board_height = texture.height

        super().__init__(
            self.board_width,
            self.board_height,
            "五子棋"
        )

        # 背景精灵
        self.board_sprite = arcade.Sprite(BOARD_IMAGE)
        self.board_sprite.center_x = self.board_width / 2
        self.board_sprite.center_y = self.board_height / 2

        # 计算棋盘参数（自动适配图片）
        self.margin = 50
        self.cell_size = (self.board_width - 2 * self.margin) / (BOARD_SIZE - 1)

        # 棋子
        self.pieces = arcade.SpriteList()
        self.board_state = {}  # {(row, col): "black"/"white"}

        # 当前玩家
        self.current_player = "black"

        # 棋子缩放（按格子大小自动算）
        self.piece_scale = self.cell_size / 256 * 0.9

    def on_draw(self):
        arcade.start_render()
        self.board_sprite.draw()
        self.pieces.draw()

    # ================== 鼠标点击 ==================
    def on_mouse_press(self, x, y, button, modifiers):
        row, col = self.get_nearest_intersection(x, y)

        if row is None or col is None:
            return

        # 不允许重复落子
        if (row, col) in self.board_state:
            return

        px, py = self.grid_to_pixel(row, col)

        # 创建棋子
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

    # ================== 坐标转换 ==================
    def grid_to_pixel(self, row, col):
        x = self.margin + col * self.cell_size
        y = self.margin + row * self.cell_size
        return x, y

    def get_nearest_intersection(self, x, y):
        col = round((x - self.margin) / self.cell_size)
        row = round((y - self.margin) / self.cell_size)

        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return row, col
        return None, None


if __name__ == "__main__":
    game = GomokuGame()
    arcade.run()
