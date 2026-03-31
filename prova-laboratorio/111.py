from PIL import Image

def image_to_matrix(image_path, rows=39, cols=51):
    img = Image.open(image_path).convert('RGB')
    width, height = img.size
    
    # 计算每个格子的平均宽高
    cell_w = width / cols
    cell_h = height / rows
    
    matrix = []
    
    for r in range(rows):
        row_data = []
        for c in range(cols):
            # 取格子的中心点坐标，避开边缘的网格线
            center_x = int(c * cell_w + cell_w / 2)
            center_y = int(r * cell_h + cell_h / 2)
            
            # 获取该点的 RGB 颜色
            r_val, g_val, b_val = img.getpixel((center_x, center_y))
            
            # 颜色判定逻辑 (根据你图片的主色调)
            # 橙色 (墙): R 高, G 中, B 低
            if r_val > 200 and g_val > 100 and b_val < 100:
                row_data.append(1) # 墙
            # 蓝色 (起点/出口): B 高
            elif b_val > 150 and r_val < 150:
                row_data.append(2)
            # 红色 (目标): R 高, G 低, B 低
            elif r_val > 200 and g_val < 100:
                row_data.append(3)
            # 白色或其他 (空地)
            else:
                row_data.append(0)
                
        matrix.append(row_data)
    return matrix

# 使用方法
image_path = "prova-laboratorio/jBvyfLbsfcwwsix.png!a-3-854x.webp" # 替换成你的文件名
map_matrix = image_to_matrix(image_path)

# 打印出可以复制到代码里的格式
print("game_map = [")
for row in map_matrix:
    print(f"    {row},")
print("]")