#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英语学习游戏合集
包含6个英语学习游戏：
1. 打地鼠 - 单词识别和反应速度训练
2. 掷沙包 - 单词发音识别
3. 连连看 - 单词与中文释义匹配
4. 单词拼写 - 听音拼写训练
5. 闪卡 - 单词记忆和复习
6. 拯救地球 - 单词填空游戏
"""

import pygame
import random
import time
import os
import sys
from pygame import mixer



# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# 初始化pygame
pygame.init()
try:
    mixer.init()
    print("音效系统初始化成功")
except:
    print("音效系统初始化失败，游戏将继续但没有音效")

# 创建屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("英语学习游戏合集")

# 中英文单词对照字典
WORD_DICT = {
    # 一年级上册
    "book": "书", "ruler": "尺子", "pencil": "铅笔", "schoolbag": "书包", 
    "teacher": "教师", "I": "我", "have": "有", "a/an": "一(个)",
    "face": "脸", "ear": "耳朵", "eye": "眼睛", "nose": "鼻子", 
    "mouth": "嘴巴", "this": "这(个)", "my": "我的", "is": "是",
    "dog": "狗", "bird": "鸟", "cat": "猫", "tiger": "老虎", 
    "monkey": "猴子", "it": "它", "what": "什么", "one": "一", 
    "two": "二", "three": "三", "four": "四", "five": "五", 
    "six": "六", "seven": "七", "eight": "八", "nine": "九", 
    "ten": "十", "black": "黑色", "red": "红色", "yellow": "黄色", 
    "green": "绿色", "blue": "蓝色", "colour": "颜色", "apple": "苹果", 
    "pear": "梨", "banana": "香蕉", "orange": "橙子", "you": "你/你们", 
    "like": "喜欢", "yes": "是", "no": "不", "do": "助动词","miss": "错过","are": "是","does":"助动词",
    
    # 一年级下册
    "chair": "椅子", "desk": "书桌", "blackboard": "黑板", "under": "在...下面",
    "in": "在...里面", "where": "在哪里", "on": "在...上", "light": "灯",
    "box": "箱子", "bed": "床", "door": "门", "near": "靠近", "behind": "在...背后",
    "plane": "飞机", "ball": "球", "doll": "玩偶", "train": "火车", "car": "汽车",
    "bear": "熊", "can": "可以", "sure": "当然", "sorry": "对不起", "rice": "米饭",
    "noodles": "面条", "vegetable": "蔬菜", "fish": "鱼", "chicken": "鸡",
    "egg": "鸡蛋", "hungry": "饥饿的", "want": "想要", "and": "和", "juice": "果汁",
    "water": "水", "tea": "茶", "milk": "牛奶", "thirsty": "口渴的", "thanks": "谢谢",
    "shirt": "衬衫", "socks": "袜子", "T-shirt": "T恤", "shorts": "短裤",
    "skirt": "裙子", "dress": "连衣裙", "your": "你的",
    
    # 二年级上册
    "father": "父亲", "mother": "母亲", "brother": "兄弟", "sister": "姐妹",
    "grandmother": "祖母", "grandfather": "祖父", "who": "谁", "he": "他",
    "she": "她", "classmate": "同学", "friend": "朋友", "woman": "女人",
    "girl": "女孩", "man": "男人", "boy": "男孩", "look": "看", "his": "他的",
    "her": "她的", "name": "名字", "or": "或者", "big": "大的", "tall": "高的",
    "short": "矮的", "thin": "瘦的", "handsome": "英俊的", "pretty": "漂亮的",
    "new": "新的", "does": "助动词", "bookshop": "书店", "park": "公园",
    "zoo": "动物园", "hospital": "医院", "school": "学校", "supermarket": "超市",
    "go": "去", "to": "向", "grass": "草", "tree": "树", "flower": "花",
    "boat": "船", "lake": "湖", "hill": "小山", "Christmas": "圣诞节",
    "Father Christmas": "圣诞老人", "Christmas tree": "圣诞树", "card": "卡片",
    "present": "礼物", "happy": "快乐的", "New Year": "新年", "thank": "谢谢",
    "merry": "愉快的", "here": "这里", "too": "也"
}

WORD_LIST = list(WORD_DICT.keys())

def get_chinese_font(size=36):
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
            font = pygame.font.SysFont(font_name, size)
            # 测试是否能渲染中文
            test_surface = font.render('测试', True, (0, 0, 0))
            return font
        except:
            continue
    
    # 如果所有字体都失败，使用默认字体
    return pygame.font.Font(None, size)

class GameMenu:
    """游戏菜单类"""
    def __init__(self):
        self.selected_game = 0
        self.games = [
            "单词打地鼠",
            "掷沙包单词识别",
            "单词连连看",
            "单词拼写挑战",
            "单词闪卡记忆",
            "拯救地球单词填空"
        ]
        self.game_descriptions = [
            "点击地鼠学习单词，测试反应速度",
            "听音识别单词，提高听力理解",
            "匹配单词与中文释义，加强记忆",
            "听音拼写单词，训练拼写能力",
            "闪卡记忆单词，快速复习",
            "单词填空游戏，巩固学习成果"
        ]
    
    def draw(self):
        global screen
        screen.fill(WHITE)
        
        font_title = get_chinese_font(48)
        title = font_title.render("英语学习游戏合集", True, BLUE)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        font_game = get_chinese_font(32)
        font_desc = get_chinese_font(20)
        
        for i, (game, desc) in enumerate(zip(self.games, self.game_descriptions)):
            color = BLUE if i == self.selected_game else BLACK
            game_text = font_game.render(game, True, color)
            desc_text = font_desc.render(desc, True, GRAY)
            
            y_pos = 150 + i * 80
            screen.blit(game_text, (SCREEN_WIDTH//2 - game_text.get_width()//2, y_pos))
            screen.blit(desc_text, (SCREEN_WIDTH//2 - desc_text.get_width()//2, y_pos + 40))
        
        # 操作提示
        font_hint = get_chinese_font(18)
        hint1 = font_hint.render("使用↑↓键选择游戏，按回车键开始", True, BLACK)
        hint2 = font_hint.render("按ESC键退出游戏，游戏中按ESC返回菜单", True, BLACK)
        screen.blit(hint1, (SCREEN_WIDTH//2 - hint1.get_width()//2, SCREEN_HEIGHT - 80))
        screen.blit(hint2, (SCREEN_WIDTH//2 - hint2.get_width()//2, SCREEN_HEIGHT - 50))
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_game = (self.selected_game - 1) % len(self.games)
            elif event.key == pygame.K_DOWN:
                self.selected_game = (self.selected_game + 1) % len(self.games)
            elif event.key == pygame.K_RETURN:
                return self.selected_game + 1
            elif event.key == pygame.K_ESCAPE:
                return -1
        return 0

class WhackAMoleGame:
    """打地鼠游戏"""
    def __init__(self):
        self.score = 0
        self.time_left = 60
        self.is_running = True
        self.grid_size = 3
        self.cell_size = 150
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
        x = random.randint(100, SCREEN_WIDTH - 100)
        y = random.randint(200, SCREEN_HEIGHT - 100)
        word = random.choice(WORD_LIST)
        self.moles.append(Mole(x, y, word))
    
    def handle_click(self, pos):
        if not self.is_running:
            return
            
        hit = False
        for mole in self.moles:
            if mole.is_clicked(pos):
                self.score += 10
                mole.is_hit = True
                hit = True
                break
        
        if not hit:
            self.score = max(0, self.score - 5)
    
    def draw(self):
        global screen
        screen.fill(WHITE)
        
        # 绘制游戏信息
        font = get_chinese_font(36)
        title = font.render("单词打地鼠", True, BLACK)
        score_text = font.render(f"分数: {self.score}", True, BLACK)
        time_text = font.render(f"时间: {int(self.time_left)}秒", True, BLACK)
        
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 30))
        screen.blit(score_text, (50, 100))
        screen.blit(time_text, (SCREEN_WIDTH - 200, 100))
        
        # 绘制地鼠
        for mole in self.moles:
            mole.draw()
        
        # 游戏结束画面
        if not self.is_running:
            self.draw_game_over()
    
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        font = get_chinese_font(36)
        game_over = font.render("游戏结束!", True, WHITE)
        final_score = font.render(f"最终分数: {self.score}", True, WHITE)
        restart = font.render("按R键重新开始，按ESC返回菜单", True, WHITE)
        
        screen.blit(game_over, (SCREEN_WIDTH//2 - game_over.get_width()//2, 250))
        screen.blit(final_score, (SCREEN_WIDTH//2 - final_score.get_width()//2, 320))
        screen.blit(restart, (SCREEN_WIDTH//2 - restart.get_width()//2, 380))

class Mole:
    """地鼠类"""
    def __init__(self, x, y, word):
        self.x = x
        self.y = y
        self.word = word
        self.chinese = WORD_DICT[word]
        self.appear_time = time.time()
        self.show_time = random.uniform(1.0, 2.0)
        self.is_hit = False
        self.hit_time = 0
    
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
        distance = ((pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2) ** 0.5
        return distance <= 50
    
    def draw(self):
        global screen
        # 绘制地鼠
        color = (160, 82, 45)  # 棕色
        pygame.draw.circle(screen, color, (self.x, self.y), 40)
        
        # 绘制单词
        font = get_chinese_font(20)
        word_text = font.render(self.word, True, WHITE)
        screen.blit(word_text, (self.x - word_text.get_width()//2, self.y - word_text.get_height()//2))
        
        # 如果被击中，显示中文
        if self.is_hit:
            font_cn = get_chinese_font(16)
            cn_text = font_cn.render(self.chinese, True, WHITE)
            screen.blit(cn_text, (self.x - cn_text.get_width()//2, self.y + 30))

class SandbagGame:
    """掷沙包游戏（简化版）"""
    def __init__(self):
        self.score = 0
        self.current_word = ""
        self.options = []
        self.is_running = True
    
    def start(self):
        self.score = 0
        self.is_running = True
        self.next_word()
    
    def next_word(self):
        self.current_word = random.choice(WORD_LIST)
        # 生成选项（包含正确答案和3个错误答案）
        wrong_options = random.sample([w for w in WORD_LIST if w != self.current_word], 3)
        self.options = wrong_options + [self.current_word]
        random.shuffle(self.options)
    
    def check_answer(self, selected_word):
        if selected_word == self.current_word:
            self.score += 10
            self.next_word()
            return True
        else:
            self.score = max(0, self.score - 5)
            return False
    
    def update(self):
        # 掷沙包游戏不需要实时更新
        pass
    
    def draw(self):
        global screen
        screen.fill(WHITE)
        
        font = get_chinese_font(36)
        title = font.render("掷沙包单词识别", True, BLACK)
        score_text = font.render(f"分数: {self.score}", True, BLACK)
        
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        screen.blit(score_text, (SCREEN_WIDTH - 200, 50))
        
        # 绘制当前单词区域
        font_word = get_chinese_font(48)
        word_text = font_word.render(self.current_word, True, BLUE)
        screen.blit(word_text, (SCREEN_WIDTH//2 - word_text.get_width()//2, 150))
        
        # 绘制选项按钮
        font_opt = get_chinese_font(24)
        for i, option in enumerate(self.options):
            y_pos = 250 + i * 80
            pygame.draw.rect(screen, GRAY, (200, y_pos, 400, 60), border_radius=10)
            opt_text = font_opt.render(option, True, BLACK)
            screen.blit(opt_text, (SCREEN_WIDTH//2 - opt_text.get_width()//2, y_pos + 20))
        
        # 操作提示
        font_hint = get_chinese_font(18)
        hint = font_hint.render("点击单词选择答案，按ESC返回菜单", True, BLACK)
        screen.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, SCREEN_HEIGHT - 50))

class MatchGame:
    """单词连连看游戏"""
    def __init__(self):
        self.score = 0
        self.english_words = []  # 左列英文单词
        self.chinese_meanings = []  # 右列中文释义
        self.selected_en = None  # 选中的英文单词索引
        self.selected_cn = None  # 选中的中文释义索引
        self.matched_pairs = []  # 已匹配的单词对
        self.is_running = True
        self.pair_count = 6  # 每次显示6对单词
    
    def start(self):
        self.score = 0
        self.is_running = True
        self.setup_game()
    
    def setup_game(self):
        # 随机选择单词
        words = random.sample(WORD_LIST, self.pair_count)
        
        # 左列：英文单词
        self.english_words = words.copy()
        random.shuffle(self.english_words)
        
        # 右列：中文释义（随机打乱）
        self.chinese_meanings = [WORD_DICT[word] for word in words]
        random.shuffle(self.chinese_meanings)
        
        self.selected_en = None
        self.selected_cn = None
        self.matched_pairs = []
    
    def select_english(self, index):
        if index in [pair[0] for pair in self.matched_pairs]:
            return  # 已匹配的单词不可选
        
        self.selected_en = index
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
            if WORD_DICT[en_word] == cn_meaning:
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
    
    def draw(self):
        global screen
        screen.fill(WHITE)
        
        font = get_chinese_font(36)
        title = font.render("单词连连看", True, BLACK)
        score_text = font.render(f"分数: {self.score}", True, BLACK)
        
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        screen.blit(score_text, (SCREEN_WIDTH - 200, 50))
        
        # 绘制列标题
        font_title = get_chinese_font(24)
        en_title = font_title.render("英文单词", True, BLUE)
        cn_title = font_title.render("中文释义", True, BLUE)
        
        screen.blit(en_title, (150, 120))
        screen.blit(cn_title, (450, 120))
        
        # 绘制左列：英文单词
        font_word = get_chinese_font(20)
        for i, word in enumerate(self.english_words):
            y_pos = 180 + i * 60
            
            # 判断样式：检查该单词是否已匹配
            is_matched = any(pair[0] == i for pair in self.matched_pairs)
            if is_matched:  # 已匹配的单词
                color = GRAY
                text_color = WHITE
            elif self.selected_en == i:  # 选中的单词
                color = BLUE
                text_color = WHITE
            else:  # 未选中的单词
                color = GREEN
                text_color = WHITE
            
            # 绘制单词框
            pygame.draw.rect(screen, color, (100, y_pos, 200, 40), border_radius=5)
            word_text = font_word.render(word, True, text_color)
            screen.blit(word_text, (200 - word_text.get_width()//2, y_pos + 20 - word_text.get_height()//2))
        
        # 绘制右列：中文释义
        for i, meaning in enumerate(self.chinese_meanings):
            y_pos = 180 + i * 60
            
            # 判断样式：检查该释义是否已匹配
            is_matched = any(pair[1] == i for pair in self.matched_pairs)
            if is_matched:  # 已匹配的释义
                color = GRAY
                text_color = WHITE
            elif self.selected_cn == i:  # 选中的释义
                color = BLUE
                text_color = WHITE
            else:  # 未选中的释义
                color = GREEN
                text_color = WHITE
            
            # 绘制释义框
            pygame.draw.rect(screen, color, (400, y_pos, 200, 40), border_radius=5)
            meaning_text = font_word.render(meaning, True, text_color)
            screen.blit(meaning_text, (500 - meaning_text.get_width()//2, y_pos + 20 - meaning_text.get_height()//2))
        
        # 操作提示
        font_hint = get_chinese_font(18)
        hint = font_hint.render("点击左侧单词和右侧释义进行匹配，按ESC返回菜单", True, BLACK)
        screen.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, SCREEN_HEIGHT - 50))

def main():
    global screen
    clock = pygame.time.Clock()
    
    # 使用列表来确保变量在循环中正确更新
    game_state = [0]  # 0=菜单, 1-6=各个游戏
    menu = GameMenu()
    games = {
        1: WhackAMoleGame(),
        2: SandbagGame(),
        3: MatchGame(),
        # 4: SpellingGame(),   # 单词拼写游戏
        # 5: FlashcardGame(),  # 闪卡游戏
        # 6: EarthGame()       # 拯救地球游戏
    }
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_state[0] == 0:  # 菜单界面
                result = menu.handle_event(event)
                if result == -1:
                    running = False
                elif result > 0:
                    game_state[0] = result
                    # 检查游戏是否存在，如果不存在则显示提示
                    if game_state[0] in games:
                        games[game_state[0]].start()
                    else:
                        print(f"游戏 {game_state[0]} 正在开发中，敬请期待！")
                        game_state[0] = 0  # 返回菜单
            
            else:  # 游戏界面
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state[0] = 0  # 返回菜单
                    elif event.key == pygame.K_r and game_state[0] == 1 and not games[1].is_running:
                        # 打地鼠游戏重新开始
                        games[1].start()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if game_state[0] == 1:  # 打地鼠
                        if games[1].is_running:
                            games[1].handle_click(event.pos)
                        else:
                            # 游戏结束界面点击重新开始
                            if 300 <= event.pos[1] <= 350:
                                games[1].start()
                    elif game_state[0] == 2:  # 掷沙包
                        # 检查点击了哪个选项
                        for i, option in enumerate(games[2].options):
                            y_pos = 250 + i * 80
                            if 200 <= event.pos[0] <= 600 and y_pos <= event.pos[1] <= y_pos + 60:
                                games[2].check_answer(option)
                                break
                    elif game_state[0] == 3:  # 连连看
                        # 检查点击左列英文单词
                        for i in range(len(games[3].english_words)):
                            y_pos = 180 + i * 60
                            if 100 <= event.pos[0] <= 300 and y_pos <= event.pos[1] <= y_pos + 40:
                                games[3].select_english(i)
                                break
                        
                        # 检查点击右列中文释义
                        for i in range(len(games[3].chinese_meanings)):
                            y_pos = 180 + i * 60
                            if 400 <= event.pos[0] <= 600 and y_pos <= event.pos[1] <= y_pos + 40:
                                games[3].select_chinese(i)
                                break
        
        # 更新游戏状态
        if game_state[0] > 0 and game_state[0] in games:
            if hasattr(games[game_state[0]], 'update'):
                games[game_state[0]].update()
        
        # 绘制界面
        if game_state[0] == 0:
            menu.draw()
        elif game_state[0] in games:
            games[game_state[0]].draw()
        else:
            # 显示开发中提示
            screen.fill(WHITE)
            font = get_chinese_font(36)
            text = font.render("游戏正在开发中，敬请期待！", True, BLACK)
            hint = font.render("按ESC键返回菜单", True, BLUE)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - 50))
            screen.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, SCREEN_HEIGHT//2 + 20))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()