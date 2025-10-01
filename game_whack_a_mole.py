#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单词打地鼠游戏模块
"""

import pygame
import random
import time
from chinese_output import render_chinese_text
from word_audio import AudioSystem

class WhackAMoleGame:
    """打地鼠游戏"""
    def __init__(self, word_dict, word_list, screen_width, screen_height):
        self.word_dict = word_dict
        self.word_list = word_list
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.audio_system = AudioSystem()
        
        self.score = 0
        self.time_left = 60
        self.is_running = True
        self.grid_size = 3
        self.cell_width = 180  # 长方形宽度
        self.cell_height = 140  # 增加长方形高度
        self.moles = []
        self.last_spawn_time = 0
        self.spawn_rate = 1.5
        self.max_moles = 2
        self.game_start_time = time.time()
        
    def start(self):
        self.score = 0
        self.time_left = 60
        self.is_running = True
        self.moles = []
        self.game_start_time = time.time()
    
    def update(self):
        if not self.is_running:
            return
            
        # 更新游戏时间
        elapsed = time.time() - self.game_start_time
        self.time_left = max(0, 60 - elapsed)
        
        if self.time_left <= 0:
            self.is_running = False
            return
        
        # 生成新地鼠
        current_time = time.time()
        if current_time - self.last_spawn_time > self.spawn_rate and len(self.moles) < self.max_moles:
            self.spawn_mole()
            self.last_spawn_time = current_time
        
        # 更新地鼠状态
        self.moles = [mole for mole in self.moles if mole.update()]
    
    def spawn_mole(self):
        """生成新地鼠"""
        # 在网格位置生成地鼠
        row = random.randint(0, self.grid_size - 1)
        col = random.randint(0, self.grid_size - 1)
        
        # 计算长方形网格布局，与draw方法保持一致
        total_width = self.grid_size * self.cell_width
        margin_x = (self.screen_width - total_width) // 2
        margin_y = 150
        
        # 计算总高度并设置固定行间距不超过3px
        total_height = self.grid_size * self.cell_height
        available_height = self.screen_height - margin_y - 15  # 顶部边距和底部边距
        if total_height < available_height:
            row_spacing = min(3, (available_height - total_height) // (self.grid_size - 1))
        else:
            row_spacing = 0
        
        x = margin_x + col * self.cell_width + self.cell_width // 2
        y = margin_y + row * (self.cell_height + row_spacing) + self.cell_height // 2
        
        word = random.choice(self.word_list)
        self.moles.append(Mole(x, y, word, self.word_dict[word]))
    
    def handle_click(self, pos):
        if not self.is_running:
            return
            
        hit = False
        for mole in self.moles:
            if mole.is_clicked(pos):
                self.score += 10
                mole.is_hit = True
                mole.hit_time = time.time()
                # 播放单词发音
                try:
                    self.audio_system.speak(mole.word)
                except Exception as e:
                    print(f"发音失败: {e}")
                hit = True
                break
        
        if not hit:
            self.score = max(0, self.score - 5)
            # 点击空白区域也尝试播放提示音
            try:
                self.audio_system.speak("miss")
            except:
                pass
    
    def draw(self, screen):
        screen.fill((255, 255, 255))
        
        # 绘制游戏信息
        font = render_chinese_text("单词打地鼠", 36, (0, 0, 0))
        score_text = render_chinese_text(f"分数: {self.score}", 36, (0, 0, 0))
        time_text = render_chinese_text(f"时间: {int(self.time_left)}秒", 36, (0, 0, 0))
        
        screen.blit(font, (self.screen_width//2 - font.get_width()//2, 30))
        screen.blit(score_text, (50, 100))
        screen.blit(time_text, (self.screen_width - 200, 100))
        
        # 绘制长方形网格背景
        total_width = self.grid_size * self.cell_width
        margin_x = (self.screen_width - total_width) // 2
        margin_y = 150
        
        # 计算总高度并设置固定行间距不超过3px
        total_height = self.grid_size * self.cell_height
        available_height = self.screen_height - margin_y - 15  # 顶部边距和底部边距
        if total_height < available_height:
            # 设置固定行间距不超过3px
            row_spacing = min(3, (available_height - total_height) // (self.grid_size - 1))
        else:
            row_spacing = 0
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x = margin_x + j * self.cell_width
                y = margin_y + i * (self.cell_height + row_spacing)
                
                pygame.draw.rect(screen, (240, 240, 240), (x, y, self.cell_width, self.cell_height), border_radius=10)
                pygame.draw.rect(screen, (200, 200, 200), (x, y, self.cell_width, self.cell_height), 2, border_radius=10)
        
        # 绘制地鼠
        for mole in self.moles:
            mole.draw(screen)
        
        # 游戏结束画面
        if not self.is_running:
            self.draw_game_over(screen)
    
    def draw_game_over(self, screen):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        font = render_chinese_text("游戏结束!", 36, (255, 255, 255))
        final_score = render_chinese_text(f"最终分数: {self.score}", 36, (255, 255, 255))
        restart = render_chinese_text("按R键重新开始，按ESC返回菜单", 24, (255, 255, 255))
        
        screen.blit(font, (self.screen_width//2 - font.get_width()//2, 250))
        screen.blit(final_score, (self.screen_width//2 - final_score.get_width()//2, 320))
        screen.blit(restart, (self.screen_width//2 - restart.get_width()//2, 380))

class Mole:
    """地鼠类"""
    def __init__(self, x, y, word, chinese):
        self.x = x
        self.y = y
        self.word = word
        self.chinese = chinese
        self.appear_time = time.time()
        self.show_time = random.uniform(1.0, 2.0)
        self.is_hit = False
        self.hit_time = 0
        # 加载背景图片
        try:
            self.background_image = pygame.image.load("assets/img/flag.png")
            # 调整图片大小以适应地鼠框
            self.background_image = pygame.transform.scale(self.background_image, (120, 100))
        except:
            self.background_image = None
    
    def update(self):
        current_time = time.time()
        
        if self.is_hit:
            if current_time - self.hit_time > 1.0:
                return False
            return True
            
        if current_time - self.appear_time > self.show_time:
            return False
            
        return True
    
    def is_clicked(self, pos):
        width, height = 120, 100  # 更新点击检测区域高度
        # 检查点击是否在长方形区域内
        return (self.x - width//2 <= pos[0] <= self.x + width//2 and 
                self.y - height//2 <= pos[1] <= self.y + height//2)
    
    def draw(self, screen):
        # 绘制长方形地鼠
        width, height = 120, 100  # 增加地鼠框高度
        
        if not self.is_hit:
            # 未击中时显示背景图片
            if self.background_image:
                screen.blit(self.background_image, (self.x - width//2, self.y - height//2))
            else:
                # 如果没有图片，使用默认颜色
                color = (160, 82, 45)  # 棕色
                pygame.draw.rect(screen, color, (self.x - width//2, self.y - height//2, width, height), border_radius=10)
        
        # 绘制英文单词（顶部）- 击中后放大字体
        if self.is_hit:
            # 击中后放大字体并加粗显示
            font_en = pygame.font.SysFont('Arial', 28, bold=True)  # 从22增加到28
            text_surface = font_en.render(self.word, True, (0, 0, 0))  # 黑色，高对比度
        else:
            font_en = pygame.font.SysFont('Arial', 20)  # 保持20号字体
            text_surface = font_en.render(self.word, True, (255, 255, 0))  # 黄色，在背景上更显眼
        screen.blit(text_surface, (self.x - text_surface.get_width()//2, self.y - height//2 + 15))
        
        # 如果被击中，显示中文释义（底部）- 放大字体
        if self.is_hit:
            font_cn = render_chinese_text(self.chinese, 22, (255, 0, 0), bold=True)  # 从16增加到22，红色，高对比度
            screen.blit(font_cn, (self.x - font_cn.get_width()//2, self.y + height//2 - 30))
        else:
            # 未击中时显示提示
            hint_font = render_chinese_text("点击我!", 14, (255, 255, 255))  # 白色，在背景上清晰可见
            screen.blit(hint_font, (self.x - hint_font.get_width()//2, self.y + height//2 - 25))