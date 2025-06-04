import os
import subprocess

# 目标文件夹
input_dir = r"C:\MyDocument\ToDoList\D20_ToHardDisk\D20250430_本科职业生涯规划_读研、出国、找工作的具体措施"

for fname in os.listdir(input_dir):
    if fname.lower().endswith(".m4a"):
        src = os.path.join(input_dir, fname)
        dst = os.path.join(input_dir, os.path.splitext(fname)[0] + ".mp3")
        # -qscale:a 2 代表 VBR 质量，可调整（0-9，数值越小质量越高）
        subprocess.run([
            "ffmpeg",
            "-y",           # 覆盖同名文件
            "-i", src,
            "-codec:a", "libmp3lame",
            "-qscale:a", "2",
            dst
        ], check=True)
        print(f"[OK] {fname} → {os.path.basename(dst)}")
