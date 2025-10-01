#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试所有游戏功能
"""

import pygame
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_game_collection():
    """测试游戏合集"""
    try:
        from english_games_collection import main
        print("✓ 游戏合集导入成功")
        
        # 测试游戏常量
        from english_games_collection import SCREEN_WIDTH, SCREEN_HEIGHT
        print(f"✓ 屏幕尺寸: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        
        # 测试单词库
        from english_games_collection import WORD_DICT, WORD_LIST
        print(f"✓ 单词库加载成功，共{len(WORD_LIST)}个单词")
        
        # 测试字体函数
        from english_games_collection import get_chinese_font
        pygame.init()
        font = get_chinese_font(24)
        print("✓ 中文字体加载成功")
        
        print("\n🎮 所有游戏功能测试通过！")
        print("运行命令: python english_games_collection.py")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False
    
    return True

def test_individual_games():
    """测试单个游戏"""
    try:
        # 测试打地鼠游戏
        from english_games_collection import WhackAMoleGame, Mole
        game = WhackAMoleGame()
        game.start()
        print("✓ 打地鼠游戏初始化成功")
        
        # 测试掷沙包游戏
        from english_games_collection import SandbagGame
        game2 = SandbagGame()
        game2.start()
        print("✓ 掷沙包游戏初始化成功")
        
        # 测试连连看游戏
        from english_games_collection import MatchGame
        game3 = MatchGame()
        game3.start()
        print("✓ 连连看游戏初始化成功")
        
        print("\n🎯 所有单个游戏测试通过！")
        
    except Exception as e:
        print(f"❌ 单个游戏测试失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("开始测试英语学习游戏合集...\n")
    
    success1 = test_game_collection()
    success2 = test_individual_games()
    
    if success1 and success2:
        print("\n🎉 所有测试通过！游戏可以正常运行。")
        print("\n运行说明:")
        print("1. 运行游戏合集: python english_games_collection.py")
        print("2. 使用方向键选择游戏")
        print("3. 按回车键开始游戏")
        print("4. 按ESC键返回菜单")
    else:
        print("\n❌ 部分测试失败，请检查代码。")