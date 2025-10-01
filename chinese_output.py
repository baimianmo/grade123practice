#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文输出模块
提供中文文本渲染功能
"""

import pygame

def get_chinese_font(size=36, bold=False):
    """获取支持中文的字体"""
    chinese_fonts = [
        'microsoftyahei',      # 微软雅黑
        'simhei',              # 黑体
        'microsoftjhenghei',   # 微软正黑
        'fangsong',            # 仿宋
        'kaiti',               # 楷体
        'arial'                # 回退字体
    ]
    
    for font_name in chinese_fonts:
        try:
            font = pygame.font.SysFont(font_name, size, bold=bold)
            # 测试是否能渲染中文
            test_surface = font.render('测试', True, (0, 0, 0))
            return font
        except:
            continue
    
    # 如果所有字体都失败，使用默认字体
    return pygame.font.Font(None, size)

def render_chinese_text(text, size, color, bold=False):
    """渲染中文文本"""
    font = get_chinese_font(size)
    if bold:
        font.set_bold(True)
    return font.render(text, True, color)