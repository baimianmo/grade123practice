#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英语学习游戏合集 - 主程序
模块化重构版本
"""

import pygame
import sys
from chinese_output import render_chinese_text
from word_audio import AudioSystem

# 导入游戏模块
from game_whack_a_mole import WhackAMoleGame
from game_sandbag import SandbagGame
from game_match import MatchGame
from game_spelling import SpellingGame
from game_flashcard import FlashcardGame
from game_earth import EarthGame
from wordlist_en import WORD_DICT, WORD_LIST

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# 使用导入的单词字典和列表
word_dict = WORD_DICT
word_list = WORD_LIST

def main():
    # 初始化pygame
    pygame.init()
    try:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("英语学习游戏合集")
        audio_system = AudioSystem()
        print("音效系统初始化成功")
    except Exception as e:
        print(f"初始化失败: {e}")
        sys.exit(1)

    # 游戏字典
    games = {
        1: WhackAMoleGame(word_dict, word_list, SCREEN_WIDTH, SCREEN_HEIGHT),
        2: SandbagGame(word_dict, word_list, SCREEN_WIDTH, SCREEN_HEIGHT),
        3: MatchGame(word_dict, word_list, SCREEN_WIDTH, SCREEN_HEIGHT),
        4: SpellingGame(word_dict, word_list, SCREEN_WIDTH, SCREEN_HEIGHT),
        5: FlashcardGame(word_dict, word_list, SCREEN_WIDTH, SCREEN_HEIGHT),
        6: EarthGame(word_dict, word_list, SCREEN_WIDTH, SCREEN_HEIGHT)
    }

    clock = pygame.time.Clock()
    game_state = [0]  # 0: 菜单, 1-6: 对应游戏
    selected_option = 0
    menu_options = [
        "1. 单词打地鼠",
        "2. 掷沙包单词识别", 
        "3. 单词连连看",
        "4. 单词拼写挑战",
        "5. 单词闪卡记忆",
        "6. 拯救地球单词填空"
    ]
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                print(f"主程序接收到键盘事件: key={event.key}, unicode='{event.unicode}'")
                
                # 首先检查ESC键（特殊处理，不传递给游戏）
                if event.key == pygame.K_ESCAPE:
                    if game_state[0] == 0:  # 菜单界面
                        running = False
                    else:  # 游戏界面
                        game_state[0] = 0
                    continue  # 跳过后续处理
                
                # 强制处理所有键盘事件，确保小写字母键能被捕获
                if game_state[0] > 0 and game_state[0] in games:  # 游戏界面
                    if hasattr(games[game_state[0]], 'handle_key'):
                        print(f"强制传递键盘事件到游戏 {game_state[0]}: key={event.key}, unicode='{event.unicode}'")
                        games[game_state[0]].handle_key(event)
                        continue  # 跳过后续处理
                
                if game_state[0] == 0:  # 菜单界面
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        game_state[0] = selected_option + 1
                        if game_state[0] in games:
                            games[game_state[0]].start()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                
                else:  # 游戏界面
                    if event.key == pygame.K_r and game_state[0] == 1:
                        # 打地鼠游戏重新开始
                        games[1].start()
                        continue  # 跳过后续处理
                    else:
                        # 将键盘事件传递给当前游戏
                        if game_state[0] in games:
                            if hasattr(games[game_state[0]], 'handle_key'):
                                print(f"传递键盘事件到游戏 {game_state[0]}: {event.key}")
                                games[game_state[0]].handle_key(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_state[0] > 0 and game_state[0] in games:  # 游戏界面
                    if hasattr(games[game_state[0]], 'handle_click'):
                        games[game_state[0]].handle_click(event.pos)
        
        # 更新游戏状态
        if game_state[0] == 0:  # 菜单界面
            screen.fill(WHITE)
            title = render_chinese_text("英语学习游戏合集", 48, BLACK)
            screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
            
            for i, option in enumerate(menu_options):
                color = BLUE if i == selected_option else BLACK
                option_text = render_chinese_text(option, 36, color)
                screen.blit(option_text, (SCREEN_WIDTH//2 - option_text.get_width()//2, 150 + i * 60))
            
            hint_text = render_chinese_text("使用↑↓键选择游戏，回车键开始，ESC键退出", 18, GRAY)
            screen.blit(hint_text, (SCREEN_WIDTH//2 - hint_text.get_width()//2, 500))
        
        else:  # 游戏界面
            if game_state[0] in games:
                # 更新游戏逻辑
                if hasattr(games[game_state[0]], 'update'):
                    games[game_state[0]].update()
                
                # 绘制游戏界面
                if hasattr(games[game_state[0]], 'draw'):
                    games[game_state[0]].draw(screen)
                
                # 显示返回提示
                hint_text = render_chinese_text("按ESC键返回菜单", 18, GRAY)
                screen.blit(hint_text, (SCREEN_WIDTH - hint_text.get_width() - 20, 20))
            else:
                # 游戏不存在的情况
                screen.fill(WHITE)
                error_text = render_chinese_text("游戏正在开发中...", 36, RED)
                screen.blit(error_text, (SCREEN_WIDTH//2 - error_text.get_width()//2, SCREEN_HEIGHT//2))
                hint_text = render_chinese_text("按ESC键返回菜单", 18, GRAY)
                screen.blit(hint_text, (SCREEN_WIDTH//2 - hint_text.get_width()//2, SCREEN_HEIGHT//2 + 50))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()