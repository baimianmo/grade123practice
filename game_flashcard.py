#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单词闪卡游戏模块
"""

import pygame
import random
from chinese_output import render_chinese_text
from word_audio import AudioSystem

class FlashcardGame:
    """单词闪卡游戏"""
    def __init__(self, word_dict, word_list, screen_width, screen_height):
        self.word_dict = word_dict
        self.word_list = word_list
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.audio_system = AudioSystem()
        
        self.score = 0
        self.current_word = ""
        self.show_meaning = False
        self.is_running = True
        self.cards_remaining = 20
        self.correct_count = 0
        self.card_index = 0
        self.card_words = []
    
    def start(self):
        self.score = 0
        self.is_running = True
        self.show_meaning = False
        self.cards_remaining = 20
        self.correct_count = 0
        self.card_index = 0
        self.card_words = random.sample(self.word_list, min(20, len(self.word_list)))
        self.current_word = self.card_words[0]
        # 播放第一个单词发音
        try:
            self.audio_system.speak(self.current_word)
        except:
            pass
    
    def next_card_from_pool(self):
        if self.cards_remaining > 0:
            self.current_word = random.choice(self.word_list)
            self.show_meaning = False
            self.cards_remaining -= 1
            # 播放单词发音
            try:
                self.audio_system.speak(self.current_word)
            except:
                pass
        else:
            self.is_running = False
    
    def next_card(self):
        if self.cards_remaining > 0:
            self.current_word = random.choice(self.word_list)
            self.show_meaning = False
            self.cards_remaining -= 1
        else:
            self.is_running = False
    
    def handle_key(self, key):
        if key == pygame.K_SPACE:
            # 反复切换显示英文单词和中文意思
            self.show_meaning = not self.show_meaning
        elif key == pygame.K_LEFT:
            self.previous_card()
        elif key == pygame.K_RIGHT:
            self.next_card()
        elif key == pygame.K_y or key == pygame.K_1:
            self.mark_correct()
        elif key == pygame.K_n or key == pygame.K_2:
            self.mark_incorrect()
    
    def previous_card(self):
        if self.card_index > 0:
            self.card_index -= 1
            self.current_word = self.card_words[self.card_index]
            self.show_meaning = False
    
    def next_card(self):
        if self.card_index < len(self.card_words) - 1:
            self.card_index += 1
            self.current_word = self.card_words[self.card_index]
            self.show_meaning = False
        elif self.cards_remaining > 0:
            self.next_card_from_pool()
    
    def reveal_meaning(self):
        self.show_meaning = True
    
    def mark_correct(self):
        if self.show_meaning:
            self.score += 5
            self.correct_count += 1
            self.next_card()
    
    def mark_incorrect(self):
        if self.show_meaning:
            self.score = max(0, self.score - 2)
            self.next_card()
    
    def update(self):
        pass
    
    def draw(self, screen):
        screen.fill((255, 255, 255))
        
        title = render_chinese_text("单词闪卡记忆", 36, (0, 0, 0))
        score_text = render_chinese_text(f"分数: {self.score}", 36, (0, 0, 0))
        remaining_text = render_chinese_text(f"剩余卡片: {self.cards_remaining}", 24, (100, 100, 100))
        
        screen.blit(title, (self.screen_width//2 - title.get_width()//2, 50))
        screen.blit(score_text, (self.screen_width - 200, 50))
        screen.blit(remaining_text, (50, 100))
        
        # 显示卡片
        card_color = (70, 130, 180) if not self.show_meaning else (50, 150, 50)
        pygame.draw.rect(screen, card_color, (150, 200, 500, 200), border_radius=15)
        
        if not self.show_meaning:
            # 显示英文单词
            word_text = render_chinese_text(self.current_word, 48, (255, 255, 255))
            screen.blit(word_text, (self.screen_width//2 - word_text.get_width()//2, 280))
            
            hint_text = render_chinese_text("按空格键显示中文意思", 20, (200, 200, 200))
            screen.blit(hint_text, (self.screen_width//2 - hint_text.get_width()//2, 350))
        else:
            # 显示中文意思
            meaning_text = render_chinese_text(self.word_dict[self.current_word], 36, (255, 255, 255))
            screen.blit(meaning_text, (self.screen_width//2 - meaning_text.get_width()//2, 250))
            
            # 显示选项按钮
            pygame.draw.rect(screen, (50, 200, 50), (200, 320, 150, 50), border_radius=10)
            pygame.draw.rect(screen, (200, 50, 50), (450, 320, 150, 50), border_radius=10)
            
            correct_text = render_chinese_text("认识", 24, (255, 255, 255))
            incorrect_text = render_chinese_text("不认识", 24, (255, 255, 255))
            
            screen.blit(correct_text, (275 - correct_text.get_width()//2, 335))
            screen.blit(incorrect_text, (525 - incorrect_text.get_width()//2, 335))
            
            # 添加反复切换提示
            toggle_hint = render_chinese_text("按空格键返回英文单词", 20, (200, 200, 200))
            screen.blit(toggle_hint, (self.screen_width//2 - toggle_hint.get_width()//2, 380))
        
        # 游戏结束画面
        if not self.is_running:
            overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            
            result_text = render_chinese_text(f"学习完成！正确率: {self.correct_count}/20", 36, (255, 255, 255))
            final_score = render_chinese_text(f"最终分数: {self.score}", 36, (255, 255, 255))
            restart_text = render_chinese_text("按ESC返回菜单", 24, (255, 255, 255))
            
            screen.blit(result_text, (self.screen_width//2 - result_text.get_width()//2, 250))
            screen.blit(final_score, (self.screen_width//2 - final_score.get_width()//2, 300))
            screen.blit(restart_text, (self.screen_width//2 - restart_text.get_width()//2, 350))