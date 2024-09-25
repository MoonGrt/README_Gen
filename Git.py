import sys, os, subprocess, requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QPlainTextEdit, QFrame, QGridLayout, QComboBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFileDialog, QScrollArea, QSizePolicy, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from datetime import datetime

class App_window(QWidget):
    def __init__(self):
        super().__init__()
        self.readme_content = ''
        self.contents = {}
        self.init_ui()

    def init_ui(self):
        # 设置主窗口属性
        self.resize(600, 500)
        self.setWindowTitle('Git')
        self.setWindowIcon(QIcon('images/icons/markdown.svg'))

        # 基本信息
        self.username_label = QLabel('GitHub Username:')
        self.username_input = QLineEdit()
        self.repo_label = QLabel('Repository Name:')
        self.repo_input = QComboBox(self)
        self.mail_label = QLabel('Mail address:')
        self.mail_input = QLineEdit()
        self.folder_path_label = QLabel('Folder Path:')
        self.folder_path_input = QLineEdit()
        self.browse_button = QPushButton('Browse', self)
        self.browse_button.clicked.connect(self.browse_folder)
        # License 信息
        self.MIT_date_label = QLabel('Date:')
        self.MIT_date_input = QLineEdit()
        self.MIT_name_label = QLabel('Name:')
        self.MIT_name_input = QLineEdit()
        self.MIT_label = QLabel('MIT:')
        self.MIT_input = QPlainTextEdit()
        self.MIT_input.setFixedHeight(200)

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

        # 信息链接
        # self.username_input.textChanged.connect(self.handle_username_change)
        # self.repo_input.currentIndexChanged.connect(self.handle_repo_change)
        # self.mail_input.textChanged.connect(self.handle_mail_change)
        # self.MIT_name_input.textChanged.connect(self.handle_MIT_name_change)
        # self.MIT_date_input.textChanged.connect(self.handle_MIT_name_change)

        # 生成、发送按钮
        self.git_send_button = QPushButton('Git Send', self)
        self.git_send_button.clicked.connect(self.git_send)


        # 右侧布局
        self.grid_layout = QGridLayout(self)
        self.update_form_layout()
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.set_gridcolwidth_ratios([1, 2])

        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.grid_layout)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.git_send_button)

        right_layout = QVBoxLayout()
        right_layout.addWidget(scroll_area)
        right_layout.addLayout(bottom_layout)


        # 总体布局
        self.setLayout(right_layout)


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

    # 根据用户选择的内容更新窗口
    def update_form_layout(self):
        # 清空self.grid_layout
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                # 移除组件，但保留widget
                self.grid_layout.removeWidget(widget)
                widget.setParent(None)

        # 添加基础内容
        self.add_grid(self.username_label, self.username_input)
        self.add_grid(self.repo_label, self.repo_input)
        self.add_grid(self.mail_label, self.mail_input)
        self.add_grid(self.folder_path_label, self.browse_button)
        self.add_grid(self.folder_path_input)
        self.add_grid()

        # lience
        self.add_grid(self.MIT_label)
        self.add_grid(self.MIT_layout)
        self.add_grid(self.MIT_input)
        self.add_grid()

        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.set_gridcolwidth_ratios([1, 2])

    # 浏览文件夹
    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select File or Folder")
        if folder_path:
            self.folder_path_input.setText(folder_path)
    # TODO: 根据README 的 file_tree 勾选相应内容

    def get_repoinfo(self):
        url = f"https://api.github.com/users/{self.username_input.text()}/repos"
        response = requests.get(url)

        if response.status_code == 200:
            repositories = response.json()
            return repositories
        else:
            print(f"Error: Unable to fetch repositories. Status code: {response.status_code}")
            return None

    # 设置每列的宽度比例
    def set_gridcolwidth_ratios(self, ratios):
        for col, ratio in enumerate(ratios):
            self.grid_layout.setColumnStretch(col, ratio)

    # 发送到github仓库
    def git_send(self):
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App_window()
    window.show()
    sys.exit(app.exec_())
