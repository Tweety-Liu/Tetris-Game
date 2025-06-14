import pygame
import sys
import time
import random
from pygame.locals import *
from pygame.locals import *
from initial_settings import *    #導入初始設定
from game_logic import *    #導入遊戲邏輯
import tkinter as tk
from tkinter import messagebox
from imagemusic_loader import *    #導入圖片與音樂
from boss_mode import *    #導入BOSS模式相關函式
from login import Player, PlayerDataManager    #導入登入模組
from normal_mode import *
from boss_mode import *
screen = pygame.display.set_mode((510, 720))
pygame.display.set_caption("Tetris Game")

buttons = [
    {"text": "Normal", "pos": (200, 100), "action": "normal"},
    {"text": "BOSS", "pos": (200, 180), "action": "boss"},
    {"text": "Ranking", "pos": (200, 260), "action": "rank"},
]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
pygame.init()

# === 字型 & 顏色 ===
font = pygame.font.SysFont(None, 50)
def draw_buttons():
    screen.fill(WHITE)
    for btn in buttons:
        pygame.draw.rect(screen, BLUE, (*btn["pos"], 200, 50))
        txt = font.render(btn["text"], True, WHITE)
        screen.blit(txt, (btn["pos"][0] + 30, btn["pos"][1] + 10))
    pygame.display.flip()

def check_click(pos):
    for btn in buttons:
        x, y = btn["pos"]
        if x <= pos[0] <= x + 200 and y <= pos[1] <= y + 50:
            return btn["action"]
    return None

def main_menu():
    
    while True:
        pygame.mixer.music.stop()  # 🔊 停掉上一段音樂
        pygame.mixer.stop() 
        draw_buttons()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                action = check_click(event.pos)
                if action == "normal":
                    import normal_mode
                    normal_mode.run_game()  
                elif action == "boss":
                    import boss_mode
                    boss_mode.run_game()
                elif action == "rank":
                    import ranking
                    ranking.show()
        pygame.display.update()


  # 然後進入主選單
def show_start_screen(screen):
    screen.blit(background4_img, (0, 0)) # 顯示封面圖片
    pygame.display.update()

    # 等待任意鍵或滑鼠點擊
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                waiting = False
if __name__ == "__main__":
    pygame.init()
    show_start_screen(screen)  # 🔥 顯示封面
    main_menu()



# === 按鈕資料 ===
