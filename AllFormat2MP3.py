import os
import subprocess

# ———— 配置 ————
TARGET_DIR = r"G:\D20250506_研究生院科普大赛作品副本"
DELETE_ORIGINAL = False  # 设置为 True 则删除源文件，False 保留

def convert_to_mp3(input_path: str, output_path: str) -> None:
    """
    使用 ffmpeg 将音视频文件转换为 MP3。
    """
    cmd = [
        "ffmpeg",
        "-y",               # 覆盖输出文件
        "-i", input_path,   # 输入文件路径
        "-vn",              # 去除视频流
        "-acodec", "libmp3lame",
        "-ab", "192k",      # 设置音频比特率
        output_path
    ]
    subprocess.run(cmd, check=True)

def batch_convert(directory: str) -> None:
    """
    递归遍历目录，批量转换音频/视频为 MP3。
    """
    if not os.path.isdir(directory):
        print(f"错误：{directory} 不是有效目录")
        return

    for root, _, files in os.walk(directory):
        for fname in files:
            base, ext = os.path.splitext(fname)
            ext = ext.lower()
            if ext in (".mp4", ".wav"):
                src = os.path.join(root, fname)
                dst = os.path.join(root, base + ".mp3")

                # 跳过已存在的目标文件
                if os.path.exists(dst):
                    print(f"[跳过] 已存在：{dst}")
                    continue

                try:
                    print(f"[转换] {src} → {dst}")
                    convert_to_mp3(src, dst)
                    if DELETE_ORIGINAL:
                        os.remove(src)
                        print(f"[已删除源文件] {src}")
                except subprocess.CalledProcessError as e:
                    print(f"[失败] {src}：{e}")

if __name__ == "__main__":
    print(f"开始批量转换：{TARGET_DIR}")
    batch_convert(TARGET_DIR)
    print("全部完成！")
