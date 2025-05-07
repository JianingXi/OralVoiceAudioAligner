import os
from moviepy.editor import VideoFileClip

def video_to_audio_recursive(input_dir, output_dir=None):
    # 支持的视频格式
    video_exts = {'.mp4', '.mov', '.avi', '.mkv', '.flv', '.webm'}

    if output_dir is None:
        output_dir = input_dir

    for root, _, files in os.walk(input_dir):
        for filename in files:
            name, ext = os.path.splitext(filename)
            ext = ext.lower()

            if ext in video_exts:
                video_path = os.path.join(root, filename)

                # 构建对应的输出路径（保持子目录结构）
                relative_path = os.path.relpath(root, input_dir)
                target_dir = os.path.join(output_dir, relative_path)
                os.makedirs(target_dir, exist_ok=True)

                audio_path = os.path.join(target_dir, name + ".wav")

                try:
                    print(f"[INFO] 正在处理：{video_path}")
                    clip = VideoFileClip(video_path)
                    clip.audio.write_audiofile(audio_path, codec='pcm_s16le')
                    clip.close()
                    print(f"[OK] 已保存音频：{audio_path}")
                except Exception as e:
                    print(f"[ERROR] 处理失败：{video_path}，错误：{e}")

if __name__ == "__main__":
    input_folder = r"G:\D20250506_研究生院科普大赛作品副本"
    video_to_audio_recursive(input_folder)
