import os
import subprocess

# ———— 配置 ————
# 直接把你的目标文件夹写在这里
TARGET_DIR = r"G:\D20250506_研究生院科普大赛作品副本"

def convert_to_mp3(input_path: str, output_path: str) -> None:
    """
    调用 ffmpeg 将音视频文件转换为 MP3。
    - 使用 libmp3lame 编码，192k 比特率
    - 去除视频流（-vn）
    """
    cmd = [
        "ffmpeg",
        "-y",               # 覆盖已存在文件
        "-i", input_path,   # 输入
        "-vn",              # 不处理视频流
        "-acodec", "libmp3lame",
        "-ab", "192k",      # 192kbps
        output_path
    ]
    subprocess.run(cmd, check=True)

def batch_convert(directory: str) -> None:
    """
    遍历目录，把所有 .mp4/.wav 文件转成 .mp3。
    """
    if not os.path.isdir(directory):
        print(f"错误：{directory} 不是有效目录")
        return

    for fname in os.listdir(directory):
        base, ext = os.path.splitext(fname)
        ext = ext.lower()
        if ext in (".mp4", ".wav"):
            src = os.path.join(directory, fname)
            dst = os.path.join(directory, base + ".mp3")
            try:
                print(f"[转换] {src} → {dst}")
                convert_to_mp3(src, dst)
            except subprocess.CalledProcessError as e:
                print(f"[失败] {src}：{e}")

if __name__ == "__main__":
    print(f"开始批量转换：{TARGET_DIR}")
    batch_convert(TARGET_DIR)
    print("全部完成！")
