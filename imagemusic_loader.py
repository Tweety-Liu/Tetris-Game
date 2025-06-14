import os
import pygame
current = os.path.dirname(__file__)
background_img = pygame.image.load(os.path.join(current, "UIimages", "bgimage.png"))    #導入背景圖片
# 將背景圖片縮放到指定大小
background_img = pygame.transform.scale(background_img, (510, 720))
background2_img = pygame.image.load(os.path.join(current, "UIimages", "bgimage2.png"))    #導入背景圖片
background2_img = pygame.transform.scale(background2_img, (510, 720))
background3_img = pygame.image.load(os.path.join(current, "UIimages", "bgimage3.png"))    #導入背景圖片
background3_img = pygame.transform.scale(background3_img, (510, 720))
background4_img = pygame.image.load(os.path.join(current, "UIimages", "bgimage4.png"))    #導入背景圖片
background4_img = pygame.transform.scale(background4_img, (510, 720))
boss_img = pygame.image.load(os.path.join(current, "UIimages","boss_idle.png"))
boss_img_hit = pygame.image.load(os.path.join(current, "UIimages","boss_hit.png"))
# 將BOSS圖片縮放到指定大小
boss_img = pygame.transform.scale(boss_img, (100, 100))
boss_hit_img = pygame.transform.scale(boss_img_hit, (100, 100))

pygame.mixer.init()
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
block_images = load_smallblockimage()    #小方塊圖片導入


# 音樂導入
def load_music():
    current = os.path.dirname(__file__)
    pygame.mixer.music.load(os.path.join(current, "sounds", "bgm.ogg"))  # 背景音樂
    pygame.mixer.music.set_volume(0.1)  # 音量設定
    pygame.mixer.music.play(-1)  # 循環播放
def load_gameover_sound():
    current = os.path.dirname(__file__)
    gameover_sound = pygame.mixer.Sound(os.path.join(current, "sounds", "gameover.wav"))  # 遊戲結束音效
    gameover_sound.set_volume(0.1)  # 音量設定
    return gameover_sound
def load_fallblock_sound():
    current = os.path.dirname(__file__)
    fallblock_sound = pygame.mixer.Sound(os.path.join(current, "sounds", "fall_block.wav"))  # 方塊下落音效
    fallblock_sound.set_volume(0.1)  # 音量設定
    return fallblock_sound
def load_clearlinelit_sound():
    current = os.path.dirname(__file__)
    clearlinelit_sound = pygame.mixer.Sound(os.path.join(current, "sounds", "line_clearlit.wav"))  # 消除行音效
    clearlinelit_sound.set_volume(0.1)  # 音量設定
    return clearlinelit_sound
def load_clearlineheavy_sound():
    current = os.path.dirname(__file__)
    clearlinehy_sound = pygame.mixer.Sound(os.path.join(current, "sounds", "line_clearheavy.wav"))  # 消除行音效
    clearlinehy_sound.set_volume(0.1)  # 音量設定
    return clearlinehy_sound
def load_bossbgm():
    current = os.path.dirname(__file__)
    pygame.mixer.music.load(os.path.join(current, "sounds", "bossbgm.ogg"))  # Boss戰背景音樂
    pygame.mixer.music.set_volume(0.2)  # 音量設定
    pygame.mixer.music.play(-1)  # 循環播放
def load_hit_sound():
    current = os.path.dirname(__file__)
    hit_sound = pygame.mixer.Sound(os.path.join(current, "sounds", "boss_hit.wav"))  # 方塊碰撞音效
    hit_sound.set_volume(0.1)  # 音量設定
    return hit_sound
# 排行榜導入
bg_ranking = pygame.image.load(os.path.join(current, "UIimages", "rankingbg.jpeg"))
bg_ranking = pygame.transform.scale(bg_ranking, (510, 720))