#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单词拼写游戏模块 - 按钮版本
使用按钮界面进行单词拼写
"""

from pygame.rect import Rect
import pygame
import random
from chinese_output import render_chinese_text
from word_audio import AudioSystem

class SpellingGame:
    """单词拼写游戏（按钮版本）"""
    def __init__(self, word_dict, word_list, screen_width, screen_height):
        self.word_dict = word_dict
        self.word_list = word_list
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.audio_system = AudioSystem()
        
        self.score = 0
        self.current_word = ""
        self.user_input = ""
        self.is_running = True
        self.message = ""
        self.message_timer = 0
        self.input_active = False  # 输入框激活状态
        
        # 字母按钮配置 - 每行9个字母（26个字母分成3行）
        self.letters = "abcdefghijklmnopqrstuvwxyz"
        self.button_size = 40
        self.button_margin = 6
        self.buttons_start_y = 350
        # 功能按钮起始X坐标
        self.function_buttons_x = 450
        
    def start(self):
        self.score = 0
        self.is_running = True
        self.user_input = ""
        self.message = ""
        self.input_active = False
        self.delayed_next_word = False  # 初始化延迟切换标志
        self.next_word()
    
    def next_word(self):
        self.current_word = random.choice(self.word_list)
        self.user_input = ""
        self.message = f"请输入单词: {self.word_dict[self.current_word]}"
        # 播放单词发音
        try:
            self.audio_system.speak(self.current_word)
        except:
            pass
    
    def handle_click(self, pos):
        # 检查字母按钮点击（9列3行布局）
        for i, letter in enumerate(self.letters):
            row = i // 9
            col = i % 9
            x = 40 + col * (self.button_size + self.button_margin)
            y = self.buttons_start_y + row * (self.button_size + self.button_margin)
            button_rect = pygame.Rect(x, y, self.button_size, self.button_size)
            
            if button_rect.collidepoint(pos):
                self.user_input += letter
                return
        
        # 检查删除按钮（右侧第一行，距离3px）
        delete_rect = pygame.Rect(self.function_buttons_x, self.buttons_start_y, 
                                self.button_size * 2 + self.button_margin, self.button_size)
        if delete_rect.collidepoint(pos):
            self.user_input = self.user_input[:-1]
            return
        
        # 检查提交按钮（右侧第二行，距离3px）
        submit_rect = pygame.Rect(self.function_buttons_x, self.buttons_start_y + (self.button_size + self.button_margin),
                                self.button_size * 2 + self.button_margin, self.button_size)
        if submit_rect.collidepoint(pos):
            self.check_spelling()
            return
        
        # 检查跳过按钮（右侧第三行，距离3px）
        skip_rect = pygame.Rect(self.function_buttons_x, self.buttons_start_y + 2 * (self.button_size + self.button_margin),
                              self.button_size * 2 + self.button_margin, self.button_size)
        if skip_rect.collidepoint(pos):
            self.next_word()
            return
        
        # 检查输入框点击（激活键盘输入）
        input_box_rect = pygame.Rect(200, 200, 400, 60)
        if input_box_rect.collidepoint(pos):
            self.input_active = True
            return
    
    def handle_key(self, event):
        if not self.input_active:
            return
            
        if event.key == pygame.K_RETURN:
            self.check_spelling()
        elif event.key == pygame.K_BACKSPACE:
            self.user_input = self.user_input[:-1]
        elif event.key == pygame.K_ESCAPE:
            self.input_active = False
        elif pygame.K_a <= event.key <= pygame.K_z:
            # 处理字母键输入
            letter = chr(event.key)
            self.user_input += letter
        elif event.key == pygame.K_SPACE:
            self.user_input += " "
        elif event.key == pygame.K_MINUS:
            # 处理连字符输入
            self.user_input += "-"
    
    def check_spelling(self):
        if self.user_input.lower() == self.current_word.lower():
            self.score += 10
            self.message = "拼写正确！+10分"
            self.message_timer = pygame.time.get_ticks() + 1500  # 停顿1.5秒
            # 延迟切换单词
            self.delayed_next_word = True
            return True
        else:
            self.score = max(0, self.score - 5)
            self.message = f"拼写错误！正确答案: {self.current_word}"
            self.message_timer = pygame.time.get_ticks() + 2000
            return False
    
    def update(self):
        if self.message_timer > 0 and pygame.time.get_ticks() > self.message_timer:
            self.message = f"请输入单词: {self.word_dict[self.current_word]}"
            self.message_timer = 0
            # 延迟切换单词
            if hasattr(self, 'delayed_next_word') and self.delayed_next_word:
                self.next_word()
                self.delayed_next_word = False
    
    def draw(self, screen):
        screen.fill((255, 255, 255))
        
        title = render_chinese_text("单词拼写挑战", 36, (0, 0, 0))
        score_text = render_chinese_text(f"分数: {self.score}", 36, (0, 0, 0))
        
        screen.blit(title, (self.screen_width//2 - title.get_width()//2, 50))
        screen.blit(score_text, (self.screen_width - 200, 50))
        
        # 显示提示信息
        message_text = render_chinese_text(self.message, 24, (0, 0, 255))
        screen.blit(message_text, (self.screen_width//2 - message_text.get_width()//2, 120))
        
        # 显示当前单词的中文意思
        #meaning_text = render_chinese_text(f"中文意思: {self.word_dict[self.current_word]}", 24, (100, 100, 100))
        #screen.blit(meaning_text, (self.screen_width//2 - meaning_text.get_width()//2, 160))
        
        # 简化显示：只显示输入文本，不显示输入框背景
        input_text = render_chinese_text(self.user_input, 32, (0, 0, 0))
        if self.user_input:
            screen.blit(input_text, (self.screen_width//2 - input_text.get_width()//2, 215))
        else:
            placeholder = render_chinese_text("点击下方字母按钮输入", 20, (150, 150, 150))
            screen.blit(placeholder, (self.screen_width//2 - placeholder.get_width()//2, 220))
        
        # 绘制字母按钮（9列3行布局）
        for i, letter in enumerate(self.letters):
            row = i // 9
            col = i % 9
            x = 40 + col * (self.button_size + self.button_margin)
            y = self.buttons_start_y + row * (self.button_size + self.button_margin)
            
            # 绘制按钮
            button_rect = pygame.Rect(x, y, self.button_size, self.button_size)
            pygame.draw.rect(screen, (100, 150, 255), button_rect, border_radius=8)
            pygame.draw.rect(screen, (0, 0, 200), button_rect, 2, border_radius=8)
            
            # 绘制字母
            font = pygame.font.SysFont('Arial', 20)
            letter_text = font.render(letter.upper(), True, (255, 255, 255))
            screen.blit(letter_text, (x + self.button_size//2 - letter_text.get_width()//2, 
                                    y + self.button_size//2 - letter_text.get_height()//2))
        
        # 绘制删除按钮（右侧第一行，距离3px）
        delete_rect = pygame.Rect(self.function_buttons_x, self.buttons_start_y, 
                                self.button_size * 2 + self.button_margin, self.button_size)
        pygame.draw.rect(screen, (255, 100, 100), delete_rect, border_radius=8)
        pygame.draw.rect(screen, (200, 0, 0), delete_rect, 2, border_radius=8)
        
        delete_text = render_chinese_text("删除", 16, (255, 255, 255))
        screen.blit(delete_text, (delete_rect.centerx - delete_text.get_width()//2, 
                                delete_rect.centery - delete_text.get_height()//2))
        
        # 绘制提交按钮（右侧第二行，距离3px）
        submit_rect = pygame.Rect(self.function_buttons_x, self.buttons_start_y + (self.button_size + self.button_margin),
                                self.button_size * 2 + self.button_margin, self.button_size)
        pygame.draw.rect(screen, (100, 255, 100), submit_rect, border_radius=8)
        pygame.draw.rect(screen, (0, 200, 0), submit_rect, 2, border_radius=8)
        
        submit_text = render_chinese_text("提交", 16, (255, 255, 255))
        screen.blit(submit_text, (submit_rect.centerx - submit_text.get_width()//2, 
                                submit_rect.centery - submit_text.get_height()//2))
        
        # 绘制跳过按钮（右侧第三行，距离3px）
        skip_rect = pygame.Rect(self.function_buttons_x, self.buttons_start_y + 2 * (self.button_size + self.button_margin),
                              self.button_size * 2 + self.button_margin, self.button_size)
        pygame.draw.rect(screen, (255, 200, 100), skip_rect, border_radius=8)
        pygame.draw.rect(screen, (200, 150, 0), skip_rect, 2, border_radius=8)
        
        skip_text = render_chinese_text("跳过", 16, (255, 255, 255))
        screen.blit(skip_text, (skip_rect.centerx - skip_text.get_width()//2, 
                              skip_rect.centery - skip_text.get_height()//2))
        
        # 移除输入框背景，只保留状态指示
        input_box_rect: Rect = pygame.Rect(200, 200, 400, 60)
        if self.input_active:
            # 键盘激活时显示绿色边框
            pygame.draw.rect(screen, (0, 200, 0), input_box_rect, 2, border_radius=8)
            #active_text = render_chinese_text("✓", 16, (0, 150, 0))
            #screen.blit(active_text, (input_box_rect.right + 5, input_box_rect.centery - active_text.get_height()//2))
        else:
            # 键盘未激活时显示蓝色边框
            pygame.draw.rect(screen, (0, 0, 200), input_box_rect, 2, border_radius=8)
            #inactive_text = render_chinese_text("✗", 16, (150, 0, 0))
            #screen.blit(inactive_text, (input_box_rect.right + 5, input_box_rect.centery - inactive_text.get_height()//2))
        
        # 操作提示
        hint1 = render_chinese_text("点击字母按钮输入单词", 18, (100, 100, 100))
        hint2 = render_chinese_text("按ESC返回菜单", 18, (100, 100, 100))
        
        screen.blit(hint1, (self.screen_width//2 - hint1.get_width()//2, 550))
        screen.blit(hint2, (self.screen_width//2 - hint2.get_width()//2, 580))