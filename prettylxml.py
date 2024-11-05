import os

def list_all_files(directory):
    """
    列出指定目录及其所有子目录中的所有文件。

    :param directory: 要遍历的目录路径
    :return: 包含所有文件路径的列表
    """
    all_files = []

    # 使用 os.walk 遍历目录
    for dirpath, dirnames, filenames in os.walk(directory):
        print(dirpath, filenames)
        for filename in filenames:
            # print(dirpath,filename)
            # 获取文件的完整路径
            full_path = os.path.join(dirpath, filename)
            all_files.append(full_path)

    return all_files

# 示例使用
directory_path = '/opt/lamesbond.github.io/xmls'  # 替换为你要遍历的目录路径
files = list_all_files(directory_path)

# 打印所有找到的文件
# for file in files:
#     print(file)
