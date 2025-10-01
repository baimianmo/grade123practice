#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单词发音模块
使用本地音频文件提供单词发音功能
"""

import pygame
import os
import threading

class AudioSystem:
    """音频系统类"""
    def __init__(self):
        self.sounds_dir = "sounds"
        self.is_initialized = True
        # 初始化pygame音频系统
        pygame.mixer.init()
        print("音频系统初始化成功")
    
    def speak(self, word):
        """发音单词"""
        try:
            # 处理特殊单词 "a/an" -> 使用 "a" 的发音
            audio_word = word
            if word == "a/an":
                audio_word = "a"
            
            # 处理文件名中的特殊字符，将斜杠替换为下划线
            filename_word = word.replace("/", "_")
            
            # 构建音频文件路径
            sound_file = os.path.join(self.sounds_dir, f"{filename_word}.wav")
            
            # 检查文件是否存在
            if not os.path.exists(sound_file):
                print(f"音频文件不存在: {sound_file}")
                return False
            
            # 播放音频
            sound = pygame.mixer.Sound(sound_file)
            sound.play()
            return True
            
        except Exception as e:
            print(f"发音失败: {e}")
            return False
    
    def play_sound(self, sound_file):
        """播放音效文件"""
        try:
            if not os.path.exists(sound_file):
                return False
            sound = pygame.mixer.Sound(sound_file)
            sound.play()
            return True
        except Exception as e:
            print(f"播放音效失败: {e}")
            return False