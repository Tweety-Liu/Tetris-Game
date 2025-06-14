import pygame
from pygame.locals import *
from initial_settings import *  # 導入初始設定
from imagemusic_loader import *
def draw_boardscreen():
    g_ranking = pygame.transform.scale(bg_ranking, (width, height))

def handle_ranking_keys(event, scroll_offset, scroll_speed):
    if event.key == pygame.K_UP:
        return max(0, scroll_offset - scroll_speed)
    elif event.key == pygame.K_DOWN:
        return scroll_offset + scroll_speed
    return scroll_offset

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

#主選單畫面
def draw_main_menu(screen):
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 36)
    title = font.render("Tetris Game Menu", True, (255, 255, 255))
    opt1 = font.render("1. Normal Mode", True, (255, 255, 0))
    opt2 = font.render("2. Achievement Mode", True, (255, 255, 0))
    opt3 = font.render("3. View Leaderboard", True, (255, 255, 0))
    quit_opt = font.render("ESC to Quit", True, (255, 100, 100))

    screen.blit(title, (60, 80))
    screen.blit(opt1, (80, 140))
    screen.blit(opt2, (80, 180))
    screen.blit(opt3, (80, 220))
    screen.blit(quit_opt, (80, 280))

    pygame.display.flip()
# 取得玩家資料
def show():
    screen.blit(background3_img, (0, 0))
    running = True
    while running:
        # 遊戲邏輯與繪圖（略）
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False  # 按 q 就回主選單
        
        pygame.display.update()