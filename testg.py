import os
import re

directory = "/opt/lamesbond.github.io/xmls/fanpai-erpangfeng"

for filename in os.listdir(directory):
    if filename.endswith(".xml"):
        # 读取文件
        # input_file = os.path.join(directory, filename)
        # 读取文件内容
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # 定义处理后的内容列表
        new_lines = []

        # 处理每一行
        for line in lines:
            if "重要信息：" in line:

                # 使用正则表达式进行替换，仅在“重要信息：”后有内容时添加换行符
                modified_line = re.sub(r'(重要信息：)(\S)', r'\1\n\2', line)
                print(modified_line)
                new_lines.append(modified_line)
            else:
                new_lines.append(line)

        # 将修改后的内容写回文件
        with open(filename, "w", encoding="utf-8") as file:
            file.writelines(new_lines)

        # print(filename,"文件已成功修改为：\n",new_lines)