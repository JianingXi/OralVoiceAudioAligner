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

def transcribe_and_save(audio_path: str, model_size: str = "small"):
    """
    离线转录音频，输出简体中文，并保存到同目录 txt 文件。
    """
    print(f"[INFO] 加载模型 {model_size} ……")
    model = whisper.load_model(model_size)

    print(f"[INFO] 转录中：{audio_path} …")
    result = model.transcribe(audio_path, language="zh", fp16=False)

    # 准备输出路径：同目录、同文件名但 .txt
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
                print(line)        # 控制台打印
                f.write(line + "\n")  # 写入文件
    print(f"[INFO] 已保存转写结果到：{out_txt}")

if __name__ == "__main__":
    # 把这里改成你的音频文件全路径
    audio_file = r"C:\Users\xijia\Desktop\pandoc\广州医科大学(番禺校区)一期.m4a"
    transcribe_and_save(audio_file, model_size="large-v1")  # small, large-v1
