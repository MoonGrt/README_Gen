import sys, os, subprocess, requests, re
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QPlainTextEdit, QFrame, QGridLayout, QComboBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFileDialog, QScrollArea, QSizePolicy, QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from datetime import datetime
from Markdown import Markdown
from FileTree import FileTree
from ContentTree import ContentTree
from README_temple import README_temple
from PicText import PicText
import html2text

class App_window(QWidget):
    def __init__(self):
        super().__init__()
        self.Markdown = Markdown()
        self.README_temple = README_temple()
        self.aboutgen_window = PicText()

        self.readme_content = ''
        self.contents = {}
        self.init_ui()

    def init_ui(self):
        # 设置主窗口属性
        self.resize(1100, 800)
        self.setWindowTitle('README.md Generator')
        self.setWindowIcon(QIcon('images/icons/markdown.svg'))


        # 基本信息
        self.username_label = QLabel('GitHub Username:')
        self.username_input = QLineEdit()
        self.repo_label = QLabel('Repository Name:')
        # self.repo_input = QLineEdit()
        self.repo_input = QComboBox(self)
        self.mail_label = QLabel('Mail address:')
        self.mail_input = QLineEdit()
        self.folder_path_label = QLabel('Folder Path:')
        self.folder_path_input = QLineEdit()
        self.browse_button = QPushButton('Browse', self)
        self.browse_button.clicked.connect(self.browse_folder)
        # Head 信息
        self.title_label = QLabel('Project Title:')
        self.title_input = QLineEdit()
        self.description_label = QLabel('Project Description:')
        self.description_input = QPlainTextEdit()
        self.description_input.setFixedHeight(80)  # 200
        # File tree 信息
        self.markdown_filetree_label = QLabel('Fire Tree:')
        self.markdown_filetree_input = QPlainTextEdit()
        self.markdown_filetree_input.setFixedHeight(200)
        # About The Project 信息
        self.about_label = QLabel('About The Project:')
        self.about_input = QTextEdit()
        self.about_input.setFixedHeight(400)
        self.aboutgen_button = QPushButton('About Gen', self)
        self.aboutgen_button.clicked.connect(self.about_gen)
        # Build with 信息
        self.buildwith_label = QLabel('Build with:')
        self.buildwith_input = QPlainTextEdit()
        self.buildwith_input.setFixedHeight(200)
        # Getting Started 信息
        self.start_label = QLabel('Getting Started:')
        self.start_input = QPlainTextEdit()
        self.start_input.setFixedHeight(200)
        # Prerequisites 信息
        self.prerequisites_label = QLabel('Prerequisites:')
        self.prerequisites_input = QPlainTextEdit()
        self.prerequisites_input.setFixedHeight(200)
        # Installation 信息
        self.installation_label = QLabel('Installation:')
        self.installation_input = QPlainTextEdit()
        self.installation_input.setFixedHeight(200)
        # Usage 信息
        self.usage_label = QLabel('Usage:')
        self.usage_input = QPlainTextEdit()
        self.usage_input.setFixedHeight(200)
        # Roadmap 信息
        self.roadmap_label = QLabel('Roadmap:')
        self.roadmap_input = QPlainTextEdit()
        self.roadmap_input.setFixedHeight(200)
        # Version 信息
        self.version_label = QLabel('Version:')
        self.version_input = QPlainTextEdit()
        self.version_input.setFixedHeight(200)
        # Contributing 信息
        self.contributing_label = QLabel('Contributing:')
        self.contributing_input = QPlainTextEdit()
        self.contributing_input.setFixedHeight(200)
        # License 信息
        self.license_label = QLabel('License:')
        self.license_input = QPlainTextEdit()
        self.license_input.setFixedHeight(200)
        self.MIT_date_label = QLabel('Date:')
        self.MIT_date_input = QLineEdit()
        self.MIT_name_label = QLabel('Name:')
        self.MIT_name_input = QLineEdit()
        self.MIT_label = QLabel('MIT:')
        self.MIT_input = QPlainTextEdit()
        self.MIT_input.setFixedHeight(200)
        # Contact 信息
        self.contact_label = QLabel('Contact:')
        self.contact_input = QPlainTextEdit()
        self.contact_input.setFixedHeight(200)
        # Acknowledgements 信息
        self.acknowledgements_label = QLabel('Acknowledgements:')
        self.acknowledgements_input = QPlainTextEdit()
        self.acknowledgements_input.setFixedHeight(200)

        # 设置信息默认值
        self.username_input.setText('MoonGrt')
        self.mail_input.setText('1561145394@qq.com')
        self.MIT_date_input.setText(str(datetime.now().year))
        self.MIT_name_input.setText('MoonGrt')

        self.MIT_layout = QHBoxLayout()
        self.MIT_layout.addWidget(self.MIT_date_label, 1)
        self.MIT_layout.addWidget(self.MIT_date_input, 2)
        self.MIT_layout.addStretch(1)
        self.MIT_layout.addWidget(self.MIT_name_label, 1)
        self.MIT_layout.addWidget(self.MIT_name_input, 2)

        # repo_input 信息填充
        # 获取用户仓库列表
        repositories = self.get_repoinfo()
        if repositories:
            for repo in repositories:
                self.repo_input.addItem(repo["name"])
        self.title_input.setText(self.repo_input.currentText())

        # 信息链接
        self.username_input.textChanged.connect(self.handle_username_change)
        self.repo_input.currentIndexChanged.connect(self.handle_repo_change)
        self.mail_input.textChanged.connect(self.handle_mail_change)
        self.MIT_name_input.textChanged.connect(self.handle_MIT_name_change)
        self.MIT_date_input.textChanged.connect(self.handle_MIT_name_change)

        # 生成、发送按钮
        self.confirm_button = QPushButton('Gen', self)
        self.confirm_button.clicked.connect(self.GEN)
        self.git_send_button = QPushButton('Git Send', self)
        self.git_send_button.clicked.connect(self.git_send)

        # 内容目录
        self.content_tree = ContentTree()
        self.content_tree.add_items("README.md", [("Head", [], True),
                                               ("Contents", [], True),
                                               ("File Tree", [], True),
                                            #    ("About The Project", ["Built With"]),
                                               ("About The Project", ["Built With"], True),
                                               ("Getting Started", ["Prerequisites", "Installation"]),
                                               ("Usage", []),
                                               ("Roadmap", []),
                                               ("Version", []),
                                               ("Contributing", [], True),
                                               ("License", [], True),
                                               ("Contact", [], True),
                                               ("Acknowledgments", [], True)], True, True)  # parent child checked expanded
        self.content_tree.add_items("requirements.txt")
        self.content_tree.add_items("run.bat")
        self.content_tree.itemChanged.connect(self.handle_contenttree_changed)

        # 文件树
        self.file_tree = FileTree()
        self.file_tree.itemChanged.connect(self.handle_filetree_changed)


        # 左侧布局
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.content_tree)
        left_layout.addWidget(self.file_tree)

        # 右侧布局
        self.grid_layout = QGridLayout(self)
        self.update_form_layout(self.content_tree.get_items_state())
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.set_gridcolwidth_ratios([1, 2])

        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.grid_layout)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.confirm_button)
        bottom_layout.addWidget(self.git_send_button)

        right_layout = QVBoxLayout()
        right_layout.addWidget(scroll_area)
        right_layout.addLayout(bottom_layout)


        # 总体布局 左右
        layout = QHBoxLayout()
        layout.addLayout(left_layout, 1)
        layout.addLayout(right_layout, 3)
        self.setLayout(layout)


    # 添加组件到 grid_layout
    def add_grid(self, *widgets):
        # 如果没有传入任何组件，则添加空行或空行
        if not widgets:
            # 创建横线
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            self.grid_layout.addWidget(line, self.grid_layout.rowCount(), 0, 1, -1)
        else:
            # 获取当前行数
            row_position = self.grid_layout.rowCount()

            # 如果只有一个组件，则设置其占据整行
            if len(widgets) == 1:
                if isinstance(widgets[0], QWidget):
                    widgets[0].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                    self.grid_layout.addWidget(widgets[0], row_position, 0, 1, -1)
                elif isinstance(widgets[0], QHBoxLayout):
                    self.grid_layout.addLayout(widgets[0], row_position, 0, 1, -1)
            else:
                # 将组件添加到布局的下一行
                for col, widget in enumerate(widgets):
                    widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                    self.grid_layout.addWidget(widget, row_position, col)

    # 处理 username 变化
    def handle_username_change(self, new_text):
        self.contact_input.setPlainText(self.README_temple.gen_Contact(self.username_input.text(), self.repo_input.currentText(), self.mail_input.text()))

    # 处理 repo 变化
    def handle_repo_change(self, new_text):
        self.title_input.setText(self.repo_input.currentText())

    # 处理 mail 变化
    def handle_mail_change(self, new_text):
        self.contact_input.setPlainText(self.README_temple.gen_Contact(self.username_input.text(), self.repo_input.currentText(), self.mail_input.text()))

    # 处理 MIT_date 变化
    def handle_MIT_date_change(self, new_text):
        self.MIT_input.setPlainText(self.README_temple.gen_MIT(self.MIT_date_input.text(), self.MIT_name_input.text()))

    # 处理 MIT_name 变化
    def handle_MIT_name_change(self, new_text):
        self.MIT_input.setPlainText(self.README_temple.gen_MIT(self.MIT_date_input.text(), self.MIT_name_input.text()))

    # 设置每列的宽度比例
    def set_gridcolwidth_ratios(self, ratios):
        for col, ratio in enumerate(ratios):
            self.grid_layout.setColumnStretch(col, ratio)

    def get_repoinfo(self):
        url = f"https://api.github.com/users/{self.username_input.text()}/repos"
        response = requests.get(url)

        if response.status_code == 200:
            repositories = response.json()
            return repositories
        else:
            print(f"Error: Unable to fetch repositories. Status code: {response.status_code}")
            return None

    # 浏览文件夹
    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select File or Folder")
        if folder_path:
            self.folder_path_input.setText(folder_path)
            self.file_tree.clear()
            self.file_tree.add_items(self.file_tree.root, folder_path)
            
            self.README_temple.extract_contents(self.folder_path_input.text() + '/README.md')
            self.fill_README()

    # 将已有的 README 或者 temple README 中内容填入 GUI
    def fill_README(self):
        self.description_input.setPlainText(self.README_temple.description)

        self.markdown_filetree_input.setPlainText(self.README_temple.filetree)
        self.about_input.setPlainText(self.README_temple.about)
        self.buildwith_input.setPlainText(self.README_temple.build)
        self.start_input.setPlainText(self.README_temple.start)
        self.prerequisites_input.setPlainText(self.README_temple.prerequisites)
        self.installation_input.setPlainText(self.README_temple.installation)
        self.usage_input.setPlainText(self.README_temple.usage)
        self.roadmap_input.setPlainText(self.README_temple.roadmap)
        self.version_input.setPlainText(self.README_temple.version)
        self.contributing_input.setPlainText(self.README_temple.contributing)
        self.license_input.setPlainText(self.README_temple.license)
        self.MIT_input.setPlainText(self.README_temple.gen_MIT())
        self.contact_input.setPlainText(self.README_temple.contact)
        self.acknowledgements_input.setPlainText(self.README_temple.acknowledgments)

    # 生成 about
    def about_gen(self):
        # 点击按钮后创建并显示文本编辑器窗口
        self.aboutgen_window.show()
        self.aboutgen_window.closeEvent = self.set_about

    def set_about(self, event):
        markdown_content = html2text.html2text(self.aboutgen_window.get_text())
        self.about_input.setPlainText(markdown_content)

    # 发送到github仓库
    def git_send(self):
        # 切换到用户指定的文件夹
        dir = self.folder_path_input.text()
        if os.path.exists(dir):
            os.chdir(dir)
        else:
            print("Please select a folder")
            return

        # 检查当前目录是否包含.git文件夹，以确定是否已进行git初始化
        if not os.path.exists('.git'):
            # 如果未初始化，则执行git初始化
            subprocess.run(['git', 'init'])
            print("Git initialized.")

        # 检查是否已有远程仓库
        remote_output = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
        if 'origin' not in remote_output.stdout:
            # 如果没有远程仓库，则添加
            # 获取远程仓库URL，替换为你自己的GitHub仓库URL
            repository_url = f"https://github.com/{self.username_input.text()}/{self.repo_input.currentText()}.git"
            subprocess.run(['git', 'remote', 'add', 'origin', repository_url])
            print(f"Remote repository added: {repository_url}")

        # 将所有更改添加到暂存区
        subprocess.run(['git', 'add', '.'])
        # 检查是否有未提交的更改
        status_output = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        if not status_output.stdout:
            print("No changes to commit.")
            return
        # 提交更改
        subprocess.run(['git', 'commit', '-m', 'Commit changes'])

        # 获取当前分支名称
        branch_output = subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True)
        current_branch = branch_output.stdout.strip()

        # 将更改推送到GitHub的当前分支
        remote_info = subprocess.run(['git', 'remote', 'show', 'origin'], capture_output=True, text=True)
        if 'unknown' in remote_info.stdout:
            # 如果没有上游分支，则使用 -u 参数设置上游分支
            subprocess.run(['git', 'push', '-u', 'origin', current_branch])
        else:
            # 如果已有上游分支，则直接推送
            subprocess.run(['git', 'push', '-f', 'origin', current_branch])

        print(f"Changes pushed to {current_branch} on GitHub.")

    # 将FileTree类的handle_item_changed函数移到这里：file_tree选项的选择要影响窗口内容
    def handle_filetree_changed(self, item, column):
        # 处理选项状态改变时的逻辑
        if item.childCount() > 0:  # 只处理文件夹
            if item.checkState(0) == 0:
                for i in range(item.childCount()):
                    child_item = item.child(i)
                    child_item.setCheckState(0, 0)  # 如果母选项未选中，则禁用子选项的选择功能
                    child_item.setDisabled(True)
            elif item.checkState(0) == 2:
                for i in range(item.childCount()):
                    child_item = item.child(i)
                    child_item.setDisabled(False)
                    # if child_item.text(0) != '.git':
                    #     child_item.setCheckState(0, 2)  # 如果母选项选中，则开启子选项的选择功能
        # 根据用户的选择改变 markdown_filetree_input
        # self.markdown_filetree_input.setPlainText(self.README_temple.gen_Filetree())

    # 将ContentTree类的handle_item_changed函数移到这里：content_tree选项的选择要影响窗口部件
    def handle_contenttree_changed(self, item, column):
        # 处理选项状态改变时的逻辑
        if item.childCount() > 0:  # 只处理文件夹
            if item.checkState(0) == 0:
                for i in range(item.childCount()):
                    child_item = item.child(i)
                    # child_item.setCheckState(0, 0)  # 如果母选项未选中，则禁用子选项的选择功能
                    child_item.setDisabled(True)
            elif item.checkState(0) == 2:
                for i in range(item.childCount()):
                    child_item = item.child(i)
                    # child_item.setCheckState(0, 2)  # 如果母选项选中，则开启子选项的选择功能
                    child_item.setDisabled(False)
        contents = self.content_tree.get_items_state()
        self.update_form_layout(contents)

    # 根据用户选择的内容更新窗口
    def update_form_layout(self, contents):
        # 清空self.grid_layout
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                # 移除组件，但保留widget
                self.grid_layout.removeWidget(widget)
                widget.setParent(None)

        # 是否开启 README
        if contents.get('README.md'):
            # 添加基础内容
            self.add_grid(self.username_label, self.username_input)
            self.add_grid(self.repo_label, self.repo_input)
            self.add_grid(self.mail_label, self.mail_input)
            self.add_grid(self.folder_path_label, self.browse_button)
            self.add_grid(self.folder_path_input)
            self.add_grid()
            # 是否开启 Head
            if contents.get('Head'):
                self.add_grid(self.title_label, self.title_input)
                self.add_grid(self.description_label)
                self.add_grid(self.description_input)
                self.add_grid()
            # 是否开启 Contents
            if contents.get('Contents'):
                pass
            # 是否开启 Filetree
            if contents.get('File Tree'):
                self.add_grid(self.markdown_filetree_label)
                self.add_grid(self.markdown_filetree_input)
                self.file_tree.setEnabled(True)
                self.add_grid()
            else:
                self.file_tree.setEnabled(False)
            # 是否开启 About The Project
            if contents.get('About The Project'):
                self.add_grid(self.about_label, self.aboutgen_button)
                self.add_grid(self.about_input)
                self.add_grid()
                if contents.get('Built With'):
                    self.add_grid(self.buildwith_label)
                    self.add_grid(self.buildwith_input)
                    self.add_grid()
            # 是否开启 Getting Started
            if contents.get('Getting Started'):
                self.add_grid(self.start_label)
                self.add_grid(self.start_input)
                self.add_grid()
                if contents.get('Prerequisites'):
                    self.add_grid(self.prerequisites_label)
                    self.add_grid(self.prerequisites_input)
                    self.add_grid()
                if contents.get('Installation'):
                    self.add_grid(self.installation_label)
                    self.add_grid(self.installation_input)
                    self.add_grid()
            # 是否开启 Usage
            if contents.get('Usage'):
                self.add_grid(self.usage_label)
                self.add_grid(self.usage_input)
                self.add_grid()
            # 是否开启 Roadmap
            if contents.get('Roadmap'):
                self.add_grid(self.roadmap_label)
                self.add_grid(self.roadmap_input)
                self.add_grid()
            # 是否开启 Version
            if contents.get('Version'):
                self.add_grid(self.version_label)
                self.add_grid(self.version_input)
                self.add_grid()
            # 是否开启 Contributing
            if contents.get('Contributing'):
                self.add_grid(self.contributing_label)
                self.add_grid(self.contributing_input)
                self.add_grid()
            # 是否开启 License
            if contents.get('License'):
                self.add_grid(self.license_label)
                self.add_grid(self.license_input)
                self.add_grid(self.MIT_label)
                self.add_grid(self.MIT_layout)
                self.add_grid(self.MIT_input)
                self.add_grid()
            # 是否开启 Contact
            if contents.get('Contact'):
                self.add_grid(self.contact_label)
                self.add_grid(self.contact_input)
                self.add_grid()
            # 是否开启 Acknowledgments
            if contents.get('Acknowledgments'):
                self.add_grid(self.acknowledgements_label)
                self.add_grid(self.acknowledgements_input)
                self.add_grid()

        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.set_gridcolwidth_ratios([1, 2])

    def GEN(self):
        self.contents = self.content_tree.get_items_state()
        if self.contents.get('requirements.txt'):
            # 生成 requirements.txt
            self.generate_requirements()
        if self.contents.get('run.bat'):
            # 生成 run.bat
            self.generate_run_bat()
        if self.contents.get('README.md'):
            # 生成 README.md
            content = self.content_tree.get_tree_structure()
            print(content)
            
            print(self.generate_readme1(content))

    def generate_readme1(self, content, level=2):
        markdown = ""
        for section in content:
            for key, value in section.items():
                if value is True:
                    # Add the section title with corresponding heading level
                    # markdown += f"<!-- {key.upper()} -->\n"
                    markdown += f"{'#' * level} {key}\n\n"
                    markdown += self.generate_sections(key)
                    if 'children' in section and section['children']:
                        # Recursively add the child sections
                        markdown += self.generate_readme1(section['children'], level + 1)
        return markdown

    def generate_sections(self, section):
        # 生成 README.md 的 Head 部分
        if section == 'Head':
            title = self.title_input.text()
            description = self.description_input.toPlainText()
            return self.README_temple.gen_Head(self.username_input.text(), self.repo_input.currentText(), title, description)
        # 生成 README.md 的 Contents 部分
        if section == 'Contents':
            return self.README_temple.gen_Contents(self.contents)
        # 生成 README.md 的 File tree 部分
        if section == 'File Tree':
            return self.README_temple.gen_Filetree()
        # 生成 README.md 的 About The Project 部分
        if section == 'About The Project':
            return self.README_temple.gen_About()
        if section == 'Built With':
            return self.README_temple.gen_Build()
        # 生成 README.md 的 Getting Started 部分
        if section == 'Getting Started':
            return self.README_temple.gen_Getting_Started()
        if section == 'Prerequisites':
            return self.README_temple.gen_Prerequisites()
        if section == 'Installation':
            return self.README_temple.gen_Installation()
        # 生成 README.md 的 Usage 部分
        if section == 'Usage':
            return self.README_temple.gen_Usage()
        # 生成 README.md 的 Roadmap 部分
        if section == 'Roadmap':
            return self.README_temple.gen_Roadmap()
        # 生成 README.md 的 Version 部分
        if section == 'Version':
            return self.README_temple.gen_Verison()
        # 生成 README.md 的 Contributing 部分
        if section == 'Contributing':
            return self.README_temple.gen_Contributing()
        # 生成 README.md 的 License 部分
        if section == 'License':
            return self.README_temple.gen_License()
        # 生成 README.md 的 Contact 部分
        if section == 'Contact':
            return self.README_temple.gen_Contact()
        # 生成 README.md 的 Acknowledgments 部分
        if section == 'Acknowledgments':
            return self.README_temple.gen_Acknowledgments()
        # 生成 README.md 的 Foot 部分
        if section == 'Head':
            return self.README_temple.gen_Foot(self.username_input.text(), self.repo_input.currentText())



    def generate_readme(self):
        username = self.username_input.text()
        repo_name = self.repo_input.currentText()
        self.readme_content = ''

        # 生成 README.md 的 Head 部分
        if self.contents.get('Head'):
            title = self.title_input.text()
            description = self.description_input.toPlainText()
            self.readme_content += self.README_temple.gen_Head(username, repo_name, title, description)
        # 生成 README.md 的 Contents 部分
        if self.contents.get('Contents'):
            self.readme_content += self.README_temple.gen_Contents(self.contents)
        # 生成 README.md 的 File tree 部分
        if self.contents.get('File Tree'):
            # self.readme_content += gen_Filetree(self.file_tree.get_markdown_tree())
            self.readme_content += self.markdown_filetree_input.toPlainText()
        # 生成 README.md 的 About The Project 部分
        if self.contents.get('About The Project'):
            self.readme_content += self.about_input.toPlainText()
            if self.contents.get('Built With'):
                self.readme_content += self.buildwith_input.toPlainText()
        # 生成 README.md 的 Getting Started 部分
        if self.contents.get('Getting Started'):
            self.readme_content += self.start_input.toPlainText()
            if self.contents.get('Prerequisites'):
                self.readme_content += self.prerequisites_input.toPlainText()
            if self.contents.get('Installation'):
                self.readme_content += self.installation_input.toPlainText()
        # 生成 README.md 的 Usage 部分
        if self.contents.get('Usage'):
            self.readme_content += self.usage_input.toPlainText()
        # 生成 README.md 的 Roadmap 部分
        if self.contents.get('Roadmap'):
            self.readme_content += self.roadmap_input.toPlainText()
        # 生成 README.md 的 Version 部分
        if self.contents.get('Version'):
            self.readme_content += self.version_input.toPlainText()
        # 生成 README.md 的 Contributing 部分
        if self.contents.get('Contributing'):
            # self.readme_content += gen_Contributing()
            self.readme_content += self.contributing_input.toPlainText()
        # 生成 README.md 的 License 部分
        if self.contents.get('License'):
            # self.readme_content += gen_License()
            self.readme_content += self.license_input.toPlainText()
        # 生成 README.md 的 Contact 部分
        if self.contents.get('Contact'):
            # self.readme_content += gen_Contact(username, repo_name, mail_address)
            self.readme_content += self.contact_input.toPlainText()
        # 生成 README.md 的 Acknowledgments 部分
        if self.contents.get('Acknowledgments'):
            # self.readme_content += gen_Acknowledgments()
            self.readme_content += self.acknowledgements_input.toPlainText()
        # 生成 README.md 的 Foot 部分
        if self.contents.get('Head'):
            self.readme_content += self.README_temple.gen_Foot(username, repo_name)

        self.Markdown.markdown_show(self.readme_content, self.MIT_input.toPlainText(), self.folder_path_input.text(), self.contents)

    def generate_requirements(self, path='.'):
        subprocess.run(['pipreqs', path, '--force'], check=True)

    def generate_run_bat(self):
        # TODO: 有问题
        batch_content = f"@echo off\npython {os.path.abspath(__file__)}"
        print(batch_content)
        with open('run.bat', 'w') as file:
            file.write(batch_content)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App_window()
    window.show()
    sys.exit(app.exec_())



# TODO: 如果文件夹下有 README 则将相应内容填充到窗口，文件树的填充有问题
# TODO: 自动识别仓库名
# TODO: 添加对git异常的处理：fatal: detected dubious ownership in repository at 'U:/xxx'
#       添加 ”git config --global --add safe.directory U:/xxx“
# TODO: 新建文件（图片等）后更新文件树
# TODO: 添加“图片展示功能”
# TODO: 中英文版本
# TODO: 添加release版本控制
# TODO: 添加版本更新说明

# TODO: git branch
