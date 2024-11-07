import re

cleaned_xml = "影片《垫底辣妹》重要信息 本片分级：PG-13"

# 使用正则表达式匹配 "影片" 和 "重要信息" 之间的字符，并替换
cleaned_xml = re.sub(r"影片《(.*?)》重要信息", r"\n影片《\1》重要信息", cleaned_xml)

print(cleaned_xml)
