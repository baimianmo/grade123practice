#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
拯救地球单词填空游戏模块
"""

import pygame
import random
from chinese_output import render_chinese_text
from word_audio import AudioSystem

class EarthGame:
    """拯救地球单词填空游戏"""
    def __init__(self, word_dict, word_list, screen_width, screen_height):
        self.word_dict = word_dict
        self.word_list = word_list
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # 初始化音频系统
        self.audio_system = AudioSystem()
        
        # 初始化游戏状态
        self.reset_game()
    
    def reset_game(self):
        """重置游戏状态"""
        self.score = 0
        self.current_word = ""
        self.missing_letter = ""
        self.user_input = ""
        self.is_running = True
        self.earth_health = 100
        self.level = 1
        self.message = ""
        self.input_active = True  # 游戏开始时输入激活
        self.pause_timer = 0
        self.word_paused = False
        self.completed_word = ""
        self.display_word = ""
        self.word_y = 0
        self.word_speed = 2
    
    def start(self):
        self.reset_game()
        self.message = "拯救地球！填写正确的字母"
        self.next_puzzle()
    
    def next_puzzle(self):
        if self.earth_health > 0:
            self.current_word = random.choice([w for w in self.word_list if len(w) > 3])
            
            # 单词开始降落时发音（非阻塞方式）
            try:
                self.audio_system.speak(self.current_word)
            except Exception as e:
                print(f"发音错误: {e}")
            
            # 随机隐藏一个字母，用_代替
            hide_pos = random.randint(0, len(self.current_word) - 1)
            self.missing_letter = self.current_word[hide_pos]
            self.user_input = ""
            self.input_active = True
            self.display_word = self.current_word[:hide_pos] + "_" + self.current_word[hide_pos+1:]
            self.word_y = -50  # 从上方开始降落
            self.word_speed = 2
            self.word_paused = False
            self.completed_word = ""
            self.message = f"拯救地球！填写正确的字母"
        else:
            self.is_running = False
            self.input_active = False
    
    def handle_key(self, event):
        if not self.input_active:
            print("输入未激活")
            return
            
        # 调试输出，确认键盘事件被接收
        print(f"拯救地球游戏接收到键盘事件: key={event.key}, unicode='{event.unicode}', 当前输入: '{self.user_input}'")
        
        # 使用unicode属性处理所有字母输入（最可靠的方法）
        if event.unicode and event.unicode.isalpha():
            self.user_input += event.unicode.lower()
            print(f"通过unicode处理字母后: '{self.user_input}'")
            return
            
        # 特殊功能键处理
        if event.key == pygame.K_BACKSPACE:
            self.user_input = self.user_input[:-1]
            print(f"删除后输入: '{self.user_input}'")
        elif event.key == pygame.K_RETURN:
            if self.user_input:
                print(f"提交答案: '{self.user_input}'")
                self.check_answer()
            else:
                print("回车键按下，但输入为空")
        # ESC键现在由主程序统一处理，不需要在游戏中单独处理
        else:
            print(f"未处理的键盘事件: key={event.key}, unicode='{event.unicode}'")
    
    def check_answer(self):
        if self.user_input.lower() == self.missing_letter.lower():
            # 正确输入：显示完整单词，暂停降落，发音
            self.score += 10
            self.earth_health = min(100, self.earth_health + 5)
            self.level += 1
            self.message = "正确！地球更健康了！"
            self.completed_word = self.current_word
            self.word_paused = True
            self.pause_timer = pygame.time.get_ticks() + 1000  # 暂停1秒
            return True
        else:
            # 错误输入：停顿0.5秒
            self.score = max(0, self.score - 5)
            self.earth_health = max(0, self.earth_health - 10)
            self.message = f"错误！正确答案是: {self.missing_letter}"
            self.word_paused = True
            self.pause_timer = pygame.time.get_ticks() + 500  # 暂停0.5秒
            if self.earth_health <= 0:
                self.is_running = False
            return False
    
    def update(self):
        # 处理暂停计时器
        if self.word_paused and pygame.time.get_ticks() > self.pause_timer:
            self.word_paused = False
            # 不清空user_input，保留用户输入
            self.input_active = True
            self.completed_word = ""
            if self.earth_health > 0:
                self.next_puzzle()
        
        # 单词降落逻辑（仅在未暂停时）
        if self.is_running and self.earth_health > 0 and not self.word_paused:
            if hasattr(self, 'word_y') and hasattr(self, 'word_speed'):
                self.word_y += self.word_speed
                # 如果单词落到地球位置
                if self.word_y > 250:
                    self.earth_health = max(0, self.earth_health - 10)
                    if self.earth_health > 0:
                        self.next_puzzle()
                    else:
                        self.is_running = False
    
    def draw(self, screen):
        screen.fill((30, 30, 50))  # 深蓝色背景，太空主题
        
        title = render_chinese_text("拯救地球单词填空", 36, (255, 255, 255))
        score_text = render_chinese_text(f"分数: {self.score}", 36, (255, 255, 255))
        level_text = render_chinese_text(f"关卡: {self.level}", 24, (200, 200, 200))
        
        screen.blit(title, (self.screen_width//2 - title.get_width()//2, 30))
        screen.blit(score_text, (self.screen_width - 200, 30))
        screen.blit(level_text, (50, 80))
        
        # 显示输入状态（调试信息）
        status_text = render_chinese_text(f"输入状态: {'激活' if self.input_active else '未激活'}", 18, (255, 255, 255))
        screen.blit(status_text, (50, 120))
        
        # 绘制地球
        earth_color = (0, min(255, int(self.earth_health * 2.55)), 0)  # 根据健康度改变颜色
        pygame.draw.circle(screen, earth_color, (self.screen_width//2, 250), 80)
        
        # 显示降落的单词
        if hasattr(self, 'display_word') and hasattr(self, 'word_y'):
            if self.completed_word:
                # 显示完整的单词（正确输入时）
                word_text = render_chinese_text(self.completed_word, 24, (0, 255, 0))
            else:
                word_text = render_chinese_text(self.display_word, 24, (255, 255, 255))
            screen.blit(word_text, (self.screen_width//2 - word_text.get_width()//2, self.word_y))
        
        # 显示健康度
        health_text = render_chinese_text(f"地球健康度: {self.earth_health}%", 24, (255, 255, 255))
        screen.blit(health_text, (self.screen_width//2 - health_text.get_width()//2, 350))
        
        # 显示谜题
        puzzle_text = render_chinese_text(self.message, 28, (255, 255, 255))
        screen.blit(puzzle_text, (self.screen_width//2 - puzzle_text.get_width()//2, 400))
        
        # 显示输入框和用户输入
        input_box_rect = pygame.Rect(300, 450, 200, 50)
        pygame.draw.rect(screen, (255, 255, 255), input_box_rect, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 255), input_box_rect, 2, border_radius=8)
        
        if self.user_input:
            input_text = render_chinese_text(self.user_input, 36, (0, 0, 0))
            screen.blit(input_text, (self.screen_width//2 - input_text.get_width()//2, 465))
        else:
            placeholder = render_chinese_text("输入字母", 20, (150, 150, 150))
            screen.blit(placeholder, (self.screen_width//2 - placeholder.get_width()//2, 465))
        
        # 显示操作提示
        hint_text = render_chinese_text("按回车键提交答案", 18, (200, 200, 200))
        screen.blit(hint_text, (self.screen_width//2 - hint_text.get_width()//2, 520))
        
        # 游戏结束画面
        if not self.is_running:
            overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))
            
            if self.earth_health <= 0:
                result_text = render_chinese_text("地球被摧毁了！", 48, (255, 0, 0))
            else:
                result_text = render_chinese_text("成功拯救地球！", 48, (0, 255, 0))
            
            final_score = render_chinese_text(f"最终分数: {self.score}", 36, (255, 255, 255))
            restart_text = render_chinese_text("按ESC返回菜单", 24, (255, 255, 255))
            
            screen.blit(result_text, (self.screen_width//2 - result_text.get_width()//2, 250))
            screen.blit(final_score, (self.screen_width//2 - final_score.get_width()//2, 320))
            screen.blit(restart_text, (self.screen_width//2 - restart_text.get_width()//2, 380))