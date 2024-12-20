from datetime import datetime
import re

class README_temple():
    def __init__(self, language='en'):
        self.language = language
        self.file_content = ""
        self.temple_content = ""

        self.pro_name = ""
        self.description = ""
        self.link = ""

        self.head = ""
        self.contents = ""
        self.filetree = ""
        self.about = ""
        self.build = ""
        self.start = ""
        self.prerequisites = ""
        self.installation = ""
        self.usage = ""
        self.roadmap = ""
        self.version = ""
        self.contributing = ""
        self.license = ""
        self.contact = ""
        self.acknowledgments = ""


    def set_filetree(self, filetree):
        self.filetree = filetree

    def extract_contents(self, file):
        if file:
            try:
                with open(file, 'r', encoding='utf-8') as file:
                    self.file_content = file.read()
            except:
                if self.language == 'en':
                    print("No README.md!")
                elif self.language == 'cn':
                    print("No README_cn.md!")
                

        if self.language == 'en':
            temple = 'Temple/temple_blank_en.md'
        elif self.language == 'cn':
            temple = 'Temple/temple_blank_cn.md'
        with open(temple, 'r', encoding='utf-8') as file:
            self.temple_content = file.read()

        self.extract_proname()
        self.extract_description()
        self.extract_filetree()
        self.extract_about()
        self.extract_build()
        self.extract_start()
        self.extract_prerequisites()
        self.extract_installation()
        self.extract_usage()
        self.extract_roadmap()
        self.extract_version()
        self.extract_contributing()
        self.extract_license()
        self.extract_contact()
        self.extract_acknowledgments()

    # 提取当前文件中 README 的 project name
    def extract_proname(self):
        # 定义正则表达式，匹配 <p align="center"> 到下一个 <br /> 之间的内容
        pattern = r'<h3 align="center">(.*?)</h3>'
        # 使用正则表达式进行匹配
        match = re.search(pattern, self.file_content, re.DOTALL)
        # 提取匹配到的内容
        if not match:
            match = re.search(pattern, self.temple_content, re.DOTALL)
        self.pro_name = match.group(1).strip()  # 获取整个匹配的内容

    # 提取当前文件中 README 的 description
    def extract_description(self):
        # 定义正则表达式，匹配 <p align="center"> 到下一个 <br /> 之间的内容
        pattern = r"<p align=\"center\">\s*(.*?)\s*<br />"
        # 使用正则表达式进行匹配
        match = re.search(pattern, self.file_content, re.DOTALL)
        # 提取匹配到的内容
        if not match:
            match = re.search(pattern, self.temple_content, re.DOTALL)
        self.description = match.group(1).strip()  # 获取整个匹配的内容

    # 提取当前文件中 README 的 File Tree
    def extract_filetree(self):
        # 定义正则表达式模式，匹配整个文件树块（包括起始的 HTML 注释、标题和代码块）
        if self.language == 'en':
            pattern = r"<!-- FILE TREE -->\s*## File Tree\s*```(.*?)```"
        elif self.language == 'cn':
            pattern = r"<!-- 文件树 -->\s*## 文件树\s*```(.*?)```"
        # 使用正则表达式进行匹配
        match = re.search(pattern, self.file_content, re.DOTALL)
        # 如果匹配成功，提取并返回整个文件树块
        if not match:
            match = re.search(pattern, self.temple_content, re.DOTALL)
        self.filetree = match.group(1).strip()  # 获取整个匹配的内容

    # 提取当前文件中 README 的 About The Project
    def extract_about(self):
        # 定义正则表达式模式，匹配整个文件树块（包括起始的 HTML 注释、标题和代码块）
        if self.language == 'en':
            pattern = r'<!-- ABOUT THE PROJECT -->\s*## About The Project(.*?)<p align="right">'
        elif self.language == 'cn':
            pattern = r'<!-- 关于本项目 -->\s*## 关于本项目(.*?)<p align="right">'
        # 使用正则表达式进行匹配
        match = re.search(pattern, self.file_content, re.DOTALL)
        # 如果匹配成功，提取并返回整个文件树块
        if not match:
            match = re.search(pattern, self.temple_content, re.DOTALL)
        self.about = match.group(1).strip()  # 获取整个匹配的内容

    # 提取当前文件中 README 的 Built With
    def extract_build(self):
        # 定义正则表达式模式，匹配整个文件树块（包括起始的 HTML 注释、标题和代码块）
        if self.language == 'en':
            pattern = r'### Built With(.*?)<p align="right">'
        elif self.language == 'cn':
            pattern = r'### 构建工具(.*?)<p align="right">'
        # 使用正则表达式进行匹配
        match = re.search(pattern, self.file_content, re.DOTALL)
        # 如果匹配成功，提取并返回整个文件树块
        if not match:
            match = re.search(pattern, self.temple_content, re.DOTALL)
        self.build = match.group(1).strip()  # 获取整个匹配的内容

    # 提取当前文件中 README 的 Getting Started
    def extract_start(self):
        # 定义正则表达式模式，匹配整个文件树块（包括起始的 HTML 注释、标题和代码块）
        if self.language == 'en':
            pattern = r'<!-- GETTING STARTED -->\s*## Getting Started(.*?)<p align="right">'
        elif self.language == 'cn':
            pattern = r'<!-- 开始 -->\s*## 开始(.*?)<p align="right">'
        # 使用正则表达式进行匹配
        match = re.search(pattern, self.file_content, re.DOTALL)
        # 如果匹配成功，提取并返回整个文件树块
        if not match:
            match = re.search(pattern, self.temple_content, re.DOTALL)
        self.start = match.group(1).strip()  # 获取整个匹配的内容

    # 提取当前文件中 README 的 Prerequisites
    def extract_prerequisites(self):
        # 定义正则表达式模式，匹配整个文件树块（包括起始的 HTML 注释、标题和代码块）
        if self.language == 'en':
            pattern = r'### Prerequisites(.*?)### Installation'
        elif self.language == 'cn':
            pattern = r'### 依赖(.*?)### 安装'
        # 使用正则表达式进行匹配
        match = re.search(pattern, self.file_content, re.DOTALL)
        # 如果匹配成功，提取并返回整个文件树块
        if not match:
            match = re.search(pattern, self.temple_content, re.DOTALL)
        self.prerequisites = match.group(1).strip()  # 获取整个匹配的内容

    # 提取当前文件中 README 的 Installation
    def extract_installation(self):
        # 定义正则表达式模式，匹配整个文件树块（包括起始的 HTML 注释、标题和代码块）
        if self.language == 'en':
            pattern = r'### Installation(.*?)<p align="right">'
        elif self.language == 'cn':
            pattern = r'### 安装(.*?)<p align="right">'
        # 使用正则表达式进行匹配
        match = re.search(pattern, self.file_content, re.DOTALL)
        # 如果匹配成功，提取并返回整个文件树块
        if not match:
            match = re.search(pattern, self.temple_content, re.DOTALL)
        self.installation = match.group(1).strip()  # 获取整个匹配的内容

    # 提取当前文件中 README 的 Usage
    def extract_usage(self):
        # 定义正则表达式模式，匹配整个文件树块（包括起始的 HTML 注释、标题和代码块）
        if self.language == 'en':
            pattern = r'<!-- USAGE EXAMPLES -->\s*## Usage(.*?)<p align="right">'
        elif self.language == 'cn':
            pattern = r'<!-- 使用方法 -->\s*## 使用方法(.*?)<p align="right">'
        # 使用正则表达式进行匹配
        match = re.search(pattern, self.file_content, re.DOTALL)
        # 如果匹配成功，提取并返回整个文件树块
        if not match:
            match = re.search(pattern, self.temple_content, re.DOTALL)
        self.usage = match.group(1).strip()  # 获取整个匹配的内容

    # 提取当前文件中 README 的 Roadmap
    def extract_roadmap(self):
        # 定义正则表达式模式，匹配整个文件树块（包括起始的 HTML 注释、标题和代码块）
        if self.language == 'en':
            pattern = r'<!-- ROADMAP -->\s*## Roadmap(.*?)<p align="right">'
        elif self.language == 'cn':
            pattern = r'<!-- 路线图 -->\s*## 路线图(.*?)<p align="right">'
        # 使用正则表达式进行匹配
        match = re.search(pattern, self.file_content, re.DOTALL)
        # 如果匹配成功，提取并返回整个文件树块
        if not match:
            match = re.search(pattern, self.temple_content, re.DOTALL)
        self.roadmap = match.group(1).strip()  # 获取整个匹配的内容

    # 提取当前文件中 README 的 Version
    def extract_version(self):
        # 定义正则表达式模式，匹配整个文件树块（包括起始的 HTML 注释、标题和代码块）
        if self.language == 'en':
            pattern = r'<!-- VERSION -->\s*## Version(.*?)<p align="right">'
        elif self.language == 'cn':
            pattern = r'<!-- 版本 -->\s*## 版本(.*?)<p align="right">'
        # 使用正则表达式进行匹配
        match = re.search(pattern, self.file_content, re.DOTALL)
        # 如果匹配成功，提取并返回整个文件树块
        if not match:
            match = re.search(pattern, self.temple_content, re.DOTALL)
        self.version = match.group(1).strip()  # 获取整个匹配的内容

    # 提取当前文件中 README 的 Contributing
    def extract_contributing(self):
        # 定义正则表达式模式，匹配整个文件树块（包括起始的 HTML 注释、标题和代码块）
        if self.language == 'en':
            pattern = r'<!-- CONTRIBUTING -->\s*## Contributing(.*?)<p align="right">'
        elif self.language == 'cn':
            pattern = r'<!-- 贡献 -->\s*## 贡献(.*?)<p align="right">'
        # 使用正则表达式进行匹配
        match = re.search(pattern, self.file_content, re.DOTALL)
        # 如果匹配成功，提取并返回整个文件树块
        if not match:
            match = re.search(pattern, self.temple_content, re.DOTALL)
        self.contributing = match.group(1).strip()  # 获取整个匹配的内容

    # 提取当前文件中 README 的 Licence
    def extract_license(self):
        # 定义正则表达式模式，匹配整个文件树块（包括起始的 HTML 注释、标题和代码块）
        if self.language == 'en':
            pattern = r'<!-- LICENSE -->\s*## License(.*?)<p align="right">'
        elif self.language == 'cn':
            pattern = r'<!-- 许可证 -->\s*## 许可证(.*?)<p align="right">'
        # 使用正则表达式进行匹配
        match = re.search(pattern, self.file_content, re.DOTALL)
        # 如果匹配成功，提取并返回整个文件树块
        if not match:
            match = re.search(pattern, self.temple_content, re.DOTALL)
        self.license = match.group(1).strip()  # 获取整个匹配的内容

    # 提取当前文件中 README 的 Contact
    def extract_contact(self):
        # 定义正则表达式模式，匹配整个文件树块（包括起始的 HTML 注释、标题和代码块）
        if self.language == 'en':
            pattern = r'<!-- CONTACT -->\s*## Contact(.*?)<p align="right">'
        elif self.language == 'cn':
            pattern = r'<!-- 联系我们 -->\s*## 联系我们(.*?)<p align="right">'
        # 使用正则表达式进行匹配
        match = re.search(pattern, self.file_content, re.DOTALL)
        # 如果匹配成功，提取并返回整个文件树块
        if not match:
            match = re.search(pattern, self.temple_content, re.DOTALL)
        self.contact = match.group(1).strip()  # 获取整个匹配的内容

    # 提取当前文件中 README 的 Acknowledgments
    def extract_acknowledgments(self):
        # 定义正则表达式模式，匹配整个文件树块（包括起始的 HTML 注释、标题和代码块）
        if self.language == 'en':
            pattern = r'<!-- ACKNOWLEDGMENTS -->\s*## Acknowledgments(.*?)<p align="right">'
        elif self.language == 'cn':
            pattern = r'<!-- 致谢 -->\s*## 致谢(.*?)<p align="right">'
        # 使用正则表达式进行匹配
        match = re.search(pattern, self.file_content, re.DOTALL)
        # 如果匹配成功，提取并返回整个文件树块
        if not match:
            match = re.search(pattern, self.temple_content, re.DOTALL)
        self.acknowledgments = match.group(1).strip()  # 获取整个匹配的内容



    def gen_chineselink(self):
        return """**English | [简体中文](README_cn.md)**"""

    def gen_englishlink(self):
        return """**简体中文 | [English](README.md)**"""

    def gen_topid(self):
        return """<div id="top"></div>"""

    def gen_toplink(self):
        return """<p align="right">(<a href="#top">top</a>)</p>"""

    # 生成 README.md 的 Head 部分
    def gen_Head(self, username, repo_name, title, description):
        if self.language == 'en':
            Contents = f"""
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
    <a href="https://github.com/{username}/{repo_name}">
    <img src="Document/images/logo.png" alt="Logo" width="80" height="80">
    </a>
<h3 align="center">{title}</h3>
    <p align="center">
    {description}
    <br />
    <a href="https://github.com/{username}/{repo_name}"><strong>Explore the docs »</strong></a>
    <br />
    <a href="https://github.com/{username}/{repo_name}">View Demo</a>
    ·
    <a href="https://github.com/{username}/{repo_name}/issues">Report Bug</a>
    ·
    <a href="https://github.com/{username}/{repo_name}/issues">Request Feature</a>
    </p>
</div>
"""
            return Contents
        elif self.language == 'cn':
            Contents = f"""
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
    <a href="https://github.com/{username}/{repo_name}">
    <img src="Document/images/logo.png" alt="Logo" width="80" height="80">
    </a>
<h3 align="center">{title}</h3>
    <p align="center">
    {description}
    <br />
    <a href="https://github.com/{username}/{repo_name}"><strong>浏览文档 »</strong></a>
    <br />
    <a href="https://github.com/{username}/{repo_name}">查看 Demo</a>
    ·
    <a href="https://github.com/{username}/{repo_name}/issues">反馈 Bug</a>
    ·
    <a href="https://github.com/{username}/{repo_name}/issues">请求新功能</a>
    </p>
</div>
"""
            return Contents

    # # pattern 1
    # # 生成 README.md 的 Contents 部分
    # def gen_Contents(self, contents):
    #     Contents = """\n<!-- CONTENTS -->\n## Contents\n"""

    #     # 是否开启Filetree
    #     if contents.get('File Tree'):
    #         Contents += """- [File Tree](#file-tree)\n"""
    #     # 是否开启About The Project
    #     if contents.get('About The Project'):
    #         Contents += """- [About The Project](#about-the-project)\n"""
    #         if contents.get('Built With'):
    #             Contents += """  - [Built With](#built-with)\n"""
    #     # 是否开启Getting Started
    #     if contents.get('Getting Started'):
    #         Contents += """- [Getting Started](#getting-started)\n"""
    #         if contents.get('Prerequisites'):
    #             Contents += """  - [Prerequisites](#prerequisites)\n"""
    #         if contents.get('Installation'):
    #             Contents += """  - [Installation](#installation)\n"""
    #     # 是否开启Usage
    #     if contents.get('Usage'):
    #         Contents += """- [Usage](#usage)\n"""
    #     # 是否开启Roadmap
    #     if contents.get('Roadmap'):
    #         Contents += """- [Roadmap](#roadmap)\n"""
    #     # 是否开启Contributing
    #     if contents.get('Contributing'):
    #         Contents += """- [Contributing](#contributing)\n"""
    #     # 是否开启License
    #     if contents.get('License'):
    #         Contents += """- [License](#license)\n"""
    #     # 是否开启Contact
    #     if contents.get('Contact'):
    #         Contents += """- [Contact](#contact)\n"""
    #     # 是否开启Acknowledgments
    #     if contents.get('Acknowledgments'):
    #         Contents += """- [Acknowledgments](#acknowledgments)\n\n"""

    #     return Contents

    # pattern 2
    # 生成 README.md 的 Contents 部分
    def gen_Contents(self, contents):
        if self.language == 'en':
            Contents = """<!-- CONTENTS -->\n<details open>\n  <summary>Contents</summary>\n  <ol>\n"""
            # 是否开启 Filetree
            if contents.get('File Tree'):
                Contents += """    <li><a href="#file-tree">File Tree</a></li>\n"""
            # 是否开启 About The Project
            if contents.get('About The Project'):
                Contents += """    <li>\n      <a href="#about-the-project">About The Project</a>\n      <ul>\n"""
                if contents.get('Built With'):
                    Contents += """        <li><a href="#built-with">Built With</a></li>\n"""
                Contents += """      </ul>\n    </li>\n"""
            # 是否开启 Getting Started
            if contents.get('Getting Started'):
                Contents += """    <li>\n      <a href="#getting-started">Getting Started</a>\n      <ul>\n"""
                if contents.get('Prerequisites'):
                    Contents += """        <li><a href="#prerequisites">Prerequisites</a></li>\n"""
                if contents.get('Installation'):
                    Contents += """        <li><a href="#installation">Installation</a></li>\n"""
                Contents += """      </ul>\n    </li>\n"""
            # 是否开启 Usage
            if contents.get('Usage'):
                Contents += """    <li><a href="#usage">Usage</a></li>\n"""
            # 是否开启 Roadmap
            if contents.get('Roadmap'):
                Contents += """    <li><a href="#roadmap">Roadmap</a></li>\n"""
            # 是否开启 Version
            if contents.get('Version'):
                Contents += """    <li><a href="#version">Version</a></li>\n"""
            # 是否开启 Contributing
            if contents.get('Contributing'):
                Contents += """    <li><a href="#contributing">Contributing</a></li>\n"""
            # 是否开启 License
            if contents.get('License'):
                Contents += """    <li><a href="#license">License</a></li>\n"""
            # 是否开启 Contact
            if contents.get('Contact'):
                Contents += """    <li><a href="#contact">Contact</a></li>\n"""
            # 是否开启 Acknowledgments
            if contents.get('Acknowledgments'):
                Contents += """    <li><a href="#acknowledgments">Acknowledgments</a></li>\n"""
            Contents += """  </ol>\n</details>\n\n"""
            return Contents
        elif self.language == 'cn':
            Contents = """<!-- CONTENTS -->\n<details open>\n  <summary>目录</summary>\n  <ol>\n"""
            # 是否开启 文件树
            if contents.get('文件树'):
                Contents += """    <li><a href="#文件树">文件树</a></li>\n"""
            # 是否开启 关于本项目
            if contents.get('关于本项目'):
                Contents += """    <li>\n      <a href="#关于本项目">关于本项目</a>\n      <ul>\n"""
                if contents.get('构建工具'):
                    Contents += """        <li><a href="#构建工具">构建工具</a></li>\n"""
                Contents += """      </ul>\n    </li>\n"""
            # 是否开启 开始
            if contents.get('开始'):
                Contents += """    <li>\n      <a href="#开始">开始</a>\n      <ul>\n"""
                if contents.get('依赖'):
                    Contents += """        <li><a href="#依赖">依赖</a></li>\n"""
                if contents.get('安装'):
                    Contents += """        <li><a href="#安装">安装</a></li>\n"""
                Contents += """      </ul>\n    </li>\n"""
            # 是否开启 使用方法
            if contents.get('使用方法'):
                Contents += """    <li><a href="#使用方法">使用方法</a></li>\n"""
            # 是否开启 路线图
            if contents.get('路线图'):
                Contents += """    <li><a href="#路线图">路线图</a></li>\n"""
            # 是否开启 版本
            if contents.get('版本'):
                Contents += """    <li><a href="#版本">版本</a></li>\n"""
            # 是否开启 贡献
            if contents.get('贡献'):
                Contents += """    <li><a href="#贡献">贡献</a></li>\n"""
            # 是否开启 许可证
            if contents.get('许可证'):
                Contents += """    <li><a href="#许可证">许可证</a></li>\n"""
            # 是否开启 联系我们
            if contents.get('联系我们'):
                Contents += """    <li><a href="#联系我们">联系我们</a></li>\n"""
            # 是否开启 致谢
            if contents.get('致谢'):
                Contents += """    <li><a href="#致谢">致谢</a></li>\n"""
            Contents += """  </ol>\n</details>\n\n"""
            return Contents

    # 生成 README.md 的 Filetree 部分
    def gen_Filetree(self):
        return f"""'''\n{self.filetree}\n'''"""

    # 生成 README.md 的 About The Project 部分
    def gen_About(self):
        return f"""{self.about}"""

    # 生成 README.md 的 Build 部分
    def gen_Build(self):
        return f"""{self.build}"""

    # 生成 README.md 的 Getting Started 部分
    def gen_Getting_Started(self):
        return f"""{self.start}"""

    # 生成 README.md 的 Prerequisites 部分
    def gen_Prerequisites(self):
        return f"""{self.prerequisites}"""

    # 生成 README.md 的 Installation 部分
    def gen_Installation(self):
        return f"""{self.installation}"""

    # 生成 README.md 的 Usage 部分
    def gen_Usage(self):
        return f"""{self.usage}"""

    # 生成 README.md 的 Roadmap 部分
    def gen_Roadmap(self):
        return f"""{self.roadmap}"""

    # 生成 README.md 的 Verison 部分
    def gen_Verison(self):
        return f"""{self.version}"""

    # 生成 README.md 的 Contributing 部分
    def gen_Contributing(self):
        return f"""{self.contributing}"""

    # 生成 README.md 的 License 部分
    def gen_License(self):
        return f"""{self.license}"""

    # 生成 MIT licsense
    def gen_MIT(self, year=datetime.now().year, author_name='MoonGrt'):
        return f"""
MIT License

Copyright (c) {year} {author_name}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

    # 生成 README.md 的 Contact 部分
    def gen_Contact(self, username, repo_name, mail_address):
        return f"""{username} - {mail_address}
Project Link: [{username}/{repo_name}](https://github.com/{username}/{repo_name})
"""
    # def gen_Contact(self):
    #     return f"""{self.contact}"""

    # 生成 README.md 的 Acknowledgments 部分
    def gen_Acknowledgments(self):
        return f"""{self.acknowledgments}"""


    # 生成 README.md 的 Foot 部分
    def gen_Link(self, username, repo_name):
        return f"""
<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/{username}/{repo_name}.svg?style=for-the-badge
[contributors-url]: https://github.com/{username}/{repo_name}/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/{username}/{repo_name}.svg?style=for-the-badge
[forks-url]: https://github.com/{username}/{repo_name}/network/members
[stars-shield]: https://img.shields.io/github/stars/{username}/{repo_name}.svg?style=for-the-badge
[stars-url]: https://github.com/{username}/{repo_name}/stargazers
[issues-shield]: https://img.shields.io/github/issues/{username}/{repo_name}.svg?style=for-the-badge
[issues-url]: https://github.com/{username}/{repo_name}/issues
[license-shield]: https://img.shields.io/github/license/{username}/{repo_name}.svg?style=for-the-badge
[license-url]: https://github.com/{username}/{repo_name}/blob/master/LICENSE

"""





if __name__ == '__main__':
    # README_content = README_temple()
    README_content = README_temple('cn')
    # README_content.extract_contents('Temple/temple_blank_en.md')
    # README_content.extract_contents('README.md')
    README_content.extract_contents('README_cn.md')

    print(README_content.pro_name + '\n')
    print(README_content.description + '\n')
    print(README_content.filetree + '\n')
    print(README_content.about + '\n')
    print(README_content.build + '\n')
    print(README_content.start + '\n')
    print(README_content.prerequisites + '\n')
    print(README_content.installation + '\n')
    print(README_content.usage + '\n')
    print(README_content.roadmap + '\n')
    print(README_content.version + '\n')
    print(README_content.contributing + '\n')
    print(README_content.license + '\n')
    print(README_content.contact + '\n')
    print(README_content.acknowledgments + '\n')
