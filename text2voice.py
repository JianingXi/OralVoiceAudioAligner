import pyttsx3

def text_to_speech(input_file_path, output_file_path, speed=1.2):
    """
    将中文文本文件转换为语音并保存为 MP3 文件，使用 Microsoft Yunyang（男性）声音，速度为1.2倍。

    Args:
        input_file_path (str): 输入文本文件路径。
        output_file_path (str): 输出 MP3 文件路径。
        speed (float): 语速倍率（默认1.2倍）。
    """
    # 初始化 pyttsx3 引擎
    engine = pyttsx3.init()

    # 设置语速
    original_rate = engine.getProperty('rate')
    engine.setProperty('rate', int(original_rate * speed))

    # 设置声音
    voice_id = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\SPEECH_OneCore\\Voices\\Tokens\\MSTTS_V110_zhCN_YunyangM"
    engine.setProperty('voice', voice_id)

    # 读取文本内容
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # 保存为 MP3
        engine.save_to_file(text, output_file_path)
        engine.runAndWait()

        print(f"语音文件已保存为：{output_file_path}")

    except Exception as e:
        print(f"发生错误：{e}")



if __name__ == "__main__":
    # 示例路径，可自行更改
    input_file_path = r"C:\Users\xijia\Desktop\DoingPlatform\D20250428_教创赛省赛决赛答辩\A05写稿\文字转语音循环播放\text1.txt"
    output_file_path = r"C:\Users\xijia\Desktop\DoingPlatform\D20250428_教创赛省赛决赛答辩\A05写稿\文字转语音循环播放\output_fast.mp3"
    text_to_speech(input_file_path, output_file_path, speed=1.6)
    output_file_path = r"C:\Users\xijia\Desktop\DoingPlatform\D20250428_教创赛省赛决赛答辩\A05写稿\文字转语音循环播放\output_norm.mp3"
    text_to_speech(input_file_path, output_file_path, speed=1.1)

    input_file_path = r"C:\Users\xijia\Desktop\DoingPlatform\D20250428_教创赛省赛决赛答辩\A05写稿\文字转语音循环播放\text_p1.txt"
    output_file_path = r"C:\Users\xijia\Desktop\DoingPlatform\D20250428_教创赛省赛决赛答辩\A05写稿\文字转语音循环播放\output_fast_1.mp3"
    text_to_speech(input_file_path, output_file_path, speed=1.6)

    input_file_path = r"C:\Users\xijia\Desktop\DoingPlatform\D20250428_教创赛省赛决赛答辩\A05写稿\文字转语音循环播放\text_p2.txt"
    output_file_path = r"C:\Users\xijia\Desktop\DoingPlatform\D20250428_教创赛省赛决赛答辩\A05写稿\文字转语音循环播放\output_fast_2.mp3"
    text_to_speech(input_file_path, output_file_path, speed=1.6)

    input_file_path = r"C:\Users\xijia\Desktop\DoingPlatform\D20250428_教创赛省赛决赛答辩\A05写稿\文字转语音循环播放\text_p3.txt"
    output_file_path = r"C:\Users\xijia\Desktop\DoingPlatform\D20250428_教创赛省赛决赛答辩\A05写稿\文字转语音循环播放\output_fast_3.mp3"
    text_to_speech(input_file_path, output_file_path, speed=1.6)