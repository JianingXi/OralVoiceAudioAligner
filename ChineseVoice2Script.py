import whisper
import re
import os
import shutil
from datetime import timedelta
from opencc import OpenCC
import tempfile

# 初始化繁转简
cc = OpenCC('t2s')

def format_time(seconds: float) -> str:
    """秒转 HH:MM:SS"""
    td = timedelta(seconds=int(seconds))
    return str(td).zfill(8)

def split_sentences(text: str) -> list[str]:
    """中文按句号、问号、叹号切分"""
    parts = re.split(r'(?<=[。？！])\s*', text)
    return [p.strip() for p in parts if p.strip()]

def transcribe_and_save(original_path: str, model) -> None:
    print(f"[INFO] 转录中：{original_path} …")

    try:
        # 创建短路径副本（带原始扩展名）
        ext = os.path.splitext(original_path)[1]
        temp_dir = tempfile.mkdtemp()
        temp_audio_path = os.path.join(temp_dir, "audio" + ext)
        shutil.copy2(original_path, temp_audio_path)

        # 转录
        result = model.transcribe(temp_audio_path, language="zh", fp16=False)

        segments = result.get("segments", [])
        if not segments:
            print(f"[WARN] 无法解析任何文本：{original_path}")
            return

        out_txt = os.path.splitext(original_path)[0] + ".txt"
        with open(out_txt, "w", encoding="utf-8") as f:
            for seg in segments:
                start = seg["start"]
                raw_text = seg["text"].strip()
                for sentence in split_sentences(raw_text):
                    sentence_simplified = cc.convert(sentence)
                    timestamp = format_time(start)
                    line = f"[{timestamp}] {sentence_simplified}"
                    print(line)
                    f.write(line + "\n")

        print(f"[OK] 已保存转写结果到：{out_txt}")

    except Exception as e:
        print(f"[ERROR] 转录失败：{original_path}，原因：{repr(e)}")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def batch_transcribe(folder_path: str, model_size: str = "small") -> None:
    print(f"[INFO] 加载模型 {model_size} ……")
    model = whisper.load_model(model_size)

    audio_extensions = {".mp3", ".m4a", ".wav", ".flac", ".aac"}
    total_files, transcribed = 0, 0

    for root, _, files in os.walk(folder_path):
        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext in audio_extensions:
                filepath = os.path.join(root, filename)
                total_files += 1
                transcribe_and_save(filepath, model)
                transcribed += 1

    print(f"\n[SUMMARY] 共检测到音频文件 {total_files} 个，成功转写 {transcribed} 个。")

if __name__ == "__main__":
    folder = r"G:\作品\科普组\微视频\44科普组_视频类_陈熙炀"
    batch_transcribe(folder, model_size="base")
