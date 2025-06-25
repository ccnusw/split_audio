import sys
import os

print("--- 1. Python 可执行文件路径 ---")
print(sys.executable)
print("\n" + "="*50 + "\n")

print("--- 2. Python 模块搜索路径 (sys.path) ---")
# sys.path 是Python寻找模块时会检查的文件夹列表
for i, path in enumerate(sys.path):
    print(f"{i}: {path}")
print("\n" + "="*50 + "\n")

print("--- 3. 检查 PYTHONPATH 环境变量 ---")
pythonpath_env = os.environ.get('PYTHONPATH')
if pythonpath_env:
    print(f"检测到 PYTHONPATH 环境变量: {pythonpath_env}")
else:
    print("未检测到 PYTHONPATH 环境变量，这是好的。")
print("\n" + "="*50 + "\n")

print("--- 4. 尝试导入 moviepy 并查看其位置 ---")
try:
    import moviepy
    print("成功导入 'moviepy' 库。")
    print(f"moviepy 库的安装位置: {moviepy.__file__}")

    # 进一步尝试导入 editor
    import moviepy.editor
    print("\n成功导入 'moviepy.editor' 模块。看起来一切正常！")

except ImportError as e:
    print(f"\n导入时发生错误: {e}")
except Exception as e:
    print(f"\n发生未知错误: {e}")