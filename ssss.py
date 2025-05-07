import os

folder = r"G:\科创组"

print("🔍 开始诊断所有音频文件路径：\n")

audio_extensions = {".mp3", ".m4a", ".wav", ".flac", ".aac"}

for root, _, files in os.walk(folder):
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext in audio_extensions:
            path = os.path.join(root, file)
            exists = os.path.exists(path)
            print(f"{'[✅存在]' if exists else '[❌不存在]'} 长度={len(path):>3} | {repr(path)}")
