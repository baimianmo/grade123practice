import os
import pyttsx3
from english_games_collection import WORD_DICT

# 确保sounds目录存在
if not os.path.exists('sounds'):
    os.makedirs('sounds')

def generate_audio_files():
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'chinese' in voice.name.lower() or 'zh' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        
        for word in list(WORD_DICT.keys()):
            # 处理特殊单词 "a/an" -> 使用 "a" 的发音
            audio_word = word
            if word == "a/an":
                audio_word = "a"
            
            # 处理文件名中的特殊字符，将斜杠替换为下划线
            filename_word = word.replace("/", "_")
            filename = f"sounds/{filename_word}.wav"
            if not os.path.exists(filename):
                engine.save_to_file(audio_word, filename)
                print(f"生成: {filename} (使用发音: {audio_word})")
        
        engine.runAndWait()
        print("所有音频文件生成完成！")
    except Exception as e:
        print(f"生成音频文件时出错: {str(e)}")

if __name__ == "__main__":
    generate_audio_files()