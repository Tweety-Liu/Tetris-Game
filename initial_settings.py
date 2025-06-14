import pygame
block_size = 30    #設定每個位置的最小像素單位
columns, rows = 10, 20    #設定自定義的行列座標單位
pygame.display.set_caption("像素風俄羅斯方塊")
screen = pygame.display.set_mode((510, 720))
pygame.key.set_repeat(150, 50)
# 設定遊戲區的大小
width = columns * block_size
height = rows * block_size
# 設定遊戲區的起始像素位置
unit_width = 510 / 17
unit_height = 720 / 24
x_offset = 30           # 從左邊往右推 30px
y_offset = 60           # 從上方往下推 30px
# 遊戲邏輯板面大小
board_width = 10        # 10 格（橫向）
board_height = 20       # 20 格（縱向）
# 初始化遊戲邏輯板面]
def create_board():
    return [[0 for _ in range(columns)] for _ in range(rows)]
z1_block = [[
    [0, 1, 1],
    [1, 1, 0],
    [0, 0, 0]
],[
    [0, 1, 0],
    [0, 1, 1],
    [0, 0, 1]
],[
    [0, 0, 0],
    [0, 1, 1],
    [1, 1, 0]
],[
    [1, 0, 0],
    [1, 1, 0],
    [0, 1, 0]
]]
z2_block = [[
    [1, 1, 0],
    [0, 1, 1],
    [0, 0, 0]
],[
    [0, 0, 1],
    [0, 1, 1],
    [0, 1, 0]
],[
    [0, 0, 0],
    [1, 1, 0],
    [0, 1, 1]
],[
    [0, 1, 0],
    [1, 1, 0],
    [1, 0, 0]
]]
l3_block = [[
    [1, 0, 0],
    [1, 1, 1],
    [0, 0, 0]
],[
    [0, 1, 1],
    [0, 1, 0],
    [0, 1, 0]
],[
    [0, 0, 0],
    [1, 1, 1],
    [0, 0, 1]
],[
    [0, 1, 0],
    [0, 1, 0],
    [1, 1, 0]
]]
l4_block = [[
    [0, 0, 1],
    [1, 1, 1],
    [0, 0, 0]
],[
    [0, 1, 0],
    [0, 1, 0],
    [0, 1, 1]
],[
    [0, 0, 0],
    [1, 1, 1],
    [1, 0, 0]
],[
    [1, 1, 0],
    [0, 1, 0],
    [0, 1, 0]
]]
square5_block = [[[1, 1],
                  [1, 1]]]
tri6_block = [[
    [0, 1, 0],
    [1, 1, 1],
    [0, 0, 0]
],[
    [0, 1, 0],
    [0, 1, 1],
    [0, 1, 0]
],[
    [0, 0, 0],
    [1, 1, 1],
    [0, 1, 0]
],[
    [0, 1, 0],
    [1, 1, 0],
    [0, 1, 0]
]]
stick7_block = [[
    [0, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 0]
],[
    [0, 0, 0, 0],
    [1, 1, 1, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
],[
    [0, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 0]
],[
    [0, 0, 0, 0],
    [1, 1, 1, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]]
block_list = [z1_block, z2_block, l3_block, l4_block, square5_block, tri6_block, stick7_block]    #設定7種方塊的矩陣表示法（包含旋轉下四種狀態）


# Boss戰相關設定
# BOSS屬性
boss_hp = 3000
boss_max_hp = 3000
boss_start_time = None

boss_last_hit_time = 0
boss_hit_interval = 0.2


#頁面捲動
scroll_offset = 0
scroll_speed = 30
# 排行榜