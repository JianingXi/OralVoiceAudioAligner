import os


def check_folders_without_txt(directory):
    for root, dirs, files in os.walk(directory):
        # 跳过子文件夹，只针对当前文件夹检查
        if root == directory:
            continue

        # 检查当前文件夹中是否有 .txt 文件
        has_txt = any(file.endswith('.txt') for file in files)

        # 如果没有 .txt 文件，则打印文件夹路径
        if not has_txt:
            print(f"Folder without .txt: {root}")


# 目标目录路径
target_dir = r"G:\作品\科普组\微视频"
check_folders_without_txt(target_dir)
