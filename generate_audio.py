import os
import pyttsx3

# 确保sounds目录存在
if not os.path.exists('sounds'):
    os.makedirs('sounds')

# 中英文单词对照字典
WORD_DICT = {
    # 一年级上册
    "book": "书", "ruler": "尺子", "pencil": "铅笔", "schoolbag": "书包", "teacher": "教师", 
    "I": "我", "have": "有", "a/an": "一(个)", "face": "脸", "ear": "耳朵", 
    "eye": "眼睛", "nose": "鼻子", "mouth": "嘴巴", "this": "这(个)", "my": "我的", 
    "is": "是", "dog": "狗", "bird": "鸟", "cat": "猫", "tiger": "老虎", 
    "monkey": "猴子", "it": "它", "what": "什么", "one": "一", "two": "二", 
    "three": "三", "four": "四", "five": "五", "six": "六", "seven": "七", 
    "eight": "八", "nine": "九", "ten": "十", "black": "黑色", "red": "红色", 
    "yellow": "黄色", "green": "绿色", "blue": "蓝色", "apple": "苹果", 
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
    "new": "新的", "bookshop": "书店", "park": "公园", "zoo": "动物园",
    "hospital": "医院", "school": "学校", "supermarket": "超市", "go": "去",
    "to": "向", "grass": "草", "tree": "树", "flower": "花", "boat": "船",
    "lake": "湖", "hill": "小山", "Christmas": "圣诞节", "Father Christmas": "圣诞老人",
    "Christmas tree": "圣诞树", "card": "卡片", "present": "礼物", "happy": "快乐的",
    "New Year": "新年", "thank": "谢谢", "merry": "愉快的", "here": "这里", "too": "也"
}

def generate_audio_files():
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'chinese' in voice.name.lower() or 'zh' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        
        for word in WORD_DICT.keys():
            filename = f"sounds/{word}.wav"
            if not os.path.exists(filename):
                engine.save_to_file(word, filename)
                print(f"生成: {filename}")
        
        engine.runAndWait()
        print("所有音频文件生成完成！")
    except Exception as e:
        print(f"生成音频文件时出错: {str(e)}")

if __name__ == "__main__":
    generate_audio_files()