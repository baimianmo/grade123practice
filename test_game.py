#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
游戏功能测试脚本
用于验证打地鼠游戏的基本功能
"""

import pygame
import sys
import os

def test_pygame_initialization():
    """测试Pygame初始化"""
    try:
        pygame.init()
        print("✓ Pygame初始化成功")
        
        # 测试显示模式
        screen = pygame.display.set_mode((100, 100))
        pygame.display.quit()
        print("✓ 显示模式测试通过")
        
        # 测试音频系统
        try:
            pygame.mixer.init()
            pygame.mixer.quit()
            print("✓ 音频系统测试通过")
        except:
            print("⚠ 音频系统初始化失败（可能不影响游戏运行）")
            
        return True
    except Exception as e:
        print(f"✗ Pygame初始化失败: {e}")
        return False

def test_file_structure():
    """测试文件结构完整性"""
    required_files = [
        'whack_a_mole.py',
        'generate_audio.py',
        'build_exe.py'
    ]
    
    required_dirs = [
        'sounds'
    ]
    
    print("\n检查文件结构:")
    
    # 检查必需文件
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} 存在")
        else:
            print(f"✗ {file} 缺失")
            
    # 检查目录
    for directory in required_dirs:
        if os.path.exists(directory) and os.path.isdir(directory):
            print(f"✓ {directory}/ 目录存在")
            # 检查音频文件数量
            if directory == 'sounds':
                sound_files = [f for f in os.listdir(directory) if f.endswith('.wav')]
                print(f"  发现 {len(sound_files)} 个音频文件")
        else:
            print(f"✗ {directory}/ 目录缺失")
            
    return True

def test_word_dictionary():
    """测试单词字典完整性"""
    try:
        # 导入游戏模块中的单词字典
        from whack_a_mole import WORD_DICT, WORD_LIST
        
        print(f"\n单词字典测试:")
        print(f"✓ 单词字典包含 {len(WORD_DICT)} 个单词")
        print(f"✓ 单词列表包含 {len(WORD_LIST)} 个单词")
        
        # 检查一些关键单词是否存在
        test_words = ['book', 'apple', 'teacher', 'father', 'Christmas']
        for word in test_words:
            if word in WORD_DICT:
                print(f"✓ '{word}' 在字典中 -> {WORD_DICT[word]}")
            else:
                print(f"✗ '{word}' 不在字典中")
                
        return True
    except Exception as e:
        print(f"✗ 单词字典测试失败: {e}")
        return False

def test_game_logic():
    """测试游戏逻辑"""
    try:
        from whack_a_mole import Mole, Game
        
        print(f"\n游戏逻辑测试:")
        
        # 测试地鼠类
        test_mole = Mole(100, 100)
        print(f"✓ 地鼠类创建成功")
        print(f"  单词: {test_mole.word}")
        print(f"  中文: {test_mole.chinese}")
        print(f"  金色: {test_mole.is_gold}")
        
        # 测试点击检测
        click_result = test_mole.is_clicked((100, 100))
        print(f"✓ 点击检测: {click_result}")
        
        # 测试游戏类
        test_game = Game()
        print(f"✓ 游戏类创建成功")
        print(f"  初始分数: {test_game.score}")
        print(f"  初始时间: {test_game.time_left}")
        
        return True
    except Exception as e:
        print(f"✗ 游戏逻辑测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("单词打地鼠游戏 - 功能测试")
    print("=" * 50)
    
    tests = [
        test_pygame_initialization,
        test_file_structure,
        test_word_dictionary,
        test_game_logic
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"测试异常: {e}")
    
    print(f"\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！游戏应该可以正常运行。")
        print("\n运行游戏命令:")
        print("python whack_a_mole.py")
    else:
        print("⚠ 部分测试失败，请检查相关问题。")
        
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)