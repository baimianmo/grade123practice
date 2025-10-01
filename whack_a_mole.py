import pygame
import random
import time
import os
import sys
from pygame import mixer
from word_audio import AudioSystem

# 全局变量
screen = None

# 强制初始化pygame系统
pygame.init()
try:
    mixer.init()
    print("音效系统初始化成功")
except:
    print("音效系统初始化失败，游戏将继续但没有音效")

# 初始化音频系统
try:
    mixer.init()
    print("音效系统初始化成功")
except:
    print("音效系统初始化失败，游戏将继续但没有音效")

# 初始化单词发音系统
audio_system = AudioSystem()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GRID_SIZE = 3
CELL_SIZE = 180
MOLE_SIZE = 120
GOLD_PROBABILITY = 0.1
GAME_DURATION = 60  # 60秒游戏时长

# 中英文单词对照字典（完整版，包含所有年级单词）
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
    "like": "喜欢", "yes": "是", "no": "不", "do": "助动词",
    
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

# 英文单词清单
WORD_LIST = list(WORD_DICT.keys())

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
LIGHT_BROWN = (160, 82, 45)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
LIGHT_GREEN = (144, 238, 144)
DARK_GREEN = (0, 100, 0)

class Mole:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_gold = random.random() < GOLD_PROBABILITY
        self.word = random.choice(WORD_LIST)
        self.chinese = WORD_DICT.get(self.word, self.word)
        self.show_time = random.uniform(1.0, 2.0)
        self.appear_time = time.time()
        self.hit_time = 0
        self.is_hit = False
        self.scale = 1.0
        self.show_chinese = False
        self.color_flipped = False
        
        # 地鼠出现时播放单词发音
        try:
            audio_system.speak(self.word)
        except Exception as e:
            print(f"发音失败: {e}")
    
    def draw(self):
        global screen
        if not screen:
            return
            
        # 绘制圆形地鼠
        mole_color = GOLD if self.is_gold else (160, 82, 45)
        mole_radius = int(CELL_SIZE * 0.4 * self.scale)
        pygame.draw.circle(screen, mole_color, (self.x, self.y), mole_radius)
        
        # 绘制单词和中文释义
        try:
            font_en = get_chinese_font(24)
            font_cn = get_chinese_font(20)
            
            # 渲染英文单词
            word_surface = font_en.render(self.word, True, WHITE)
            word_rect = word_surface.get_rect(center=(self.x, self.y - 10))
            screen.blit(word_surface, word_rect)
            
            # 如果被击中，显示中文释义
            if self.is_hit:
                try:
                    cn_surface = font_cn.render(self.chinese, True, WHITE)
                    cn_rect = cn_surface.get_rect(center=(self.x, self.y + 15))
                    screen.blit(cn_surface, cn_rect)
                except:
                    # 如果中文显示失败，只显示英文
                    pass
                
        except Exception as e:
            print(f"绘制文字失败: {str(e)}")
    
    def update(self):
        current_time = time.time()
        
        if self.is_hit:
            if current_time - self.hit_time > 1.0:  # 被击中后显示1秒
                return False
            return True
            
        if current_time - self.appear_time > self.show_time:
            return False
            
        return True
    
    def is_clicked(self, pos):
        # 扩大点击区域，确保移动端适配（≥40px）
        click_radius = max(CELL_SIZE // 2, 40)
        distance = ((pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2) ** 0.5
        return distance <= click_radius
    
    def speak(self):
        if not mixer.get_init():
            return
            
        # 确保sounds目录存在
        if not os.path.exists("sounds"):
            print("sounds目录不存在，无法播放单词发音")
            return
            
        # 构建音频文件路径
        sound_file = os.path.join("sounds", f"{self.word.lower()}.wav")
        if not os.path.exists(sound_file):
            print(f"音频文件不存在: {sound_file}")
            return
            
        try:
            # 加载并播放音频
            sound = mixer.Sound(sound_file)
            sound.play()
        except Exception as e:
            print(f"播放音频失败: {str(e)}")
            # 尝试重新初始化音频系统
            try:
                mixer.quit()
                mixer.init()
                sound = mixer.Sound(sound_file)
                sound.play()
            except:
                pass

class Game:
    def __init__(self):
        self.score = 0
        self.time_left = GAME_DURATION
        self.moles = []
        self.game_start_time = 0
        self.is_game_running = False
        self.max_moles = 2
        self.spawn_rate = 1.5
        self.last_spawn_time = 0
        self.grid = self.create_grid()
        
        # 初始化音效
        self.hit_sound = None
        self.gold_sound = None
        self.miss_sound = None
        try:
            if mixer.get_init():
                self.hit_sound = mixer.Sound("hit.wav") if os.path.exists("hit.wav") else None
                self.gold_sound = mixer.Sound("gold.wav") if os.path.exists("gold.wav") else None
                self.miss_sound = mixer.Sound("miss.wav") if os.path.exists("miss.wav") else None
        except:
            pass

    def start(self):
        self.score = 0
        self.time_left = GAME_DURATION
        self.moles = []
        self.game_start_time = time.time()
        self.is_game_running = True
        self.max_moles = 2
        self.spawn_rate = 1.5
        self.last_spawn_time = 0

    def create_grid(self):
        grid = []
        margin_x = (SCREEN_WIDTH - GRID_SIZE * CELL_SIZE) // 2
        margin_y = 200
        
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = margin_x + col * CELL_SIZE + CELL_SIZE // 2
                y = margin_y + row * CELL_SIZE + CELL_SIZE // 2
                grid.append((x, y))
        return grid

    def update(self):
        if not self.is_game_running:
            return
            
        # 更新游戏时间
        elapsed = time.time() - self.game_start_time
        self.time_left = max(0, GAME_DURATION - elapsed)
        
        # 随时间增加难度
        if self.time_left < 40 and self.max_moles < 3:
            self.max_moles = 3
        if self.time_left < 20 and self.max_moles < 4:
            self.max_moles = 4
        if self.time_left < 10:
            self.spawn_rate = 0.8
            
        # 生成新地鼠
        self.spawn_mole()
        
        # 更新地鼠状态
        active_moles = []
        for mole in self.moles:
            if mole.update():  # 如果返回True表示地鼠仍然活跃
                active_moles.append(mole)
        self.moles = active_moles
        
        # 检查游戏是否结束
        if self.time_left <= 0:
            self.is_game_running = False

    def spawn_mole(self):
        if not self.is_game_running:
            return
            
        # 确保游戏已经开始
        if time.time() - self.game_start_time < 0.5:
            return
            
        # 检查当前地鼠数量
        if len(self.moles) >= self.max_moles:
            return
            
        current_time = time.time()
        if current_time - self.last_spawn_time < self.spawn_rate:
            return
            
        # 找出所有空的地鼠洞
        available_holes = []
        for pos in self.grid:
            hole_empty = True
            for mole in self.moles:
                if mole.x == pos[0] and mole.y == pos[1]:
                    hole_empty = False
                    break
            if hole_empty:
                available_holes.append(pos)
                
        if not available_holes:
            return
            
        try:
            # 随机选择一个空的地鼠洞
            hole_pos = random.choice(available_holes)
            new_mole = Mole(hole_pos[0], hole_pos[1])
            self.moles.append(new_mole)
            self.last_spawn_time = current_time
        except Exception as e:
            print(f"生成地鼠时出错: {str(e)}")

    def draw(self):
        global screen
        if not screen:
            return
            
        # 绘制渐变背景
        for y in range(SCREEN_HEIGHT):
            gray_value = int(200 + (55 * y / SCREEN_HEIGHT))
            pygame.draw.line(screen, (gray_value, gray_value, gray_value), (0, y), (SCREEN_WIDTH, y))
        
        # 绘制游戏标题和信息区域背景
        pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, 150))
        
        # 绘制标题和分数
        try:
            font = get_chinese_font(36)
            title = font.render("Whack-A-Mole English", True, BLACK)
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))
            
            score_text = font.render(f"Score: {self.score}", True, BLACK)
            time_text = font.render(f"Time: {int(self.time_left)}s", True, BLACK)
            screen.blit(score_text, (50, 100))
            screen.blit(time_text, (SCREEN_WIDTH - 200, 100))
        except Exception as e:
            print(f"绘制界面失败: {str(e)}")
        
        # 绘制地鼠洞网格
        margin_x = (SCREEN_WIDTH - GRID_SIZE * CELL_SIZE) // 2
        margin_y = 200
        
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = margin_x + col * CELL_SIZE + CELL_SIZE // 2
                y = margin_y + row * CELL_SIZE + CELL_SIZE // 2
                
                # 绘制地鼠洞
                pygame.draw.circle(screen, BROWN, (x, y), CELL_SIZE // 2)
                pygame.draw.circle(screen, LIGHT_BROWN, (x, y), CELL_SIZE // 2 - 10)
        
        # 绘制地鼠
        for mole in self.moles:
            mole.draw()
        
        # 游戏结束画面
        if not self.is_game_running and self.time_left <= 0:
            self.draw_game_over()
            
        # 绘制游戏说明
        try:
            font = get_chinese_font(20)
            instruction = font.render("Click moles to score, click empty areas to lose points", True, BLACK)
            screen.blit(instruction, (SCREEN_WIDTH//2 - instruction.get_width()//2, SCREEN_HEIGHT - 30))
        except:
            pass

    def draw_game_over(self):
        global screen
        if not screen:
            return
            
        try:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            
            font = get_chinese_font(36)
            game_over = font.render("Game Over!", True, WHITE)
            final_score = font.render(f"Final Score: {self.score}", True, WHITE)
            restart = font.render("Press R to restart", True, WHITE)
            
            if screen:
                screen.blit(game_over, (SCREEN_WIDTH // 2 - game_over.get_width() // 2, 250))
                screen.blit(final_score, (SCREEN_WIDTH // 2 - final_score.get_width() // 2, 320))
                screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 380))
        except Exception as e:
            print(f"绘制结束画面失败: {str(e)}")

    def handle_click(self, pos):
        if not self.is_game_running:
            return
        
        hit_mole = False
        
        for mole in self.moles:
            if mole.is_clicked(pos):
                mole.is_hit = True
                mole.hit_time = time.time()
                mole.color_flipped = not mole.color_flipped
                hit_mole = True
                
                # 立即播放音效和发音
                mole.speak()
                if mole.is_gold:
                    if self.gold_sound:
                        try:
                            self.gold_sound.play()
                        except:
                            pass
                    self.score += 30
                else:
                    if self.hit_sound:
                        try:
                            self.hit_sound.play()
                        except:
                            pass
                    self.score += 10
                break
        
        if not hit_mole:
            self.score = max(0, self.score - 5)
            if self.miss_sound:
                try:
                    self.miss_sound.play()
                except:
                    pass

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

def main():
    global screen
    # 初始化显示
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Whack-A-Mole English Game")
    clock = pygame.time.Clock()
    
    # 创建游戏实例
    game = Game()
    running = True
    
    # 显示开始界面
    screen.fill(WHITE)
    try:
        font = get_chinese_font(36)
        title = font.render("Whack-A-Mole English Game", True, BLACK)
        start_info = font.render("Press SPACE to start", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//2 - 50))
        screen.blit(start_info, (SCREEN_WIDTH//2 - start_info.get_width()//2, SCREEN_HEIGHT//2 + 20))
    except Exception as e:
        print(f"绘制开始界面失败: {str(e)}")
    
    pygame.display.flip()
    
    # 等待开始
    waiting = True
    while waiting and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.start()
                    waiting = False
    
    # 主游戏循环
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    game.handle_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and not game.is_game_running:
                    # 完全重置游戏
                    game = Game()
                    game.start()
        
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(60)
        
        # 强制处理事件队列
        pygame.event.pump()

    pygame.quit()

if __name__ == "__main__":
    main()