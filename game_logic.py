from initial_settings import *
from imagemusic_loader import *    #導入圖片與音樂
import pygame
import random
from pygame.locals import *
import tkinter as tk
from tkinter import messagebox
import time
gameover_sound = load_gameover_sound()    #載入遊戲結束音效
load_fallblock_sound()    #載入方塊下落音效

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

    def get_image(self):
        if self.can_rotate:
            return self.block_image[self.rotation]
        else:
            return self.block_image[0]

    def draw(self, screen, block_size):
        pixel_x = x_offset + (self.x + self.offset_x) * block_size
        pixel_y = y_offset + (self.y + self.offset_y) * block_size
        screen.blit(self.get_image(), (pixel_x, pixel_y))
    
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
    
    # 生成方塊
    @staticmethod
    def generate_newblock():
        i = random.randint(0, len(block_list) - 1)
        block_type = i + 1
        original_shape = block_list[i]
        image = block_image[i]
        shape, offset_x, offset_y = Block.trim_shape_and_offset(original_shape)
        new_block = Block(4 - offset_x, 0, shape, image, block_type)
        return new_block
    


def handle_common_game_keys(event, current_block, board, fallblock_sound):
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
        fallblock_sound.play()
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


def draw_next_block(screen, next_block, x, y, scale=0.8):
    img = next_block.get_image()  # 取得原圖
    w, h = img.get_size()         # 取得原圖寬高
    if next_block.block_type == 7:
        scale = 0.6
    new_size = (int(w * scale), int(h * scale))  # 計算新尺寸
    scaled_img = pygame.transform.smoothscale(img, new_size)  # 縮放圖片（平滑縮放）
    screen.blit(scaled_img, (x, y))
    
def handle_block_fall(game_mode, current_block, board, next_block, clearlinehy_sound, clearlinelit_sound, score=0):
    current_block.y += 1
    if not is_valid_position(current_block, board):
        current_block.y -= 1
        lock_block(current_block, board)
        board, lines_cleared = clear_lines(board)
        score += lines_cleared * 100
        if lines_cleared > 0:
            if lines_cleared >= 4:
                clearlinehy_sound.play()
            elif lines_cleared == 1:
                clearlinelit_sound.play()
        current_block = next_block
        next_block = Block.generate_newblock()
        global running
        if game_mode == "normal":
            if not is_valid_position(current_block, board):
                show_game_over_dialog()
                running = False

        elif game_mode == "boss":
            if "boss_hp" in globals() and boss_hp - score < 0:
                show_game_over_dialog()
                running = False
    return board, score, current_block, next_block

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

def draw_board(screen, board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            value = board[row][col]
            if value != 0:
                if value in block_images:
                    screen.blit(block_images[value], (x_offset + col * block_size, y_offset + row * block_size))
                else:
                    pygame.draw.rect(screen,(255, 255, 255),(x_offset + col * block_size, y_offset + row * block_size, block_size, block_size))
                                     
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
    

def show_game_over_dialog():
    global gameover_sound
    gameover_sound.play()
    pygame.mixer.music.stop()  # 停止背景音樂
    pygame.display.flip()  # 更新畫面
    # 使用 tkinter 顯示遊戲結束對話框
    pygame.time.delay(1000)  # 等待音效播放完畢
    root = tk.Tk()
    root.withdraw()  # 隱藏主視窗
    result = messagebox.askyesno("遊戲結束", "遊戲結束！是否進入boss模式挑戰。")
    root.destroy()
    import main_stream
    main_stream.run_game()  # 返回主選單
    

    
#boss關卡
def handle_boss_mode_keys(event, boss_state):
    if event.key == pygame.K_b:
        boss_state["special_attack"] = True
# 函數：BOSS關畫面

def draw_bar(screen, left_hp, BOSS_HP):
    bar_width = 250
    hp_ratio = left_hp / BOSS_HP
    pygame.draw.rect(screen, (255, 0, 0), (45, 70, int(bar_width * hp_ratio), 15))  # 畫出血條
    font = pygame.font.SysFont("Arial", 24)
    hp_text = font.render(f"{left_hp}/{BOSS_HP}", True, (255, 255, 255))
    screen.blit(hp_text, (380, 90))

def draw_boss_mode():
    global font
    if 'font' not in globals():
        font = pygame.font.SysFont("Arial", 32)
    screen.fill((0, 0, 0))
    screen.blit(boss_current_img, (250, 100))

    # 畫血條
    
def draw_boss_result(boss_result, result_time):
    global font
    if 'font' not in globals():
        font = pygame.font.SysFont("Arial", 32)
    screen.fill((10, 0, 0))
    result_font = pygame.font.SysFont("Arial", 48)
    result_text = "🎉 勝利！🎉" if boss_result == "win" else "😢 失敗 😢"
    result_color = (255, 255, 0) if boss_result == "win" else (200, 0, 0)
    text = result_font.render(result_text, True, result_color)
    screen.blit(text, (180, 200))

    # 星數
    if boss_result == "win":
        if result_time <= 180:
            stars = 3
        elif result_time <= 300:
            stars = 2
        else:
            stars = 1
    else:
        stars = 0
    star_display = "★" * stars + "☆" * (3 - stars)
    star_text = font.render(f"星級: {star_display}", True, (255, 255, 0))
    screen.blit(star_text, (180, 270))
    info = font.render("按下 ESC 回主選單", True, (255, 255, 255))
    screen.blit(info, (160, 360))
    screen.blit(star_text, (180, 270))
    info = font.render("按下 ESC 回主選單", True, (255, 255, 255))
    screen.blit(info, (160, 360))

def add_garbage_lines(board, num_lines=1):
    for _ in range(num_lines):
        garbage_line = [1 if random.random() < 0.9 else 0 for _ in range(len(board[0]))]
        board.pop(0)  # 移除最上面一行
        board.append(garbage_line)

def hit_boss(damage, board):
    global boss_hp, boss_current_img, boss_last_hit_time
    boss_hp -= damage
    boss_current_img = boss_img_hit
    boss_last_hit_time = time.time()
    add_garbage_lines(board, 2)
def reset_boss():
    global boss_hp, boss_start_time, boss_current_img, boss_last_hit_time
    boss_hp = boss_max_hp
    boss_start_time = time.time()
    boss_current_img = boss_img
    boss_last_hit_time = 0