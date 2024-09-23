from datetime import datetime

class README_temple():
    def __init__(self):
        pass

    def gen_toplink(self):
        return """<p align="right">(<a href="#top">top</a>)</p>"""

    # 生成 README.md 的 Head 部分
    def gen_Head(self, username, repo_name, title, description):
        return f"""
<div id="top"></div>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
    <a href="https://github.com/{username}/{repo_name}">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
    </a>
<h3 align="center">{title}</h3>
    <p align="center">
    {description}
    <br />
    <a href="https://github.com/{username}/{repo_name}"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/{username}/{repo_name}">View Demo</a>
    ·
    <a href="https://github.com/{username}/{repo_name}/issues">Report Bug</a>
    ·
    <a href="https://github.com/{username}/{repo_name}/issues">Request Feature</a>
    </p>
</div>

"""

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
        Contents = """\n<!-- CONTENTS -->\n<details open>\n  <summary>Contents</summary>\n  <ol>\n"""

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

    # 生成 README.md 的 Filetree 部分
    def gen_Filetree(self, Filetree):
        return f"""
<!-- FILE TREE -->
## File Tree

```
{Filetree}
```

"""

    # 生成 README.md 的 About The Project 部分
    def gen_About_The_Project(self):
        return f"""
<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Here's a blank template to get started: To avoid retyping too much info. Do a search and replace with your text editor for the following: `github_username`, `repo_name`, `twitter_handle`, `linkedin_username`, `email_client`, `email`, `project_title`, `project_description`

"""

    # 生成 README.md 的 Build 部分
    def gen_Build(self):
        return f"""
### Built With

* [Next.js](https://nextjs.org/)
* [React.js](https://reactjs.org/)
* [Vue.js](https://vuejs.org/)
* [Angular](https://angular.io/)
* [Svelte](https://svelte.dev/)
* [Laravel](https://laravel.com)
* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com)

<p align="right">(<a href="#top">top</a>)</p>

"""

    # 生成 README.md 的 Getting Started 部分
    def gen_Getting_Started(self):
        return f"""
<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

"""

    # 生成 README.md 的 Prerequisites 部分
    def gen_Prerequisites(self):
        return f"""
### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
```sh
npm install npm@latest -g
```
<p align="right">(<a href="#top">top</a>)</p>

"""

    # 生成 README.md 的 Installation 部分
    def gen_Installation(self):
        return f"""
### Installation

Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
```sh
git clone https://github.com/your_username_/Project-Name.git
```
3. Install NPM packages
```sh
npm install
```
4. Enter your API in `config.js`
```js
const API_KEY = 'ENTER YOUR API';
```

<p align="right">(<a href="#top">top</a>)</p>

"""

    # 生成 README.md 的 Usage 部分
    def gen_Usage(self):
        return f"""
<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#top">top</a>)</p>

"""

    # 生成 README.md 的 Roadmap 部分
    def gen_Roadmap(self):
        return f"""
<!-- ROADMAP -->
## Roadmap

- [x] Add Changelog
- [x] Add top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Multi-language Support
    - [ ] Chinese
    - [ ] Spanish

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">top</a>)</p>

"""

    # 生成 README.md 的 Verison 部分
    def gen_Verison(self):
        return f"""
<!-- Version -->
## Version

- [x] Add Changelog
- [x] Add top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Multi-language Support
    - [ ] Chinese
    - [ ] Spanish

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">top</a>)</p>

"""

    # 生成 README.md 的 Contributing 部分
    def gen_Contributing(self):
        return f"""
<!-- CONTRIBUTING -->
## Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.
If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
<p align="right">(<a href="#top">top</a>)</p>

"""

    # 生成 README.md 的 License 部分
    def gen_License(self):
        return f"""
<!-- LICENSE -->
## License
Distributed under the MIT License. See `LICENSE` for more information.
<p align="right">(<a href="#top">top</a>)</p>

"""

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
        return f"""
<!-- CONTACT -->
## Contact
{username} - {mail_address}
Project Link: [{username}/{repo_name}](https://github.com/{username}/{repo_name})
<p align="right">(<a href="#top">top</a>)</p>

"""

    # 生成 README.md 的 Acknowledgments 部分
    def gen_Acknowledgments(self):
        return f"""
<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Malven's Flexbox Cheatsheet](https://flexbox.malven.co/)
* [Malven's Grid Cheatsheet](https://grid.malven.co/)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)
* [React Icons](https://react-icons.github.io/react-icons/search)
<p align="right">(<a href="#top">top</a>)</p>

"""

    # 生成 README.md 的 Foot 部分
    def gen_Foot(self, username, repo_name):
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
    print()
