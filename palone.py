import arcade
import os

# --- 游戏常量 ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
SCREEN_TITLE = "Pixel Adventure - Golden Coins!"

TILE_SIZE = 64
MOVE_SPEED = 5  # 略微调快了一点

# 地图数据 (0:空地, 1:墙, 2:终点, 3:金币)
GAME_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 0, 0, 0, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

def load_animation_frames(filename, frames_count=8):
    """ 使用 Arcade 3.x 兼容的方式加载切片动画 """
    frames = []
    try:
        # 先加载大图
        main_texture = arcade.load_texture(filename)
        frame_width = main_texture.width // frames_count
        frame_height = main_texture.height
        
        for i in range(frames_count):
            # 使用 create_subtexture 裁剪 (Arcade 3.x 推荐做法)
            texture = main_texture.create_subtexture(
                left=i * frame_width,
                top=0,
                width=frame_width,
                height=frame_height
            )
            frames.append(texture)
    except Exception as e:
        print(f"Warning: Error loading {filename}: {e}")
        # 错误占位图
        placeholder = arcade.make_soft_square_texture(TILE_SIZE, arcade.color.FUCHSIA, outer_alpha=255)
        frames = [placeholder] * frames_count
    return frames

class Coin(arcade.Sprite):
    def __init__(self, x, y, frames):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.frames = frames
        self.texture = self.frames[0]
        self.anim_index = 0

    def update_animation(self, delta_time: float = 1/60):
        self.anim_index += 0.15
        if self.anim_index >= len(self.frames):
            self.anim_index = 0
        self.texture = self.frames[int(self.anim_index)]

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        # 加载所有状态动画
        self.animations = {
            'run_up': load_animation_frames('foto/run_up.png'),
            'run_down': load_animation_frames('foto/run_down.png'),
            'run_left': load_animation_frames('foto/run_left.png'),
            'run_right': load_animation_frames('foto/run_right.png'),
            'idle_down': load_animation_frames('foto/idle_down.png'),
            'idle_left': load_animation_frames('foto/idle_left.png'),
            'idle_right': load_animation_frames('foto/idle_right.png'),
            'idle_up': load_animation_frames('foto/idle_down.png') # 缺图可用 down 暂代
        }
        self.texture = self.animations['idle_down'][0]
        self.direction = 'down'
        self.anim_index = 0.0
        self.is_moving = False

    def update(self):
        """ 物理位图更新 """
        # 预判下一步是否撞墙
        future_x = self.center_x + self.change_x
        future_y = self.center_y + self.change_y
        
        # 这里仅作简单的边界和物理移动，真正的墙体碰撞在 View 的 update 里用物理引擎或 check_collision 处理更好
        # 但为了保持逻辑简单，我们直接应用 change_x/y
        self.center_x += self.change_x
        self.center_y += self.change_y

    def update_animation(self, delta_time: float = 1/60):
        # 根据速度判断状态
        self.is_moving = (abs(self.change_x) > 0.1 or abs(self.change_y) > 0.1)
        
        if self.change_x > 0: self.direction = 'right'
        elif self.change_x < 0: self.direction = 'left'
        elif self.change_y > 0: self.direction = 'up'
        elif self.change_y < 0: self.direction = 'down'

        state = f"{'run' if self.is_moving else 'idle'}_{self.direction}"
        if state not in self.animations: state = 'idle_down'
        
        frames = self.animations[state]
        self.anim_index += 0.2
        if self.anim_index >= len(frames):
            self.anim_index = 0
        self.texture = frames[int(self.anim_index)]

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player = None
        self.player_list = None
        self.wall_list = None
        self.coin_list = None
        self.camera = None
        
        # 按键状态
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList()
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # 预加载金币动画资源 (只加载一次！)
        coin_frames = load_animation_frames("foto/animated_items.png", 8)

        # 加载地图
        map_height = len(GAME_MAP)
        for row_idx, row in enumerate(GAME_MAP):
            for col_idx, cell in enumerate(row):
                x = col_idx * TILE_SIZE + TILE_SIZE // 2
                y = (map_height - 1 - row_idx) * TILE_SIZE + TILE_SIZE // 2
                
                if cell == 1:
                    wall = arcade.SpriteSolidColor(TILE_SIZE, TILE_SIZE, arcade.color.GRAY)
                    wall.center_x, wall.center_y = x, y
                    self.wall_list.append(wall)
                elif cell == 3:
                    coin = Coin(x, y, coin_frames)
                    self.coin_list.append(coin)

        # 设置主角
        self.player = Player()
        self.player.center_x = 13 * TILE_SIZE
        self.player.center_y = (map_height - 3) * TILE_SIZE
        self.player_list.append(self.player)

    def update_player_speed(self):
        """ 参考你给出的 Better Move 逻辑 """
        self.player.change_x = 0
        self.player.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player.change_y = MOVE_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player.change_y = -MOVE_SPEED
            
        if self.left_pressed and not self.right_pressed:
            self.player.change_x = -MOVE_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player.change_x = MOVE_SPEED

    def on_key_press(self, key, modifiers):
        if key in [arcade.key.UP, arcade.key.W]: self.up_pressed = True
        elif key in [arcade.key.DOWN, arcade.key.S]: self.down_pressed = True
        elif key in [arcade.key.LEFT, arcade.key.A]: self.left_pressed = True
        elif key in [arcade.key.RIGHT, arcade.key.D]: self.right_pressed = True
        self.update_player_speed()

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.UP, arcade.key.W]: self.up_pressed = False
        elif key in [arcade.key.DOWN, arcade.key.S]: self.down_pressed = False
        elif key in [arcade.key.LEFT, arcade.key.A]: self.left_pressed = False
        elif key in [arcade.key.RIGHT, arcade.key.D]: self.right_pressed = False
        self.update_player_speed()

    def on_update(self, delta_time):
        # 更新玩家位置
        self.player_list.update()
        
        # 墙体碰撞处理 (阻止穿墙)
        hit_list = arcade.check_for_collision_with_list(self.player, self.wall_list)
        for wall in hit_list:
            # 简单的碰撞回退逻辑
            if self.player.change_x > 0: self.player.right = wall.left
            elif self.player.change_x < 0: self.player.left = wall.right
            if self.player.change_y > 0: self.player.top = wall.bottom
            elif self.player.change_y < 0: self.player.bottom = wall.top

        # 更新动画
        self.player_list.update_animation(delta_time)
        self.coin_list.update_animation(delta_time)

        # 吃金币
        coins_hit = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coins_hit:
            coin.remove_from_sprite_lists()

        # 相机跟随
        self.center_camera_to_player()

    def center_camera_to_player(self):
        screen_center_x = self.player.center_x - (SCREEN_WIDTH / 2)
        screen_center_y = self.player.center_y - (SCREEN_HEIGHT / 2)
        
        # 限制相机不超出地图边界
        map_w = len(GAME_MAP[0]) * TILE_SIZE
        map_h = len(GAME_MAP) * TILE_SIZE
        if screen_center_x < 0: screen_center_x = 0
        if screen_center_y < 0: screen_center_y = 0
        
        self.camera.move_to((screen_center_x, screen_center_y))

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game = GameView()
    game.setup()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()