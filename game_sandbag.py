#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
掷沙包单词识别游戏模块
一次出现15对单词，随机选择一个发音，点击正确的单词
"""

import pygame
import random
from chinese_output import render_chinese_text
from word_audio import AudioSystem

class SandbagGame:
    """掷沙包游戏"""
    def __init__(self, word_dict, word_list, screen_width, screen_height):
        self.word_dict = word_dict
        self.word_list = word_list
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.audio_system = AudioSystem()
        
        self.score = 0
        self.current_word = ""
        self.word_pairs = []
        self.is_running = True
        self.message = ""
        self.message_timer = 0
        self.selected_word = None
        self.selection_timer = 0
        self.selection_result = None  # "correct" or "wrong"
    
    def start(self):
        self.score = 0
        self.is_running = True
        self.message = ""
        self.selected_word = None
        self.selection_timer = 0
        self.selection_result = None
        self.generate_word_pairs()
        self.select_random_word()
    
    def generate_word_pairs(self):
        # 生成9对单词
        selected_words = random.sample(self.word_list, min(9, len(self.word_list)))
        self.word_pairs = [(word, self.word_dict[word]) for word in selected_words]
    
    def select_random_word(self):
        if self.word_pairs:
            self.current_word = random.choice(self.word_pairs)[0]
            # 播放单词发音
            try:
                self.audio_system.speak(self.current_word)
            except:
                pass
    
    def handle_click(self, pos):
        # 计算play again按钮位置（与draw方法保持一致）
        current_label = render_chinese_text("当前发音:", 24, (0, 0, 255))
        label_width = current_label.get_width()
        button_width = 120
        total_width = label_width + 5 + button_width
        start_x = self.screen_width//2 - total_width//2
        
        # 检查是否点击了play again按钮
        play_button_rect = pygame.Rect(start_x + label_width + 5, 82, button_width, 30)  # 再向下移动4px
        if play_button_rect.collidepoint(pos):
            # 重新播放当前单词发音
            try:
                self.audio_system.speak(self.current_word)
            except:
                pass
            return True
        
        # 检查点击了哪个单词
        for i, (word, meaning) in enumerate(self.word_pairs):
            row = i // 3
            col = i % 3
            x = 80 + col * 220  # 增加宽度，调整间距
            y = 150 + row * 120  # 调整行间距
            
            if x <= pos[0] <= x + 200 and y <= pos[1] <= y + 100:  # 增加方框宽度
                self.selected_word = i
                self.selection_timer = pygame.time.get_ticks() + 1500  # 1.5秒
                
                if word == self.current_word:
                    self.score += 10
                    self.message = "正确！+10分"
                    self.selection_result = "correct"
                    self.message_timer = pygame.time.get_ticks() + 1000
                    # 停留1秒后再切换
                    self.selection_timer = pygame.time.get_ticks() + 1000
                    return True
                else:
                    self.score = max(0, self.score - 5)
                    self.message = "错误！-5分"
                    self.selection_result = "wrong"
                    self.message_timer = pygame.time.get_ticks() + 1000
                    # 停留1秒后再切换
                    self.selection_timer = pygame.time.get_ticks() + 1000
                    return False
        return False
    
    def update(self):
        if self.message_timer > 0 and pygame.time.get_ticks() > self.message_timer:
            self.message = ""
            self.message_timer = 0
        
        # 检查选择结果计时器
        if self.selection_timer > 0 and pygame.time.get_ticks() > self.selection_timer:
            # 停留1秒后切换前恢复样式并生成新单词
            self.selected_word = None
            self.selection_timer = 0
            self.selection_result = None
            # 生成新单词对并选择下一个单词
            self.generate_word_pairs()
            self.select_random_word()
    
    def draw(self, screen):
        screen.fill((255, 255, 255))
        
        title = render_chinese_text("掷沙包单词识别", 36, (0, 0, 0))
        score_text = render_chinese_text(f"分数: {self.score}", 36, (0, 0, 0))
        current_label = render_chinese_text("当前发音:", 24, (0, 0, 255))
        
        screen.blit(title, (self.screen_width//2 - title.get_width()//2, 30))
        screen.blit(score_text, (self.screen_width - 200, 30))
        
        # 计算居中对齐的布局
        label_width = current_label.get_width()
        button_width = 120
        total_width = label_width + 5 + button_width  # 5px间距
        start_x = self.screen_width//2 - total_width//2
        
        # 绘制当前发音标签
        screen.blit(current_label, (start_x, 80))
        
        # 绘制play again按钮，保持5px间距
        play_button_rect = pygame.Rect(start_x + label_width + 5, 82, button_width, 30)  # 再向下移动4px
        pygame.draw.rect(screen, (100, 150, 255), play_button_rect, border_radius=5)
        play_text = render_chinese_text("play again", 16, (255, 255, 255))
        screen.blit(play_text, (play_button_rect.centerx - play_text.get_width()//2, 
                               play_button_rect.centery - play_text.get_height()//2))
        
        # 显示消息
        if self.message:
            msg_text = render_chinese_text(self.message, 24, (255, 0, 0))
            screen.blit(msg_text, (self.screen_width//2 - msg_text.get_width()//2, 110))
        
        # 绘制9个单词按钮（3行×3列）
        for i, (word, meaning) in enumerate(self.word_pairs):
            row = i // 3
            col = i % 3
            x = 80 + col * 220  # 增加宽度，调整间距
            y = 150 + row * 120  # 调整行间距
            
            # 所有单词使用相同样式，只有在选择后才区分
            if self.selected_word == i:
                # 选择正确变绿色，选择错误变红色
                if self.selection_result == "correct":
                    color = (0, 255, 0)  # 绿色
                elif self.selection_result == "wrong":
                    color = (255, 0, 0)  # 红色
                else:
                    color = (200, 200, 200)  # 默认灰色
            else:
                color = (200, 200, 200)  # 默认灰色
            
            pygame.draw.rect(screen, color, (x, y, 200, 100), border_radius=12)  # 增加方框宽度
            
            # 选中后加粗显示
            if self.selected_word == i:
                word_text = render_chinese_text(word, 32, (0, 0, 0), bold=True)  # 增大字号并加粗
            else:
                word_text = render_chinese_text(word, 32, (0, 0, 0))  # 增大字号
            
            screen.blit(word_text, (x + 100 - word_text.get_width()//2, y + 40))  # 调整位置
        
        # 操作提示
        hint_text = render_chinese_text("点击听到发音的单词，按ESC返回菜单", 18, (100, 100, 100))
        screen.blit(hint_text, (self.screen_width//2 - hint_text.get_width()//2, self.screen_height - 40))