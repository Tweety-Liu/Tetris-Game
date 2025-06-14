import pygame
import random
import tkinter as tk
from tkinter import messagebox
import os
from pygame.locals import *
pygame.init()    #初始化pygame
block_size = 30    #設定每個位置的最小像素單位
columns, rows = 10, 20    #設定自定義的行列座標單位
pygame.display.set_caption("像素風俄羅斯方塊")
current = os.path.dirname(__file__)
screen = pygame.display.set_mode((510, 720))
background_img = pygame.image.load(os.path.join(current, "UIimages", "bgimage.png"))
background_img = pygame.transform.scale(background_img, (510, 720))    #調整背景圖大小 
pygame.key.set_repeat(150, 50)    #設定按鍵重複觸發的時間間隔
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

# 初始化邏輯 board
board = [[0 for _ in range(board_width)] for _ in range(board_height)]
bg_ranking = pygame.image.load(os.path.join(current, "UIimages", "rankingbg.jpeg"))
bg_ranking = pygame.transform.scale(bg_ranking, (510, 720)) #導入排行榜背景圖 
def load_blockimage(kind):    #我用了一個函式自動把每個方塊的完整大圖抓過來
    angs = [0, 90, 180, 270]
    image = []
    current = os.path.dirname(__file__)
    if kind == "square5":
            path = os.path.join(current, "UIimages", "square5_0.png")
            every = pygame.image.load(path).convert_alpha()
            image.append(every)
    else:
        for ang in angs:
            file_name = f"{kind}_{ang}.png"
            path = os.path.join(current, "UIimages", file_name)
            every = pygame.image.load(path).convert_alpha()
            image.append(every)
    return image
def load_smallblockimage():
    current = os.path.dirname(__file__)
    littleimage = dict()
    for i in range(1, 8):
        file_name = f"block{i}.png"
        path = os.path.join(current, "UIimages", file_name)
        littleimage[i] = pygame.image.load(path).convert_alpha()
    return littleimage
z1_block_img = load_blockimage("z1")
z2_block_img = load_blockimage("z2")
l3_block_img = load_blockimage("l3")
l4_block_img = load_blockimage("l4")
square5_block_img = load_blockimage("square5")
tri6_block_img = load_blockimage("tri6")
stick7_block_img = load_blockimage("stick7")
block_image = [z1_block_img, z2_block_img, l3_block_img, l4_block_img, square5_block_img, tri6_block_img, stick7_block_img]    #把圖整理進方塊選擇列表，方便未來貼上
block_images = load_smallblockimage()
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
board = [[0 for _ in range(columns)] for _ in range(rows)]

def lock_block(block, board):
    shape = block.block_list[block.rotation]
    rows = len(shape)
    cols = len(shape[0])
    for row in range(rows):
        for col in range(cols):
            if shape[row][col] == 1:
                x = block.x + col
                y = block.y + row
                if 0 <= y < len(board) and 0 <= x < len(board[0]):
                    board[y][x] = block.block_type    # 把目前這個正在下落或放置的方塊的類型，記錄到 board上對應的格子中，表示這一格已經被佔住了
                    
def is_valid_position(block, board):
    shape = block.block_list[block.rotation]
    for row in range(len(shape)):
        for col in range(len(shape[0])):
            if shape[row][col] == 1:
                x = block.x + col
                y = block.y + row    # 判斷是否越界或碰撞到已存在的方塊
                if x < 0 or x >= len(board[0]) or y >= len(board):
                    return False
                if y >= 0 and board[y][x] != 0:
                    return False
    return True
def clear_lines(board):
    cleared_lines = 0
    new_board = []
    for row in board:
        if 0 in row:
            new_board.append(row)
        else:
            cleared_lines += 1    # 找到一整排滿的行就消除    # 消除的行數加上空白行放回頂部
    for _ in range(cleared_lines):
        new_board.insert(0, [0]*len(board[0]))
    return new_board, cleared_lines
    
def draw_board(screen, board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            value = board[row][col]
            if value != 0:
                if value in block_images:
                    screen.blit(block_images[value], (x_offset + col * block_size, y_offset + row * block_size))
                else:
                    pygame.draw.rect(screen,(255, 255, 255),(x_offset + col * block_size, y_offset + row * block_size, block_size, block_size))
                    
def show_game_over_dialog():
    root = tk.Tk()
    root.withdraw()
    tk.messagebox.showinfo("Game Over", "遊戲結束了，謝謝遊玩！")
    root.destroy()

def draw_leaderboard_page(screen, manager, scroll_offset):
    # 畫背景
    screen.bilt(bg_ranking, (0, 0))
    # 畫標題
    font_title = pygame.font.SysFont(None, 36)
    font_entry = pygame.font.SysFont("Arial", 28)
    title = font_title.render("🏆Rankings🏆(Press ESC to return)", True, (255, 255, 255))
    screen.blit(title, (20, 20))

    # 取得玩家資料
    players = manager.get_all_ranked_players()

    header = font_entry.render("Rank     Player            Score", True, (255,255,0))
    screen.bilt(header, (30, 70))

    # 玩家資料列
    for idx, (username, score) in enumerate(players, 1):
        entry = font_entry.render(f"{idx:<5}  {username:<12}  {score}", True, (255, 255, 255))
        y_pos = 100 + (idx - 1) * 30 - scroll_offset
        if 100 <= y_pos <= height - 30:
            screen.blit(entry, (30, y_pos))
    pygame.display.flip()
class Block:
    def __init__(self, x, y, shape, image, block_type):
        self.x = x    # 欲顯示的位置
        self.y = y
        self.block_list = shape    # 形狀資料，可能包含 4 個旋轉方向
        self.block_image = image    # 對應旋轉的圖片
        self.rotation = 0               # 初始角度為 0
        self.block_type = block_type    #小方塊圖片
        if self.block_type == 5:  
            self.can_rotate = False
        else:
            self.can_rotate = True
        self.update_trimmed_shape()
    def rotate(self):
        if self.can_rotate:
            self.rotation = (self.rotation + 1) % len(self.block_list)
            self.update_trimmed_shape()

    def update_trimmed_shape(self):
        shape = self.block_list[self.rotation]
        trimmed, offset_x, offset_y = self.trim_shape_and_offset(shape)
        self.trimmed_shape = trimmed
        self.offset_x = offset_x
        self.offset_y = offset_y

    def get_image(self):
        if self.can_rotate:
            return self.block_image[self.rotation]
        else:
            return self.block_image[0]

    def draw(self, screen, block_size):
        pixel_x = x_offset + (self.x + self.offset_x) * block_size
        pixel_y = y_offset + (self.y + self.offset_y) * block_size
        screen.blit(self.get_image(), (pixel_x, pixel_y))

    @staticmethod
    def trim_shape_and_offset(shape):
        # 移除空的列與行
        top, bottom = 0, len(shape) - 1
        while top <= bottom and all(cell == 0 for cell in shape[top]):
            top += 1
        while bottom >= top and all(cell == 0 for cell in shape[bottom]):
            bottom -= 1

        left, right = 0, len(shape[0]) - 1
        while left <= right and all(row[left] == 0 for row in shape):
            left += 1
        while right >= left and all(row[right] == 0 for row in shape):
            right -= 1

        trimmed = [row[left:right+1] for row in shape[top:bottom+1]]
        return trimmed, left, top
    
def generate_newblock():    # 生成方塊
    global current_block, running  # 修改全域變數
    i = random.randint(0, len(block_list) - 1)
    block_type = i + 1
    original_shape = block_list[i]
    image = block_image[i]
    shape, offset_x, offset_y = Block.trim_shape_and_offset(original_shape)

    # x = 4 是初始位置，要考慮偏移量
    current_block = Block(4 - offset_x, 0, shape, image, block_type)
    
    if not is_valid_position(current_block, board):
        show_game_over_dialog()
        running = False
        
score = 0
fall_time = 0
fall_speed = 1000
clock = pygame.time.Clock()
i = random.randint(0, len(block_list) - 1)
block_type = i + 1
shape = block_list[i]
image = block_image[i]
current_block = Block(4 , 0 , shape, image, block_type)
#頁面捲動
scroll_offset = 0
scroll_speed = 30

running = True
while running:
    screen.blit(background_img, (0, 0))
    current_time = pygame.time.get_ticks()
    current_block.draw(screen, block_size)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                current_block.x -= 1
                if not is_valid_position(current_block, board):
                    current_block.x += 1
            elif event.key == pygame.K_s:
                current_block.y += 1
                if not is_valid_position(current_block, board):
                    current_block.y -= 1
            elif event.key == pygame.K_d:
                current_block.x += 1
                if not is_valid_position(current_block, board):
                    current_block.x -= 1
            elif event.key == pygame.K_x:
                current_block.y += 1
                if not is_valid_position(current_block, board):
                    current_block.y -= 1
            elif event.key == pygame.K_SPACE:
                while True:
                    current_block.y += 1
                    if not is_valid_position(current_block, board):
                        current_block.y -= 1
                        break
            elif event.key == pygame.K_j:
                original_rotation = current_block.rotation
                current_block.rotate()
                if not is_valid_position(current_block, board):
                    current_block.rotation = original_rotation
            elif event.key == pygame.K_UP:
                scroll_offset = max(0,scroll_offset - scroll_speed)
            elif event.key == pygame.K_DOWN:
                scroll_offset += scroll_speed
    if current_time - fall_time > fall_speed:
        current_block.y += 1
        if not is_valid_position(current_block, board):
            current_block.y -= 1
            lock_block(current_block, board)
            board, lines_cleared = clear_lines(board)
            score += lines_cleared * 100
            generate_newblock()  # 用產生函式
        fall_time = current_time        # 畫出方塊與已鎖定方塊
        
    draw_board(screen, board)
    pygame.display.update()
    clock.tick(60)
pygame.quit()