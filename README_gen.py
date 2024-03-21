import sys, os, subprocess, shutil, requests, re
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QPlainTextEdit, QFrame, QGridLayout, QComboBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem, QFileDialog, QScrollArea, QSizePolicy, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from datetime import datetime

class FileTree(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(1)
        self.setHeaderLabels(["File Tree"])
        self.root = self.invisibleRootItem()

    # 添加文件、文件夹到文件树中
    def add_items(self, parent_item, path, parent_is_root=True):
        # 存储文件夹和文件
        folders = []
        files = []

        for item_name in os.listdir(path):
            item_path = os.path.join(path, item_name)
            if os.path.isdir(item_path):
                folders.append(item_name)
            else:
                files.append(item_name)

        # 首先添加文件夹，然后添加文件
        for item_name in folders + files:
            item_path = os.path.join(path, item_name)
            item = QTreeWidgetItem(parent_item, [item_name])

            if parent_is_root:  # 如果是第一层，设置默认勾选
                if item_name != '.git':
                    item.setCheckState(0, 2)
                else:
                    item.setCheckState(0, 0)
            else:
                item.setCheckState(0, 0)

            if os.path.isdir(item_path):
                self.add_items(item, item_path, False)

            # # 发射 itemChanged 信号，模拟用户手动更改选项的操作
            # self.itemChanged.emit(item, 0)

    # 获取用户选择的文件、文件夹生成的markdown文件树
    def get_markdown_tree(self):
        return "└─ Project\n" + self.get_markdown_tree_recurse(self.root)

    # 递归生成markdown文件树
    def get_markdown_tree_recurse(self, item, indent='', last=False):
        content = ""
        if item.childCount() == 0:
            return content

        # pattern 1
        # indent += '  '
        # for i in range(item.childCount()):
        #     child_item = item.child(i)
        #     item_name = child_item.text(0)

        #     if child_item.checkState(0) == 2:
        #         if child_item.childCount() > 0:
        #             content += f"{indent}- /{item_name}/\n"
        #         else:
        #             content += f"{indent}- {item_name}\n"
        #         content += self.get_markdown_tree_recurse(child_item, indent, True)


        # # pattern 2
        # indent += '   ' if last or item == self.root else '│  '
        # for i in range(item.childCount()):
        #     child_item = item.child(i)
        #     item_name = child_item.text(0)
        #     is_last = i==item.childCount()-1

        #     if child_item.checkState(0) == 2:
        #         if child_item.childCount() > 0:
        #             content += indent + ('└─ ' if is_last else '├─ ') + '/' + item_name + '/\n'
        #             content += self.get_markdown_tree_recurse(child_item, indent, is_last)
        #         else:
        #             content += indent + ('└─ ' if is_last else '├─ ') + item_name + '\n'


        # pattern 3
        indent += '  ' if last or item == self.root else '│ '

        # 统计文件和文件夹数
        file_cnt = 0
        folder_cnt = 0
        for i in range(item.childCount()):
            child_item = item.child(i)
            if child_item.checkState(0) == 2 and child_item.childCount() == 0:
                file_cnt += 1
            elif child_item.checkState(0) == 2 and child_item.childCount() > 0:
                folder_cnt += 1

        # 处理文件类型的子项
        if file_cnt:
            index = 0
            for i in range(item.childCount()):
                child_item = item.child(i)
                item_name = child_item.text(0)
                is_last = index == file_cnt - 1

                if child_item.checkState(0) == 2 and child_item.childCount() == 0:
                    index += 1
                    content += indent + ('└─ ' if not folder_cnt and is_last else '├─ ') + item_name + '\n'

        # 处理文件夹类型的子项
        if folder_cnt:
            index = 0
            for i in range(item.childCount()):
                child_item = item.child(i)
                item_name = child_item.text(0)
                is_last = index == folder_cnt - 1
                # last = i == folder_cnt

                if child_item.checkState(0) == 2 and child_item.childCount() > 0:
                    index += 1
                    content += indent + ('└─ ' if is_last else '├─ ') + '/' + item_name + '/\n'
                    content += self.get_markdown_tree_recurse(child_item, indent, is_last)

        return content

    # def handle_item_changed(self, item, column):
    #     # 处理选项状态改变时的逻辑
    #     if item.childCount() > 0:  # 只处理文件夹
    #         if item.checkState(0) == 0:  # 如果母选项未选中，则禁用子选项的选择功能
    #             for i in range(item.childCount()):
    #                 child_item = item.child(i)
    #                 child_item.setCheckState(0, 0)
    #                 child_item.setDisabled(True)
    #         elif item.checkState(0) == 2:  # 如果母选项选中，则开启子选项的选择功能
    #             for i in range(item.childCount()):
    #                 child_item = item.child(i)
    #                 child_item.setDisabled(False)
    #                 child_item.setCheckState(0, 2)

class ContentTree(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(1)
        self.setHeaderLabels(["Content"])
        self.root = self.invisibleRootItem()

    # 将内容项添加内容树中
    def add_items(self, parent_text, children=None, default_checked=False):
        parent_item = QTreeWidgetItem(self.root, [parent_text])
        parent_item.setCheckState(0, 2 if default_checked else 0)  # 设置复选框状态，默认选中或不选中
        if children:
            for child_text in children:
                child_item = QTreeWidgetItem(parent_item)
                child_item.setCheckState(0, 0)
                child_item.setText(0, child_text)
                # parent_item.setExpanded(True)
                # if not default_checked: 
                #     child_item.setDisabled(True)
        # else:

    # 获取内容树项目内容
    def get_items_state(self):
        result = {}
        for i in range(self.root.childCount()):
            child_item = self.root.child(i)
            self.get_items_recurse(child_item, result)
        return result

    def get_items_recurse(self, item, result):
        item_text = item.text(0)
        item_state = item.checkState(0)
        result[item_text] = item_state

        for i in range(item.childCount()):
            child_item = item.child(i)
            self.get_items_recurse(child_item, result)

    # def handle_item_changed(self, item, column):
    #     # 处理选项状态改变时的逻辑
    #     if item.childCount() > 0:  # 只处理文件夹
    #         if item.checkState(0) == 0:  # 如果母选项未选中，则禁用子选项的选择功能
    #             for i in range(item.childCount()):
    #                 child_item = item.child(i)
    #                 child_item.setCheckState(0, 0)
    #                 child_item.setDisabled(True)
    #         elif item.checkState(0) == 2:  # 如果母选项选中，则开启子选项的选择功能
    #             for i in range(item.childCount()):
    #                 child_item = item.child(i)
    #                 child_item.setDisabled(False)
    #                 child_item.setCheckState(0, 2)


# 完整 markdown 显示窗口
class Markdown_display(QWidget):
    def __init__(self):
        super().__init__()
        self.markdown = ''
        self.path = ''

        # 设置主窗口属性
        self.setGeometry(420, 220, 1100, 800)   # 设置窗口左上角位置为 (x, y)，宽度为 w，高度为 h
        self.setWindowTitle('Markdown display')
        self.setWindowIcon(QIcon('icons/markdown.svg'))

        self.text_edit = QPlainTextEdit()
        self.confirm_button = QPushButton("Generate")
        self.confirm_button.clicked.connect(self.save_markdown)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    # 显示 markdown
    def markdown_show(self, markdown, MIT_license, path, contents):
        self.markdown = markdown
        self.path = path
        self.contents = contents
        self.MIT_license = MIT_license
        self.text_edit.setPlainText(self.markdown)

    # 保存 markdown 到文件
    def save_markdown(self):
        if self.path:
            # 将 License 内容保存到文件中
            readme_path = self.path+'/LICENSE'
            with open(readme_path, 'w', encoding='utf-8') as readme_file:
                readme_file.write(self.MIT_license)
            print(f"LICENSE generated successfully at {readme_path}")

            # 将readme_content内容保存到文件中
            readme_path = self.path+'/README.md'
            with open(readme_path, 'w', encoding='utf-8') as readme_file:
                readme_file.write(self.markdown)
            print(f"README.md generated successfully at {readme_path}")

            self.copy_images_folder()
        else:
            QMessageBox.information(self, "Message", "Please select a folder")

        self.close()

    def copy_images_folder(self):        
        # 获取当前目录下的 'images' 文件夹路径
        source_folder = os.path.join(os.getcwd(), 'images')

        # 检查 'images' 文件夹是否存在
        if not os.path.exists(source_folder):
            print("错误：当前目录下找不到 'images' 文件夹。")
            return

        # 检查目标文件夹是否存在，如果不存在则创建
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            print(f"已创建目标文件夹：{self.path}")

        # 构建目标文件夹中 'images' 文件夹的路径
        destination_path = os.path.join(self.path, 'images')

        try:
            # 使用 shutil.copytree 复制 'images' 文件夹到目标文件夹
            shutil.copytree(source_folder, destination_path)
            print(f"成功将 'images' 文件夹复制到 {self.path}")
        except shutil.Error as e:
            print(f"复制 'images' 文件夹时发生错误：{e}")
        except Exception as e:
            print(f"{e}")


class App_window(QWidget):
    def __init__(self):
        super().__init__()
        self.readme_content = ''
        self.contents = {}
        self.init_ui()

    def init_ui(self):
        # 设置主窗口属性
        self.setGeometry(400, 200, 1100, 800)   # 设置窗口左上角位置为 (x, y)，宽度为 w，高度为 h
        self.setWindowTitle('README.md Generator')
        self.setWindowIcon(QIcon('icons/markdown.svg'))


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
        self.description_input.setFixedHeight(200)
        # File tree 信息
        self.markdown_filetree_label = QLabel('Fire Tree:')
        self.markdown_filetree_input = QPlainTextEdit()
        self.markdown_filetree_input.setFixedHeight(200)
        # About The Project 信息
        self.about_label = QLabel('About The Project:')
        self.about_input = QPlainTextEdit()
        self.about_input.setFixedHeight(200)
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
        # self.repo_input.setText('python_tool')
        self.mail_input.setText('1561145394@qq.com')
        self.MIT_date_input.setText(str(datetime.now().year))
        self.MIT_name_input.setText('MoonGrt')

        # self.description_input.setPlainText()
        # self.markdown_filetree_input.setPlainText()
        self.about_input.setPlainText(gen_About_The_Project())
        self.buildwith_input.setPlainText(gen_Build())
        self.start_input.setPlainText(gen_Getting_Started())
        self.prerequisites_input.setPlainText(gen_Prerequisites())
        self.installation_input.setPlainText(gen_Installation())
        self.usage_input.setPlainText(gen_Usage())
        self.roadmap_input.setPlainText(gen_Roadmap())
        self.version_input.setPlainText(gen_Verison())
        self.contributing_input.setPlainText(gen_Contributing())
        self.license_input.setPlainText(gen_License())
        self.MIT_input.setPlainText(gen_MIT())
        self.contact_input.setPlainText(gen_Contact(self.username_input.text(), self.repo_input.currentText(), self.mail_input.text()))
        self.acknowledgements_input.setPlainText(gen_Acknowledgments())

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
        self.confirm_button = QPushButton('Confirm', self)
        self.confirm_button.clicked.connect(self.generate_readme)
        self.git_send_button = QPushButton('Git Send', self)
        self.git_send_button.clicked.connect(self.git_send)

        # 内容目录
        self.content_tree = ContentTree()
        self.content_tree.add_items("Head", default_checked=True)
        self.content_tree.add_items("Contents", default_checked=True)
        self.content_tree.add_items("File Tree", default_checked=True)
        self.content_tree.add_items("About The Project", ["Built With"])
        self.content_tree.add_items("Getting Started", ["Prerequisites", "Installation"])
        self.content_tree.add_items("Usage")
        self.content_tree.add_items("Roadmap")
        self.content_tree.add_items("Version")
        self.content_tree.add_items("Contributing", default_checked=True)
        self.content_tree.add_items("License", default_checked=True)
        self.content_tree.add_items("Contact", default_checked=True)
        self.content_tree.add_items("Acknowledgments", default_checked=True)
        self.content_tree.itemChanged.connect(self.content_tree_handle_item_changed)

        # 文件树
        self.file_tree = FileTree()
        self.file_tree.itemChanged.connect(self.file_tree_handle_item_changed)



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
            # 创建空行
            # empty_widget = QWidget()
            # empty_widget.setFixedHeight(20)
            # self.grid_layout.addWidget(empty_widget, self.grid_layout.rowCount(), 0, 1, -1)

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
        self.contact_input.setPlainText(gen_Contact(self.username_input.text(), self.repo_input.currentText(), self.mail_input.text()))

    # 处理 repo 变化
    def handle_repo_change(self, new_text):
        self.title_input.setText(self.repo_input.currentText())

    # 处理 mail 变化
    def handle_mail_change(self, new_text):
        self.contact_input.setPlainText(gen_Contact(self.username_input.text(), self.repo_input.currentText(), self.mail_input.text()))

    # 处理 MIT_date 变化
    def handle_MIT_date_change(self, new_text):
        self.MIT_input.setPlainText(gen_MIT(self.MIT_date_input.text(), self.MIT_name_input.text()))

    # 处理 MIT_name 变化
    def handle_MIT_name_change(self, new_text):
        self.MIT_input.setPlainText(gen_MIT(self.MIT_date_input.text(), self.MIT_name_input.text()))

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
            self.markdown_filetree_input.setPlainText(gen_Filetree(self.file_tree.get_markdown_tree()))
            self.description_input.setPlainText(self.extract_description())

    # 提取当前文件夹中 README 的 description
    def extract_description(self):
        file_path = self.folder_path_input.text() + '/README.md'

        try:
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
                    return ""
        except:
            pass

    # 发送到github仓库
    def git_send(self):
        # print(self.file_tree.get_markdown_tree())
        # return

        # 切换到用户指定的文件夹
        dir = self.folder_path_input.text() 
        if os.path.exists(dir):
            os.chdir(dir)
        else:
            QMessageBox.information(self, "Message", "Please select a folder")
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
    def file_tree_handle_item_changed(self, item, column):
        # 处理选项状态改变时的逻辑
        if item.childCount() > 0:  # 只处理文件夹
            if item.checkState(0) == 0:  # 如果母选项未选中，则禁用子选项的选择功能
                for i in range(item.childCount()):
                    child_item = item.child(i)
                    child_item.setCheckState(0, 0)
                    child_item.setDisabled(True)
            elif item.checkState(0) == 2:  # 如果母选项选中，则开启子选项的选择功能
                for i in range(item.childCount()):
                    child_item = item.child(i)
                    child_item.setDisabled(False)
                    if child_item.text(0) != '.git':
                        child_item.setCheckState(0, 2)

        # 根据用户的选择改变markdown_filetree_input
        self.markdown_filetree_input.setPlainText(gen_Filetree(self.file_tree.get_markdown_tree()))

    # 将ContentTree类的handle_item_changed函数移到这里：content_tree选项的选择要影响窗口部件
    def content_tree_handle_item_changed(self, item, column):
        # 处理选项状态改变时的逻辑
        if item.childCount() > 0:  # 只处理文件夹
            if item.checkState(0) == 0:  # 如果母选项未选中，则禁用子选项的选择功能
                for i in range(item.childCount()):
                    child_item = item.child(i)
                    child_item.setCheckState(0, 0)
                    child_item.setDisabled(True)
            elif item.checkState(0) == 2:  # 如果母选项选中，则开启子选项的选择功能
                for i in range(item.childCount()):
                    child_item = item.child(i)
                    child_item.setDisabled(False)
                    child_item.setCheckState(0, 2)

        self.update_form_layout(self.content_tree.get_items_state())

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
            self.add_grid(self.about_label)
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

    # 生成 README.md
    def generate_readme(self):
        self.contents = self.content_tree.get_items_state()
        username = self.username_input.text()
        repo_name = self.repo_input.currentText()
        self.readme_content = ''

        # 生成 README.md 的 Head 部分
        if self.contents.get('Head'):
            title = self.title_input.text()
            description = self.description_input.toPlainText()
            self.readme_content += gen_Head(username, repo_name, title, description)
        # 生成 README.md 的 Contents 部分
        if self.contents.get('Contents'):
            self.readme_content += gen_Contents(self.contents)
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
            self.readme_content += gen_Foot(username, repo_name)

        self.markdown_display = Markdown_display()
        self.markdown_display.markdown_show(self.readme_content, self.MIT_input.toPlainText(), self.folder_path_input.text(), self.contents)
        self.markdown_display.show()
        # self.copy_images_folder()







# 生成 README.md 的 Head 部分
def gen_Head(username, repo_name, title, description):
    return f"""<div id="top"></div>

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
# def gen_Contents(contents):
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
def gen_Contents(contents):
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
def gen_Filetree(Filetree):
    return f"""
<!-- FILE TREE -->
## File Tree

```
{Filetree}
```

"""

# 生成 README.md 的 About The Project 部分
def gen_About_The_Project():
    return f"""<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Here's a blank template to get started: To avoid retyping too much info. Do a search and replace with your text editor for the following: `github_username`, `repo_name`, `twitter_handle`, `linkedin_username`, `email_client`, `email`, `project_title`, `project_description`

"""

# 生成 README.md 的 Build 部分
def gen_Build():
    return f"""### Built With

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
def gen_Getting_Started():
    return f"""<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.
"""

# 生成 README.md 的 Prerequisites 部分
def gen_Prerequisites():
    return f"""### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```
<p align="right">(<a href="#top">top</a>)</p>
"""

# 生成 README.md 的 Installation 部分
def gen_Installation():
    return f"""### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

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
def gen_Usage():
    return f"""<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#top">top</a>)</p>

"""

# 生成 README.md 的 Roadmap 部分
def gen_Roadmap():
    return f"""<!-- ROADMAP -->
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
def gen_Verison():
    return f"""<!-- Version -->
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
def gen_Contributing():
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
def gen_License():
    return f"""
<!-- LICENSE -->
## License
Distributed under the MIT License. See `LICENSE` for more information.
<p align="right">(<a href="#top">top</a>)</p>

"""

# 生成 MIT licsense
def gen_MIT(year=datetime.now().year, author_name='MoonGrt'):
    return f"""MIT License

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
def gen_Contact(username, repo_name, mail_address):
    return f"""
<!-- CONTACT -->
## Contact
{username} - {mail_address}
Project Link: [{username}/{repo_name}](https://github.com/{username}/{repo_name})
<p align="right">(<a href="#top">top</a>)</p>

"""

# 生成 README.md 的 Acknowledgments 部分
def gen_Acknowledgments():
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
def gen_Foot(username, repo_name):
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
    app = QApplication(sys.argv)
    window = App_window()
    window.show()
    sys.exit(app.exec_())

# TODO: 如果文件夹下有 README 则将相应内容填充到窗口
# TODO: 自动识别仓库名
# TODO: 添加对git异常的处理：fatal: detected dubious ownership in repository at 'U:/xxx'
#       添加 ”git config --global --add safe.directory U:/xxx“