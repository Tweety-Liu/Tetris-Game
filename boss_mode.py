import pygame
import random
from pygame.locals import *
from initial_settings import *    #導入初始設定
from game_logic import *    #導入遊戲邏輯
import tkinter as tk
from tkinter import messagebox
from imagemusic_loader import *    #導入圖片與音樂
import time

def run_game():# 初始化pygame
    pygame.init()    #初始化pygame
    load_bossbgm()   #載入音樂
    clearlinelit_sound = load_clearlinelit_sound()    #載入消除行音效
    clearlinehy_sound = load_clearlineheavy_sound()
    BOSS_HP = 3000
    BOSS_HIT_INTERVAL = 0.2
    last_garbage_time = pygame.time.get_ticks()
    # 初始化pygame
    pygame.init()    #初始化pygame
    load_bossbgm()   #載入音樂
    clearlinelit_sound = load_clearlinelit_sound()    #載入消除行音效
    clearlinehy_sound = load_clearlineheavy_sound()
    boss_current_img = boss_hit_img
    game_mode = "boss"
    score = 0
    fall_time = 0
    fall_speed = 1000
    time_font = pygame.font.SysFont("Arial", 24)
    clock = pygame.time.Clock()
    board = create_board()    #建立遊戲邏輯板面
    left_hp = BOSS_HP - score
    i = random.randint(0, len(block_list) - 1)
    block_type = i + 1
    shape = block_list[i]
    image = block_image[i]
    current_block = Block(4 , 0 , shape, image, block_type)
    next_block = Block.generate_newblock()
    draw_next_block(screen, next_block, 390, 210)   #畫下一個方塊
    nstart_ticks = pygame.time.get_ticks()  # 計時開始
    running = True
    while running:
        screen.blit(background_img, (0, 0))         # 背景
        current_time = pygame.time.get_ticks()      # 時間紀錄
        current_block.draw(screen, block_size)      # 畫目前方塊
        draw_next_block(screen, next_block, 390, 210)   #畫下一個方塊
        screen.blit(boss_current_img, (220, 85))  # 畫 Boss 圖片
        npassed_milsecond = pygame.time.get_ticks() - nstart_ticks
        ntotal_seconds = npassed_milsecond // 1000
        npassed_minutes = ntotal_seconds // 60
        npassed_seconds = ntotal_seconds % 60
        time_string = f"{npassed_minutes:02}:{npassed_seconds:02}"
        timer_surface = time_font.render(time_string, True, (255, 255, 255))
        screen.blit(timer_surface, (40, 60))     # 計時器
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:  # 按下 ESC 或 Q 鍵離開遊戲
                    running = False  # ESC 離開
                elif event.key == pygame.K_p:  # 按下空白鍵暫停遊戲
                    pause_start_ticks = pygame.time.get_ticks()
                    pause = True
                    while pause:
                        for pause_event in pygame.event.get():
                            if pause_event.type == pygame.QUIT:
                                pause = False
                                running = False
                            elif pause_event.type == pygame.KEYDOWN:
                                if pause_event.key == pygame.K_ESCAPE or pause_event.key == pygame.K_q:
                                    pause = False
                                    running = False
                else:
                    handle_common_game_keys(event, current_block, board, load_fallblock_sound())  # 處理遊戲按鍵
        if current_time - fall_time > fall_speed:
            board, score ,current_block, next_block = handle_block_fall(game_mode, current_block, board, next_block, clearlinehy_sound, clearlinelit_sound, score)
            fall_time = current_time
        current_time = pygame.time.get_ticks()
        if current_time - last_garbage_time >= 20000:
            add_garbage_lines(board, 3)  # 每20秒添加一行垃圾
            last_garbage_time = current_time

        font = pygame.font.SysFont(None, 35)
        score_text = font.render("HP", True, (255, 255, 255))
        screen.blit(score_text, (360, 60))
        score_value = font.render(str(BOSS_HP - score), True, (255, 0, 0))
        screen.blit(score_value, (380, 90)) 
        draw_board(screen, board)

        pygame.display.update()
        clock.tick(60)

