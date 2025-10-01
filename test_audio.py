#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试发音功能
"""

from word_audio import AudioSystem

def test_audio():
    """测试音频系统"""
    print("测试音频系统...")
    
    audio = AudioSystem()
    
    # 测试几个单词的发音
    test_words = ["apple", "book", "cat", "dog"]
    
    for word in test_words:
        print(f"尝试发音: {word}")
        success = audio.speak(word)
        if success:
            print(f"✓ {word} 发音成功")
        else:
            print(f"✗ {word} 发音失败")
        
        # 等待发音完成
        import time
        time.sleep(1)

if __name__ == "__main__":
    test_audio()