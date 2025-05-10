import os
import re

# 替换规则：将大部分特殊字符转换为下划线
def sanitize_name(name: str) -> str:
    # 将数字后面的点替换为下划线，但保留扩展名中的点
    name = re.sub(r'(\d)\.', r'\1_', name)

    # 中文引号、标点、空格、特殊字符等统统替换成下划线
    name = re.sub(r'[“”‘’"\'`。，、；：！？·（）【】《》〈〉·—～！￥…——·|\\/\[\]{}():;<>?@#$%^&*+=\s]', '_', name)
    name = re.sub(r'[-+＋＝·．·]', '_', name)  # 再次替换一些易漏的
    name = re.sub(r'_+', '_', name)  # 连续下划线压缩成一个
    name = name.strip('_')  # 去头尾下划线
    return name

def rename_all_files_and_folders(root_dir: str):
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        # 重命名文件
        for filename in filenames:
            old_path = os.path.join(dirpath, filename)
            base, ext = os.path.splitext(filename)
            new_base = sanitize_name(base)
            new_filename = new_base + ext
            new_path = os.path.join(dirpath, new_filename)
            if old_path != new_path:
                try:
                    os.rename(old_path, new_path)
                    print(f"[File] {old_path} → {new_path}")
                except Exception as e:
                    print(f"[ERROR] 无法重命名文件：{old_path}，原因：{e}")

        # 重命名文件夹
        for dirname in dirnames:
            old_dir_path = os.path.join(dirpath, dirname)
            new_dir_name = sanitize_name(dirname)
            new_dir_path = os.path.join(dirpath, new_dir_name)
            if old_dir_path != new_dir_path:
                try:
                    os.rename(old_dir_path, new_dir_path)
                    print(f"[Folder] {old_dir_path} → {new_dir_path}")
                except Exception as e:
                    print(f"[ERROR] 无法重命名文件夹：{old_dir_path}，原因：{e}")

if __name__ == "__main__":
    root_directory = r"G:\作品"
    rename_all_files_and_folders(root_directory)
