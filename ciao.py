import arcade
import os

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
SCREEN_TITLE = "Pixel Adventure"
TILE_SIZE = 32
MOVE_SPEED = 4

class Player:
    def __init__(self, start_x, start_y):
        self.grid_x = start_x
        self.grid_y = start_y
        self.pixel_x = start_x * TILE_SIZE + TILE_SIZE // 2
        self.pixel_y = start_y * TILE_SIZE + TILE_SIZE // 2
        self.target_px = self.pixel_x
        self.target_py = self.pixel_y
        self.is_moving = False
        self.direction = 'down'
        self.anim_idx = 0.0
        
        self.animations = {
            'run_up': self.load_textures('foto/run_up.png'),
            'run_down': self.load_textures('foto/run_down.png'),
            'run_left': self.load_textures('foto/run_left.png'),
            'run_right': self.load_textures('foto/run_right.png'),
            'idle_down': self.load_textures('foto/idle_down.png')
        }

    def load_textures(self, filename, frames=8):
        if not os.path.exists(filename):
            return [arcade.make_soft_circle_texture(TILE_SIZE, arcade.color.GRAY)] * frames
        
        sheet = arcade.load_spritesheet(filename)
        return sheet.get_texture_grid(size=(TILE_SIZE, TILE_SIZE), columns=frames, count=frames)

    def move(self, dx, dy, direction, game_map):
        if self.is_moving:
            return
        self.direction = direction
        nx, ny = self.grid_x + dx, self.grid_y + dy
        if 0 <= ny < len(game_map) and 0 <= nx < len(game_map[0]):
            if game_map[ny][nx] != 1:
                self.grid_x, self.grid_y = nx, ny
                self.target_px = nx * TILE_SIZE + TILE_SIZE // 2
                self.target_py = ny * TILE_SIZE + TILE_SIZE // 2
                self.is_moving = True

    def update(self):
        if self.is_moving:
            if self.pixel_x < self.target_px: self.pixel_x += MOVE_SPEED
            elif self.pixel_x > self.target_px: self.pixel_x -= MOVE_SPEED
            if self.pixel_y < self.target_py: self.pixel_y += MOVE_SPEED
            elif self.pixel_y > self.target_py: self.pixel_y -= MOVE_SPEED
            
            if self.pixel_x == self.target_px and self.pixel_y == self.target_py:
                self.is_moving = False
            self.anim_idx += 0.2
        else:
            self.anim_idx += 0.02
        if self.anim_idx >= 8:
            self.anim_idx = 0

    def draw(self):
        state = f"run_{self.direction}" if self.is_moving else "idle_down"
        texture = self.animations[state][int(self.anim_idx)]
        arcade.draw_texture_rect(texture, arcade.Rect(self.pixel_x - TILE_SIZE//2, self.pixel_y - TILE_SIZE//2, TILE_SIZE, TILE_SIZE))

class MyGame(arcade.Window):
    def __init__(self, game_map):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.game_map = game_map
        self.player = Player(13, 3)
        
        # Arcade 3.0 的新摄像机写法
        self.camera = arcade.camera.Camera2D()
        
        try:
            self.tile_texture = arcade.load_texture("foto/unnamed.jpg")
        except:
            self.tile_texture = None

    def on_draw(self):
        self.clear()
        
        # 使用摄像机
        self.camera.use()
        
        for r_idx, row in enumerate(self.game_map):
            for c_idx, cell in enumerate(row):
                x = c_idx * TILE_SIZE + TILE_SIZE // 2
                y = (len(self.game_map) - r_idx) * TILE_SIZE - TILE_SIZE // 2
                
                rect = arcade.Rect(x - TILE_SIZE//2, y - TILE_SIZE//2, TILE_SIZE, TILE_SIZE)
                
                if cell == 1:
                    if self.tile_texture:
                        arcade.draw_texture_rect(self.tile_texture, rect)
                    else:
                        arcade.draw_rect_filled(rect, arcade.color.GRAY)
                elif cell == 2:
                    arcade.draw_rect_filled(rect, arcade.color.AQUAMARINE)
        
        self.player.draw()

    def on_update(self, delta_time):
        self.player.update()
        
        # Arcade 3.0 设置摄像机位置 (中心点)
        cam_x = self.player.pixel_x
        cam_y = self.player.pixel_y
        
        # 限制摄像机边界
        map_w = len(self.game_map[0]) * TILE_SIZE
        map_h = len(self.game_map) * TILE_SIZE
        
        half_w = SCREEN_WIDTH / 2
        half_h = SCREEN_HEIGHT / 2
        
        cam_x = max(half_w, min(cam_x, map_w - half_w))
        cam_y = max(half_h, min(cam_y, map_h - half_h))
        
        self.camera.position = (cam_x, cam_y)

    def on_key_press(self, key, modifiers):
        if not self.player.is_moving:
            if key == arcade.key.W: self.player.move(0, -1, 'up', self.game_map)
            elif key == arcade.key.S: self.player.move(0, 1, 'down', self.game_map)
            elif key == arcade.key.A: self.player.move(-1, 0, 'left', self.game_map)
            elif key == arcade.key.D: self.player.move(1, 0, 'right', self.game_map)

game_map_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

if __name__ == "__main__":
    window = MyGame(game_map_data)
    arcade.run()