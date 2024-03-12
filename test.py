import re

def extract_description_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

        # 定义正则表达式，匹配 <p align="center"> 到下一个 <br /> 之间的内容
        regex_pattern = r"<p align=\"center\">\s*(.*?)\s*<br />"

        # 使用正则表达式进行匹配
        match = re.search(regex_pattern, file_content, re.DOTALL)

        # 提取匹配到的内容
        if match:
            description = match.group(1).strip()
            return description
        else:
            return "Description not found in {}".format(file_path)

if __name__ == "__main__":
    file_path = "F:\\Project\\Python\\Project\\README_gen\\README.md"
    description = extract_description_from_file(file_path)
    
    if "Description not found" not in description:
        print("File: {}\nDescription: \n{}".format(file_path, description))
    else:
        print(description)
