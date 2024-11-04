import os
import xml.etree.ElementTree as ET

# 主文件路径
main_file = "/opt/lamesbond.github.io/showinfo.xml"
# 单集文件目录
episode_dir = "/opt/lamesbond.github.io/xmls/"
# 输出文件路径
output_file = "/opt/lamesbond.github.io/rss.xml"

# 解析主文件
ET.register_namespace("itunes", "http://www.itunes.com/dtds/podcast-1.0.dtd")
tree = ET.parse(main_file)
root = tree.getroot()

# 获取 <channel> 标签
channel = root.find("channel")

# 迭代单集文件
for episode_file in os.listdir(episode_dir):
    episode_path = os.path.join(episode_dir, episode_file)
    if episode_file.endswith(".xml"):
        # 解析单集文件并找到 <item>
        episode_tree = ET.parse(episode_path)
        episode_root = episode_tree.getroot()
        
        # 将 <item> 添加到 <channel>
        channel.append(episode_root)

# 保存到新的文件
tree.write(output_file, encoding="UTF-8", xml_declaration=True)
print("RSS 文件已成功生成：", output_file)
