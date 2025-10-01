import PyInstaller.__main__
import os
import sys

def build():
    # 确保资源目录存在
    os.makedirs('sounds', exist_ok=True)
    
    # 获取资源文件路径
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # PyInstaller配置
    params = [
        'whack_a_mole.py',
        '--onefile',
        '--windowed',
        '--name=WhackAMole',
        '--add-data=sounds/*;sounds',  # 嵌入所有音频文件
        '--hidden-import=pyttsx3.drivers',
        '--hidden-import=pyttsx3.drivers.sapi5',
        '--hidden-import=pkg_resources.py2_warn',
        '--hidden-import=pygame._sdl2.audio',
        '--clean',
        '--noconfirm',
        '--log-level=WARN'
    ]
    
    # 可选：添加存在的字体文件
    ttf_files = [f for f in os.listdir() if f.endswith('.ttf')]
    for ttf in ttf_files:
        params.append(f'--add-data={ttf};.')
    
    # 添加图标文件（如果存在）
    if os.path.exists('app.ico'):
        params.append('--icon=app.ico')
    
    try:
        print("开始打包...")
        PyInstaller.__main__.run(params)
        
        # 检查输出文件
        exe_path = os.path.join('dist', 'WhackAMole.exe')
        if os.path.exists(exe_path):
            print(f"打包成功！生成文件: {exe_path}")
            print("请确保sounds目录与exe文件在同一目录下")
        else:
            print("打包失败：未生成exe文件")
    except Exception as e:
        print(f"打包过程中出错: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    build()