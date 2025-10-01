#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英语单词清单文件
包含所有游戏使用的单词字典和单词列表
"""

# 完整的单词字典（英文到中文）
WORD_DICT = {
    # 一年级上册
    "book": "书", "ruler": "尺子", "pencil": "铅笔", "schoolbag": "书包", "teacher": "教师", 
    "I": "我", "have": "有", "a/an": "一（个）", "face": "脸", "ear": "耳朵", "eye": "眼睛", 
    "nose": "鼻子", "mouth": "嘴巴", "this": "这（个）", "my": "我的", "is": "是", "dog": "狗", 
    "bird": "鸟", "cat": "猫", "tiger": "老虎", "monkey": "猴子", "it": "它", "what": "什么", 
    "one": "一", "two": "二", "three": "三", "four": "四", "five": "五", "six": "六", 
    "seven": "七", "eight": "八", "nine": "九", "ten": "十", "how": "多少", "many": "多的，许多的", 
    "there": "代替主语", "are": "是", "black": "黑色；黑色的", "red": "红色；红色的", 
    "yellow": "黄色；黄色的", "green": "绿色；绿色的", "blue": "蓝色；蓝色的", "colour": "颜色", 
    "apple": "苹果", "pear": "梨", "banana": "香蕉", "orange": "柑橘；橙", "you": "你；你们", 
    "like": "喜欢", "yes": "是，是的", "no": "不，不是", "do": "助动词",
    
    # 一年级下册
    "chair": "椅子", "desk": "书桌", "blackboard": "黑板", "under": "在……下面；在……下方", 
    "in": "在……里面", "where": "在哪里", "on": "在……上", "light": "灯", "box": "箱子；盒子", 
    "bed": "床", "door": "门；出入口", "near": "靠近，接近", "behind": "在……背后", 
    "plane": "飞机", "ball": "球", "doll": "玩偶，玩具娃娃", "train": "列车，火车", 
    "car": "小汽车", "bear": "玩具熊；熊", "can": "可以；能", "sure": "当然", "sorry": "对不起，抱歉", 
    "rice": "米饭；米", "noodles": "面条", "vegetable": "蔬菜", "fish": "鱼肉；鱼", 
    "chicken": "鸡肉；鸡", "egg": "鸡蛋", "hungry": "饥饿的", "want": "要；想要", "and": "和", 
    "juice": "果汁；蔬菜汁", "water": "水", "tea": "茶；茶叶", "milk": "牛奶", "thirsty": "口渴的", 
    "thanks": "感谢", "shirt": "衬衫", "socks": "短袜", "T-shirt": "T恤衫；短袖圆领汗衫", 
    "shorts": "短裤", "skirt": "裙子", "dress": "连衣裙；套裙", "your": "你的；你们的",
    
    # 二年级上册
    "father": "父亲；爸爸", "mother": "母亲；妈妈", "brother": "兄；弟", "sister": "姐；妹", 
    "grandmother": "（外）祖母", "grandfather": "（外）祖父", "who": "谁", "he": "他", "she": "她", 
    "classmate": "同班同学", "friend": "朋友", "woman": "女人", "girl": "女孩", "man": "男人", 
    "boy": "男孩", "look": "看；瞧", "his": "他的", "her": "她的", "name": "名字", "or": "还是", 
    "big": "大的", "tall": "高的", "short": "矮的", "thin": "瘦的", "handsome": "漂亮的，英俊的", 
    "pretty": "漂亮的，可爱的", "new": "新的", "does": "助动词", "bookshop": "书店", "park": "公园", 
    "zoo": "动物园", "hospital": "医院", "school": "学校", "supermarket": "超市", "go": "去", 
    "to": "向，朝", "grass": "草", "tree": "树", "flower": "花；花朵", "boat": "小船", "lake": "湖", 
    "hill": "小山", "Christmas": "圣诞节", "Father Christmas": "圣诞老人", "Christmas tree": "圣诞树", 
    "card": "贺卡；明信片", "present": "礼物", "happy": "快乐的；幸福的", "New Year": "新年", 
    "thank": "谢谢", "merry": "高兴地；愉快的", "here": "这儿", "too": "也；又", "miss": "错过"
}

# 单词列表（仅英文单词）
WORD_LIST = list(WORD_DICT.keys())

# 按年级分组的单词列表
GRADE_1_UPPER = ["book", "ruler", "pencil", "schoolbag", "teacher", "I", "have", "a/an", "face", "ear", "eye", "nose", "mouth", "this", "my", "is", "dog", "bird", "cat", "tiger", "monkey", "it", "what", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "how", "many", "there", "are", "black", "red", "yellow", "green", "blue", "colour", "apple", "pear", "banana", "orange", "you", "like", "yes", "no", "do"]

GRADE_1_LOWER = ["chair", "desk", "blackboard", "under", "in", "where", "on", "light", "box", "bed", "door", "near", "behind", "plane", "ball", "doll", "train", "car", "bear", "can", "sure", "sorry", "rice", "noodles", "vegetable", "fish", "chicken", "egg", "hungry", "want", "and", "juice", "water", "tea", "milk", "thirsty", "thanks", "shirt", "socks", "T-shirt", "shorts", "skirt", "dress", "your"]

GRADE_2_UPPER = ["father", "mother", "brother", "sister", "grandmother", "grandfather", "who", "he", "she", "classmate", "friend", "woman", "girl", "man", "boy", "look", "his", "her", "name", "or", "big", "tall", "short", "thin", "handsome", "pretty", "new", "does", "bookshop", "park", "zoo", "hospital", "school", "supermarket", "go", "to", "grass", "tree", "flower", "boat", "lake", "hill", "Christmas", "Father Christmas", "Christmas tree", "card", "present", "happy", "New Year", "thank", "merry", "here", "too", "miss"]

def get_word_dict():
    """获取单词字典"""
    return WORD_DICT

def get_word_list():
    """获取单词列表"""
    return WORD_LIST

def get_words_by_grade(grade):
    """按年级获取单词列表"""
    if grade == "grade1_upper":
        return GRADE_1_UPPER
    elif grade == "grade1_lower":
        return GRADE_1_LOWER
    elif grade == "grade2_upper":
        return GRADE_2_UPPER
    else:
        return WORD_LIST

if __name__ == "__main__":
    print(f"单词总数: {len(WORD_DICT)}")
    print(f"单词列表: {WORD_LIST[:10]}...")