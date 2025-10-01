#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单词连连看游戏模块
"""

import pygame
import random
from chinese_output import render_chinese_text

class MatchGame:
    """单词连连看游戏"""
    def __init__(self, word_dict, word_list, screen_width, screen_height):
        self.word_dict = word_dict
        self.word_list = word_list
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.score = 0
        self.english_words = []  # 左列英文单词
        self.chinese_meanings = []  # 右列中文释义
        self.selected_en = None  # 选中的英文单词索引
        self.selected_cn = None  # 选中的中文释义索引
        self.matched_pairs = []  # 已匹配的单词对
        self.is_running = True
        self.pair_count = 5  # 每次显示5对单词
    
    def start(self):
        self.score = 0
        self.is_running = True
        self.setup_game()
    
    def setup_game(self):
        # 随机选择单词
        words = random.sample(self.word_list, self.pair_count)
        
        # 左列：英文单词
        self.english_words = words.copy()
        random.shuffle(self.english_words)
        
        # 右列：中文释义（随机打乱）
        self.chinese_meanings = [self.word_dict[word] for word in words]
        random.shuffle(self.chinese_meanings)
        
        self.selected_en = None
        self.selected_cn = None
        self.matched_pairs = []
    
    def handle_click(self, pos):
        # 检查点击左列英文单词（调整点击区域）
        for i in range(len(self.english_words)):
            y_pos = 180 + i * 80
            if 80 <= pos[0] <= 320 and y_pos <= pos[1] <= y_pos + 60:
                self.select_english(i)
                break
        
        # 检查点击右列中文释义（调整点击区域）
        for i in range(len(self.chinese_meanings)):
            y_pos = 180 + i * 80
            if 380 <= pos[0] <= 620 and y_pos <= pos[1] <= y_pos + 60:
                self.select_chinese(i)
                break
    
    def select_english(self, index):
        if index in [pair[0] for pair in self.matched_pairs]:
            return  # 已匹配的单词不可选
        
        self.selected_en = index
        
        # 播放选中单词的发音
        try:
            from word_audio import AudioSystem
            audio = AudioSystem()
            word = self.english_words[index]
            audio.speak(word)
        except Exception as e:
            print(f"发音失败: {e}")
        
        self.check_match()
    
    def select_chinese(self, index):
        if index in [pair[1] for pair in self.matched_pairs]:
            return  # 已匹配的释义不可选
        
        self.selected_cn = index
        self.check_match()
    
    def check_match(self):
        if self.selected_en is not None and self.selected_cn is not None:
            en_word = self.english_words[self.selected_en]
            cn_meaning = self.chinese_meanings[self.selected_cn]
            
            # 检查是否匹配
            if self.word_dict[en_word] == cn_meaning:
                # 匹配成功
                self.matched_pairs.append((self.selected_en, self.selected_cn))
                self.score += 10
                
                # 检查是否全部匹配完成
                if len(self.matched_pairs) == self.pair_count:
                    # 全部匹配完成，重新生成新的一组词
                    self.setup_game()
            
            # 重置选中状态
            self.selected_en = None
            self.selected_cn = None
    
    def update(self):
        # 连连看游戏不需要实时更新
        pass
    
    def draw(self, screen):
        screen.fill((255, 255, 255))
        
        font = render_chinese_text("单词连连看", 36, (0, 0, 0))
        score_text = render_chinese_text(f"分数: {self.score}", 36, (0, 0, 0))
        
        screen.blit(font, (self.screen_width//2 - font.get_width()//2, 50))
        screen.blit(score_text, (self.screen_width - 200, 50))
        
        # 绘制列标题
        font_title = render_chinese_text("英文单词", 24, (0, 0, 255))
        cn_title = render_chinese_text("中文释义", 24, (0, 0, 255))
        
        screen.blit(font_title, (150, 120))
        screen.blit(cn_title, (450, 120))
        
        # 绘制左列：英文单词
        font_word = render_chinese_text("", 24, (255, 255, 255))
        for i, word in enumerate(self.english_words):
            y_pos = 180 + i * 80
            
            # 判断样式：检查该单词是否已匹配
            is_matched = any(pair[0] == i for pair in self.matched_pairs)
            if is_matched:  # 已匹配的单词
                color = (128, 128, 128)  # 灰色
                text_color = (255, 255, 255)
            elif self.selected_en == i:  # 选中的单词
                color = (0, 0, 255)  # 蓝色
                text_color = (255, 255, 255)
            else:  # 未选中的单词
                color = (0, 128, 0)  # 绿色
                text_color = (255, 255, 255)
            
            # 绘制单词框（扩大尺寸）
            pygame.draw.rect(screen, color, (80, y_pos, 240, 60), border_radius=8)
            word_text = render_chinese_text(word, 24, text_color)
            screen.blit(word_text, (200 - word_text.get_width()//2, y_pos + 30 - word_text.get_height()//2))
        
        # 绘制右列：中文释义
        for i, meaning in enumerate(self.chinese_meanings):
            y_pos = 180 + i * 80
            
            # 判断样式：检查该释义是否已匹配
            is_matched = any(pair[1] == i for pair in self.matched_pairs)
            if is_matched:  # 已匹配的释义
                color = (128, 128, 128)  # 灰色
                text_color = (255, 255, 255)
            elif self.selected_cn == i:  # 选中的释义
                color = (0, 0, 255)  # 蓝色
                text_color = (255, 255, 255)
            else:  # 未选中的释义
                color = (0, 128, 0)  # 绿色
                text_color = (255, 255, 255)
            
            # 绘制释义框（扩大尺寸）
            pygame.draw.rect(screen, color, (380, y_pos, 240, 60), border_radius=8)
            meaning_text = render_chinese_text(meaning, 24, text_color)
            screen.blit(meaning_text, (500 - meaning_text.get_width()//2, y_pos + 30 - meaning_text.get_height()//2))
        
        # 操作提示
        font_hint = render_chinese_text("点击左侧单词和右侧释义进行匹配，按ESC返回菜单", 18, (128, 128, 128))
        screen.blit(font_hint, (self.screen_width//2 - font_hint.get_width()//2, self.screen_height - 50))