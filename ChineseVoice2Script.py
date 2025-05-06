import whisper
import re
import os
from datetime import timedelta
from opencc import OpenCC

# 初始化繁简转换器：t2s 表示「繁体到简体」
cc = OpenCC('t2s')

def format_time(seconds: float) -> str:
    """将秒数转换为 HH:MM:SS 格式"""
    td = timedelta(seconds=int(seconds))
    total = int(td.total_seconds())
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def split_sentences(text: str) -> list[str]:
    """按中文句号、问号、叹号拆句，并保留标点"""
    parts = re.split(r'(?<=[。？！])\s*', text)
    return [p.strip() for p in parts if p.strip()]

def transcribe_and_save(audio_path: str, model) -> None:
    """
    对单个音频文件进行转写并保存为简体中文文本。
    """
    print(f"[INFO] 转录中：{audio_path} …")
    result = model.transcribe(audio_path, language="zh", fp16=False)

    dirpath = os.path.dirname(audio_path)
    basename = os.path.splitext(os.path.basename(audio_path))[0]
    out_txt = os.path.join(dirpath, basename + ".txt")

    with open(out_txt, "w", encoding="utf-8") as f:
        for seg in result["segments"]:
            start = seg["start"]
            text = seg["text"].strip()
            for sentence in split_sentences(text):
                simple = cc.convert(sentence)
                ts = format_time(start)
                line = f"[{ts}] {simple}"
                print(line)
                f.write(line + "\n")

    print(f"[INFO] 已保存转写结果到：{out_txt}")

def batch_transcribe(folder_path: str, model_size: str = "small") -> None:
    """
    遍历目录中的所有音频文件并执行转写。
    """
    print(f"[INFO] 加载模型 {model_size} ……")
    model = whisper.load_model(model_size)

    audio_extensions = {".mp3", ".m4a", ".wav", ".flac", ".aac"}
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath) and os.path.splitext(filename)[1].lower() in audio_extensions:
            try:
                transcribe_and_save(filepath, model)
            except Exception as e:
                print(f"[ERROR] 转录失败：{filename}，原因：{e}")

if __name__ == "__main__":
    folder = r"G:\D20250506_研究生院科普大赛作品副本"
    batch_transcribe(folder, model_size="large-v1")  # 可选 small, medium, large-v1 等
