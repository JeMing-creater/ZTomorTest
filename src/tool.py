import os

def get_directory_item(path):
    try:
        # 获取指定路径下的所有条目
        entries = os.listdir(path)
        return entries
    except FileNotFoundError:
        print(f"The provided path {path} does not exist.")
        return []