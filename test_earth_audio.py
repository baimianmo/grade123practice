#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试拯救地球游戏发音功能
"""

import pygame
import random
from game_earth import EarthGame

def test_earth_audio():
    """测试拯救地球游戏发音"""
    print("测试拯救地球游戏发音功能...")
    
    # 模拟单词列表
    word_list = ["apple", "book", "cat", "dog", "elephant", "fish", "grape", "house"]
    word_dict = {word: word for word in word_list}
    
    # 创建游戏实例
    game = EarthGame(word_dict, word_list, 800, 600)
    game.start()
    
    print("测试连续生成单词并发音...")
    
    # 模拟连续生成5个单词
    for i in range(5):
        print(f"\n--- 第 {i+1} 个单词 ---")
        game.next_puzzle()
        print(f"当前单词: {game.current_word}")
        print(f"显示单词: {game.display_word}")
        print(f"缺失字母: {game.missing_letter}")
        
        # 等待发音完成
        import time
        time.sleep(2)  # 等待2秒让发音完成
    
    print("\n测试完成！")

if __name__ == "__main__":
    test_earth_audio()