import pygame
import sys
import os

# --- 初始化 ---
pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pixel Adventure - 精细纹理版")

# 关键修改：放大格子的尺寸，从 40 放大到 48 (1.2倍)
TILE_SIZE = 64
# 移动速度，建议为 48 的约数 (2, 3, 4, 6, 8, 12, 16, 24)
MOVE_SPEED = 4 

# --- 1. 资源加载函数 ---
def load_animation(filename, frames_count=8):
    try:
        sheet = pygame.image.load(filename).convert_alpha()
        w, h = sheet.get_size()
        fw = w // frames_count
        frames = []
        for i in range(frames_count):
            frame = sheet.subsurface(pygame.Rect(i * fw, 0, fw, h))
            # 缩放到角色在该格子下的合适大小
            frame = pygame.transform.scale(frame, (TILE_SIZE, TILE_SIZE))
            frames.append(frame)
        return frames
    except FileNotFoundError:
        # 如果图加载失败，创建一个纯灰色方块代替
        f = pygame.Surface((TILE_SIZE, TILE_SIZE))
        f.fill((100, 100, 100))
        return [f] * frames_count

# --- 关键修改：从你提供的图片中加载墙体材质 ---
# 获取图片的完整路径，确保万无一失
current_dir = os.path.dirname(__file__)
TILE_IMAGE_PATH = os.path.join(current_dir, "gioco/unnamed.jpg")

try:
    tile_image = pygame.image.load(TILE_IMAGE_PATH).convert()
    # 缩放到新的 TILE_SIZE，使其与格子对齐
    tile_image = pygame.transform.scale(tile_image, (TILE_SIZE, TILE_SIZE))
except FileNotFoundError:
    print(f"❌ 找不到材质文件: {TILE_IMAGE_PATH}，请确保图片在脚本同一目录下。使用灰色方块代替。")
    tile_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
    tile_image.fill((100, 100, 100))

# 加载动画序列
animations = {
    'run_up': load_animation('gioco/run_up.png'),
    'run_down': load_animation('gioco/run_down.png'),
    'run_left': load_animation('gioco/run_left.png'),
    'run_right': load_animation('gioco/run_right.png'),
    'idle_down': load_animation('gioco/idle_down.png')
}

# 目标物体图片 (2) - 类似出口
goal_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
goal_image.fill((0, 255, 100)) # 亮绿色

# --- 2. 地图数据 ---
# 注意：你的地图最后一列 (50) 全部是 1，这意味着如果不处理，玩家走到最右边后摄像机无法完全居中。
game_map = [
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 3, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
[1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
[1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


# 按要求修改地图：(25, 38)的 2 替换成 0
# 坐标是 (行, 列)，索引是 [行][列] -> game_map[38][25]
if len(game_map) > 38 and len(game_map[38]) > 25:
    game_map[38][25] = 0

# --- 3. 角色逻辑类 ---
class Player:
    def __init__(self, start_x, start_y):
        self.grid_x = start_x
        self.grid_y = start_y
        self.pixel_x = start_x * TILE_SIZE
        self.pixel_y = start_y * TILE_SIZE
        self.target_px = self.pixel_x
        self.target_py = self.pixel_y
        
        self.is_moving = False
        self.dir = 'down'
        self.anim_idx = 0.0

    def move(self, dx, dy, direction):
        if self.is_moving: return
        self.dir = direction
        nx, ny = self.grid_x + dx, self.grid_y + dy
        
        # 边界与碰撞检测：如果是墙(1)，则阻挡
        if 0 <= ny < len(game_map) and 0 <= nx < len(game_map[0]):
            if game_map[ny][nx] != 1:
                self.grid_x, self.grid_y = nx, ny
                self.target_px, self.target_py = nx * TILE_SIZE, ny * TILE_SIZE
                self.is_moving = True

    def update(self):
        if self.is_moving:
            if self.pixel_x < self.target_px: self.pixel_x += MOVE_SPEED
            elif self.pixel_x > self.target_px: self.pixel_x -= MOVE_SPEED
            if self.pixel_y < self.target_py: self.pixel_y += MOVE_SPEED
            elif self.pixel_y > self.target_py: self.pixel_y -= MOVE_SPEED
            
            if self.pixel_x == self.target_px and self.pixel_y == self.target_py:
                self.is_moving = False
            self.anim_idx += 0.2 # 跑步速度
        else:
            self.anim_idx += 0.05 # 呼吸速度
            
        if self.anim_idx >= 8: self.anim_idx = 0

    def draw(self, cam_x, cam_y):
        state = f"run_{self.dir}" if self.is_moving else "idle_down"
        img = animations[state][int(self.anim_idx)]
        screen.blit(img, (self.pixel_x - cam_x, self.pixel_y - cam_y))

# --- 4. 实例化角色：在 (13, 3) 生成 ---
player = Player(13, 3)

# --- 5. 主循环 ---
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    # 输入控制
    keys = pygame.key.get_pressed()
    if not player.is_moving:
        if keys[pygame.K_w]: player.move(0, -1, 'up')
        elif keys[pygame.K_s]: player.move(0, 1, 'down')
        elif keys[pygame.K_a]: player.move(-1, 0, 'left')
        elif keys[pygame.K_d]: player.move(1, 0, 'right')

    player.update()

    # 摄像机跟随逻辑
    cam_x = player.pixel_x - SCREEN_WIDTH // 2 + TILE_SIZE // 2
    cam_y = player.pixel_y - SCREEN_HEIGHT // 2 + TILE_SIZE // 2
    
    # 限制摄像机边界，防止地图边缘出现黑边
    map_width_px = len(game_map[0]) * TILE_SIZE
    map_height_px = len(game_map) * TILE_SIZE
    cam_x = max(0, min(cam_x, map_width_px - SCREEN_WIDTH))
    cam_y = max(0, min(cam_y, map_height_px - SCREEN_HEIGHT))

    screen.fill((30, 30, 30)) # 背景设为黑色

    # 6. 渲染地图
    for r_idx, row in enumerate(game_map):
        for c_idx, cell in enumerate(row):
            draw_pos = (c_idx * TILE_SIZE - cam_x, r_idx * TILE_SIZE - cam_y)
            # 视口裁剪：只画屏幕内的格子
            if -TILE_SIZE < draw_pos[0] < SCREEN_WIDTH and -TILE_SIZE < draw_pos[1] < SCREEN_HEIGHT:
                if cell == 1:
                    screen.blit(tile_image, draw_pos)
                elif cell == 2:
                    screen.blit(goal_image, draw_pos)

    # 绘制角色
    player.draw(cam_x, cam_y)

    pygame.display.flip()
    clock.tick(60)