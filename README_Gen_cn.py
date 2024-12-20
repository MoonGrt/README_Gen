import sys, os, subprocess, requests, shutil
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QPlainTextEdit, QFrame, QGridLayout, QComboBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFileDialog, QScrollArea, QSizePolicy, QMessageBox, QMainWindow, QAction
from PyQt5.QtGui import QIcon, QImage
from PyQt5.QtCore import Qt
from datetime import datetime
from Markdown import Markdown
from FileTree import FileTree
from ContentTree import ContentTree
from README_temple import README_temple
from PicText import PicText

class App_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.content_tree = ContentTree('目录')
        self.file_tree = FileTree('文件树')
        self.Markdown = Markdown()
        self.README_temple = README_temple('cn')
        self.aboutgen_window = PicText()

        self.project_path = ''
        self.readme_content = ''
        self.contents = {}
        self.init_ui()

    def init_ui(self):
        # 设置主窗口属性
        self.resize(1000, 850)
        self.setWindowTitle('README.md 生成软件')
        self.setWindowIcon(QIcon('Document/images/icons/markdown.svg'))

        self.create_menu()
        self.add_sections()
        self.get_repoinfo()

        # 左侧布局
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.content_tree)
        left_layout.addWidget(self.file_tree)

        # 右侧布局
        self.grid_layout = QGridLayout(self)  # warning: QLayout: Attempting to add QLayout "" to App_window "", which already has a layout
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


        # 总体布局 左右  # 使用 QStackedWidget 进行页面切换
        central_widget = QWidget()  # 创建一个中央部件
        layout = QHBoxLayout(central_widget)
        layout.addLayout(left_layout, 1)
        layout.addLayout(right_layout, 3)
        self.setCentralWidget(central_widget)  # 使用 setCentralWidget 而不是 setLayout


    # 组件
    def add_sections(self):
        # 基本信息
        self.username_label = QLabel('GitHub 用户名:')
        self.username_input = QLineEdit()
        self.repo_label = QLabel('仓库名:')
        self.repo_input = QComboBox(self)
        self.mail_label = QLabel('邮箱:')
        self.mail_input = QLineEdit()
        self.folder_path_label = QLabel('项目路径:')
        self.folder_path_input = QLineEdit()
        self.browse_button = QPushButton('浏览', self)
        self.browse_button.clicked.connect(self.browse_folder)
        # Head 信息
        self.title_label = QLabel('项目名称:')
        self.title_input = QLineEdit()
        self.description_label = QLabel('项目简介:')
        self.description_input = QPlainTextEdit()
        self.description_input.setFixedHeight(80)  # 200
        # File tree 信息
        self.markdown_filetree_label = QLabel('文件树:')
        self.filetree_input = QPlainTextEdit()
        self.filetree_input.setFixedHeight(200)
        # About The Project 信息
        self.about_label = QLabel('关于本项目:')
        self.about_input = PicText()
        self.about_input.setFixedHeight(800)
        # Build with 信息
        self.buildwith_label = QLabel('构建工具:')
        self.buildwith_input = QPlainTextEdit()
        self.buildwith_input.setFixedHeight(200)
        # Getting Started 信息
        self.start_label = QLabel('开始:')
        self.start_input = QPlainTextEdit()
        self.start_input.setFixedHeight(200)
        # Prerequisites 信息
        self.prerequisites_label = QLabel('依赖:')
        self.prerequisites_input = QPlainTextEdit()
        self.prerequisites_input.setFixedHeight(200)
        # Installation 信息
        self.installation_label = QLabel('安装:')
        self.installation_input = QPlainTextEdit()
        self.installation_input.setFixedHeight(200)
        # Usage 信息
        self.usage_label = QLabel('使用方法:')
        self.usage_input = QPlainTextEdit()
        self.usage_input.setFixedHeight(200)
        # Roadmap 信息
        self.roadmap_label = QLabel('路线图:')
        self.roadmap_input = QPlainTextEdit()
        self.roadmap_input.setFixedHeight(200)
        # Version 信息
        self.version_label = QLabel('版本:')
        self.version_input = QPlainTextEdit()
        self.version_input.setFixedHeight(200)
        # Contributing 信息
        self.contributing_label = QLabel('贡献:')
        self.contributing_input = QPlainTextEdit()
        self.contributing_input.setFixedHeight(200)
        # License 信息
        self.license_label = QLabel('许可证:')
        self.license_input = QPlainTextEdit()
        self.license_input.setFixedHeight(200)
        self.MIT_date_label = QLabel('时间:')
        self.MIT_date_input = QLineEdit()
        self.MIT_name_label = QLabel('名字:')
        self.MIT_name_input = QLineEdit()
        self.MIT_label = QLabel('MIT:')
        self.MIT_input = QPlainTextEdit()
        self.MIT_input.setFixedHeight(200)
        # Contact 信息
        self.contact_label = QLabel('联系我们:')
        self.contact_input = QPlainTextEdit()
        self.contact_input.setFixedHeight(200)
        # Acknowledgements 信息
        self.acknowledgements_label = QLabel('致谢:')
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

        # 信息链接
        self.username_input.textChanged.connect(self.handle_username_change)
        self.repo_input.currentIndexChanged.connect(self.handle_repo_change)
        self.mail_input.textChanged.connect(self.handle_mail_change)
        self.title_input.textChanged.connect(self.handle_title_change)
        self.MIT_name_input.textChanged.connect(self.handle_MIT_name_change)
        self.MIT_date_input.textChanged.connect(self.handle_MIT_name_change)

        # 生成、发送按钮
        self.confirm_button = QPushButton('生成', self)
        self.confirm_button.clicked.connect(self.GEN)
        self.git_send_button = QPushButton('Git 发送', self)
        self.git_send_button.clicked.connect(self.git_send)

        # 内容目录
        self.content_tree.add_items("README.md", [("头", [], True),
                                               ("目录", [], True),
                                               ("文件树", [], True),
                                               ("关于本项目", ["构建工具"], True),
                                               ("开始", ["依赖", "安装"]),
                                               ("使用方法", []),
                                               ("路线图", []),
                                               ("版本", []),
                                               ("贡献", [], True),
                                               ("许可证", [], True),
                                               ("联系我们", [], True),
                                               ("致谢", [], True)], True, True)  # parent child checked expanded
        self.content_tree.add_items(".gitignore", [], True)
        self.content_tree.add_items("LIECENSE", [], True)
        self.content_tree.add_items("requirements.txt")
        self.content_tree.add_items("run.bat")
        self.content_tree.itemChanged.connect(self.handle_contenttree_changed)

        # 文件树
        self.file_tree.itemChanged.connect(self.handle_filetree_changed)

    def create_menu(self):
        # 文件菜单
        file_Menu = self.menuBar().addMenu('文件')

        insert_Action = QAction(QIcon('Document/images/icons/insert.svg'), '插入', self)  # 插入动作
        insert_Action.setToolTip('Insert')
        insert_Action.triggered.connect(self.insert_file)
        file_Menu.addAction(insert_Action)
        open_Action = QAction(QIcon('Document/images/icons/open.svg'), '打开', self)  # 打开动作
        open_Action.setToolTip('Open')
        open_Action.triggered.connect(self.browse_folder)
        file_Menu.addAction(open_Action)
        close_Action = QAction(QIcon('Document/images/icons/close.svg'), '关闭', self)  # 关闭动作
        close_Action.setToolTip('Close')
        close_Action.triggered.connect(self.close_folder)
        file_Menu.addAction(close_Action)
        file_Menu.addSeparator()  # 分隔线
        save_Action = QAction(QIcon('Document/images/icons/save.svg'), '保存', self)  # 保存动作
        save_Action.setToolTip('Save')
        save_Action.triggered.connect(self.GEN)
        file_Menu.addAction(save_Action)
        exit_Action = QAction(QIcon('Document/images/icons/exit.svg'), '退出', self)  # 退出动作
        exit_Action.setToolTip('Exit')
        exit_Action.triggered.connect(self.close)
        file_Menu.addAction(exit_Action)

        # 编辑菜单
        edit_Menu = self.menuBar().addMenu('编辑')

        undo_Action = QAction(QIcon('Document/images/icons/undo.svg'), '撤销', self) # 撤销操作
        undo_Action.setToolTip('Undo')
        # undo_Action.triggered.connect(self.undo)
        edit_Menu.addAction(undo_Action)
        redo_Action = QAction(QIcon('Document/images/icons/redo.svg'), '重做', self) # 重做操作
        redo_Action.setToolTip('Redo')
        # redo_Action.triggered.connect(self.redo)
        edit_Menu.addAction(redo_Action)
        edit_Menu.addSeparator()  # 分隔线
        cut_Action = QAction(QIcon('Document/images/icons/cut.svg'), '剪切', self) # 剪切操作
        cut_Action.setToolTip('Cut')
        # cut_Action.triggered.connect(self.cut)
        edit_Menu.addAction(cut_Action)
        copy_Action = QAction(QIcon('Document/images/icons/copy.svg'), '复制', self) # 复制操作
        copy_Action.setToolTip('Copy')
        # copy_Action.triggered.connect(self.copy)
        edit_Menu.addAction(copy_Action)
        paste_Action = QAction(QIcon('Document/images/icons/paste.svg'), '粘贴', self) # 粘贴操作
        paste_Action.setToolTip('Paste')
        # paste_Action.triggered.connect(self.paste)
        edit_Menu.addAction(paste_Action)
        mode_Action = QAction(QIcon('Document/images/icons/mode.svg'), '模式', self) # 模式操作
        mode_Action.setToolTip('Mode')
        mode_Action.triggered.connect(self.mode)
        edit_Menu.addAction(mode_Action)

        # 工具栏
        toolbar1 = self.addToolBar('Toolbar1')
        toolbar1.addAction(insert_Action)
        toolbar1.addAction(open_Action)
        toolbar1.addAction(close_Action)
        toolbar1.addAction(save_Action)

        toolbar2 = self.addToolBar('Toolbar2')
        toolbar2.addAction(undo_Action)
        toolbar2.addAction(redo_Action)
        toolbar2.addAction(cut_Action)
        toolbar2.addAction(copy_Action)
        toolbar2.addAction(paste_Action)
        toolbar2.addAction(mode_Action)

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
        self.contact_input.setPlainText(self.README_temple.gen_Contact(self.username_input.text(), self.repo_input.currentText(), self.mail_input.text()))

    # 处理 title 变化
    def handle_title_change(self, new_text):
        index = self.repo_input.findText(new_text)
        if index == -1:
            self.repo_input.setCurrentIndex(-1)
            self.title_input.setText(new_text)
        else:
            self.repo_input.setCurrentIndex(index)

    # 处理 mail 变化
    def handle_mail_change(self, new_text):
        self.contact_input.setPlainText(self.README_temple.gen_Contact(self.username_input.text(), self.repo_input.currentText(), self.mail_input.text()))

    # 处理 MIT_date 变化
    def handle_MIT_date_change(self, new_text):
        self.MIT_input.setPlainText(self.README_temple.gen_MIT(self.MIT_date_input.text(), self.MIT_name_input.text()))

    # 处理 MIT_name 变化
    def handle_MIT_name_change(self, new_text):
        self.MIT_input.setPlainText(self.README_temple.gen_MIT(self.MIT_date_input.text(), self.MIT_name_input.text()))

    # 将 ContentTree 类的 handle_item_changed 函数移到这里：content_tree选项的选择要影响窗口部件
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

    # 将 FileTree 类的 handle_item_changed 函数移到这里：file_tree选项的选择要影响窗口内容
    def handle_filetree_changed(self, item, column):
        # 处理选项状态改变时的逻辑
        if item.childCount() > 0 and (item.text(0) != '.git'):  # 只处理文件夹
            if item.checkState(0) == 0:
                for i in range(item.childCount()):
                    child_item = item.child(i)
                    child_item.setCheckState(0, 0)  # 如果母选项未选中，则禁用子选项的选择功能
                    child_item.setDisabled(True)
            elif item.checkState(0) == 2:
                if item.childCount() < 20:
                    for i in range(item.childCount()):
                        child_item = item.child(i)
                        child_item.setDisabled(False)
                        child_item.setCheckState(0, 2)  # 如果母选项选中，则开启子选项的选择功能
                else:
                    for i in range(item.childCount()):
                        child_item = item.child(i)
                        child_item.setDisabled(False)
        # 根据用户的选择改变 filetree_input
        self.filetree_input.setPlainText(self.file_tree.get_filetree())

    # 设置每列的宽度比例
    def set_gridcolwidth_ratios(self, ratios):
        for col, ratio in enumerate(ratios):
            self.grid_layout.setColumnStretch(col, ratio)

    def get_repoinfo(self):
        url = f"https://api.github.com/users/{self.username_input.text()}/repos"
        response = requests.get(url)

        if response.status_code == 200:
            repositories = response.json()
            # repo_input 信息填充
            # 获取用户仓库列表
            if repositories:
                for repo in repositories:
                    self.repo_input.addItem(repo["name"])
        else:
            print(f"Error: Unable to fetch repositories. Status code: {response.status_code}")

    # 浏览文件夹
    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select File or Folder")
        if folder_path:
            self.project_path = folder_path
            self.folder_path_input.setText(folder_path)

            self.file_tree.clear()
            self.file_tree.add_items(self.file_tree.root, folder_path)
            self.README_temple.extract_contents(self.folder_path_input.text() + '/README_cn.md')

            # 向 GUI 填入文字
            if not self.README_temple.filetree:
                self.README_temple.set_filetree(self.file_tree.get_filetree())
            else:
                self.file_tree.set_filetree(self.README_temple.filetree)

            index = self.repo_input.findText(self.README_temple.pro_name)
            if index == -1:
                self.repo_input.setCurrentIndex(-1)
                self.title_input.setText(self.README_temple.pro_name)
            else:
                self.repo_input.setCurrentIndex(index)

            self.description_input.setPlainText(self.README_temple.description)

            self.filetree_input.setPlainText(self.README_temple.filetree)
            self.about_input.setHtml(self.add_path(self.README_temple.about))
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

    def add_path(self, text):
        return text.replace('<img src="', f'<img src="{self.project_path}/')

    def insert_file(self):
        image_path, _ = QFileDialog.getOpenFileName(self, '打开文件', '', '图片 (*.jpg *.png *.bmp)')
        if image_path:
            image = QImage(image_path)
            if image.isNull():
                return  # 如果无法加载图像，则返回
            else:
                pass

    def close_folder(self):
        self.project_path = ''
        self.readme_content = ''
        self.contents = {}
        self.folder_path_input.clear()
        self.title_input.clear()
        self.description_input.clear()
        self.filetree_input.clear()
        self.about_input.clear()
        self.buildwith_input.clear()
        self.start_input.clear()
        self.prerequisites_input.clear()
        self.installation_input.clear()
        self.usage_input.clear()
        self.roadmap_input.clear()
        self.version_input.clear()
        self.contributing_input.clear()
        self.license_input.clear()
        self.MIT_input.clear()
        self.contact_input.clear()
        self.acknowledgements_input.clear()
        self.file_tree.clear_tree()

    def mode(self):
        pass

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
            # 是否开启 头
            if contents.get('头'):
                self.add_grid(self.title_label, self.title_input)
                self.add_grid(self.description_label)
                self.add_grid(self.description_input)
                self.add_grid()
            # 是否开启 目录
            if contents.get('目录'):
                pass
            # 是否开启 文件树
            if contents.get('文件树'):
                self.add_grid(self.markdown_filetree_label)
                self.add_grid(self.filetree_input)
                self.file_tree.setEnabled(True)
                self.add_grid()
            else:
                self.file_tree.setEnabled(False)
            # 是否开启 关于本项目
            if contents.get('关于本项目'):
                self.add_grid(self.about_label)
                self.add_grid(self.about_input)
                self.add_grid()
                if contents.get('构建工具'):
                    self.add_grid(self.buildwith_label)
                    self.add_grid(self.buildwith_input)
                    self.add_grid()
            # 是否开启 开始
            if contents.get('开始'):
                self.add_grid(self.start_label)
                self.add_grid(self.start_input)
                self.add_grid()
                if contents.get('依赖'):
                    self.add_grid(self.prerequisites_label)
                    self.add_grid(self.prerequisites_input)
                    self.add_grid()
                if contents.get('安装'):
                    self.add_grid(self.installation_label)
                    self.add_grid(self.installation_input)
                    self.add_grid()
            # 是否开启 使用方法
            if contents.get('使用方法'):
                self.add_grid(self.usage_label)
                self.add_grid(self.usage_input)
                self.add_grid()
            # 是否开启 路线图
            if contents.get('路线图'):
                self.add_grid(self.roadmap_label)
                self.add_grid(self.roadmap_input)
                self.add_grid()
            # 是否开启 版本
            if contents.get('版本'):
                self.add_grid(self.version_label)
                self.add_grid(self.version_input)
                self.add_grid()
            # 是否开启 贡献
            if contents.get('贡献'):
                self.add_grid(self.contributing_label)
                self.add_grid(self.contributing_input)
                self.add_grid()
            # 是否开启 许可证
            if contents.get('许可证'):
                self.add_grid(self.license_label)
                self.add_grid(self.license_input)
                self.add_grid(self.MIT_label)
                self.add_grid(self.MIT_layout)
                self.add_grid(self.MIT_input)
                self.add_grid()
            # 是否开启 联系我们
            if contents.get('联系我们'):
                self.add_grid(self.contact_label)
                self.add_grid(self.contact_input)
                self.add_grid()
            # 是否开启 致谢
            if contents.get('致谢'):
                self.add_grid(self.acknowledgements_label)
                self.add_grid(self.acknowledgements_input)
                self.add_grid()

        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.set_gridcolwidth_ratios([1, 2])

    def GEN(self):
        if self.content_tree.root.child(4).checkState(0) == 2:  # requirements.txt
            # 生成 requirements.txt
            self.generate_requirements()
        if self.content_tree.root.child(3).checkState(0) == 2:  # run.bat
            # 生成 run.bat
            self.generate_run_bat()
        if self.content_tree.root.child(2).checkState(0) == 2:  # LIENCE
            # 生成 LIENCE
            self.generate_LIENCE()
        if self.content_tree.root.child(1).checkState(0) == 2:  # .gitignore
            # 生成 .gitignore
            self.generate_gitignore()
        if self.content_tree.root.child(0).checkState(0) == 2:  # README.md
            # 生成 README.md
            self.contents = self.content_tree.get_tree_content()
            self.readme_content = self.generate_markdown(self.contents)

            self.Markdown.confirm_button.clicked.connect(self.markdown_confirm)
            self.Markdown.markdown_show(self.readme_content, self.folder_path_input.text())

    def markdown_confirm(self):
        if self.project_path:
            self.copy_images()
            # 将 readme_content 内容保存到文件中
            readme_path = self.project_path + '/README_cn.md'
            with open(readme_path, 'w', encoding='utf-8') as readme_file:
                readme_file.write(self.Markdown.markdown)
            print(f"README.md generated successfully at {readme_path}")
        else:
            QMessageBox.information(self, "Message", "Please select a folder")
        self.Markdown.close()

    def copy_images(self):
        destination_folder = os.path.join(self.project_path, 'Document/images')  # 目标文件夹的 images 目录
        destination_path = os.path.join(destination_folder, 'logo.png')  # 定义目标文件路径
        if not os.path.exists(destination_path):
            source_path = os.path.join(os.getcwd(), 'Document/images', 'logo.png')  # 当前文件夹下 Document/images/logo.png
            # 确保目标文件夹存在，如果不存在则创建
            os.makedirs(destination_folder, exist_ok=True)
            try:
                # 复制文件
                shutil.copy(source_path, destination_path)
                print(f'Images copied to {destination_path}')
            except shutil.Error as e:
                print(f"Copy 'images' error: {e}")
            except Exception as e:
                print(f"{e}")
        # else:
        #     print("logo.png already existed")

    def generate_markdown(self, content):
        markdown_text = ""
        for title, level, is_checked in content:
            if not level:  # 舍弃第一层
                continue
            if is_checked:
                # Add the section title with corresponding heading level
                if title == "头":
                    markdown_text += self.README_temple.gen_englishlink() + '\n'
                    markdown_text += self.README_temple.gen_topid() + '\n'
                elif title == "目录":
                    pass
                else:
                    markdown_text += f"<!-- {title.upper()} -->\n"
                    markdown_text += f"{'#' * (level+1)} {title}\n\n"
                markdown_text += self.generate_sections(title) + '\n\n\n\n'
        link = self.README_temple.gen_Link(self.username_input.text(), self.repo_input.currentText())
        # link += 
        return markdown_text + link

    def generate_sections(self, section):
        # 生成 README.md 的 头 部分
        if section == '头':
            title = self.title_input.text()
            description = self.description_input.toPlainText()
            return self.README_temple.gen_Head(self.username_input.text(), self.repo_input.currentText(), title, description)
        # 生成 README.md 的 Contents 部分
        if section == '目录':
            return self.README_temple.gen_Contents(self.content_tree.get_items_state())
        # 生成 README.md 的 文件树 部分
        if section == '文件树':
            return "```\n" + self.filetree_input.toPlainText() + "\n```"
        # 生成 README.md 的 关于本项目 部分
        if section == '关于本项目':
            return self.get_about() + '\n' + self.README_temple.gen_toplink()
        if section == '构建工具':
            return self.buildwith_input.toPlainText() + '\n' + self.README_temple.gen_toplink()
        # 生成 README.md 的 开始 部分
        if section == '开始':
            return self.start_input.toPlainText() + '\n' + self.README_temple.gen_toplink()
        if section == '依赖':
            return self.prerequisites_input.toPlainText() + '\n' + self.README_temple.gen_toplink()
        if section == '安装':
            return self.installation_input.toPlainText() + '\n' + self.README_temple.gen_toplink()
        # 生成 README.md 的 使用方法 部分
        if section == '使用方法':
            return self.usage_input.toPlainText() + '\n' + self.README_temple.gen_toplink()
        # 生成 README.md 的 路线图 部分
        if section == '路线图':
            return self.roadmap_input.toPlainText() + '\n' + self.README_temple.gen_toplink()
        # 生成 README.md 的 版本 部分
        if section == '版本':
            return self.version_input.toPlainText() + '\n' + self.README_temple.gen_toplink()
        # 生成 README.md 的 贡献 部分
        if section == '贡献':
            return self.contributing_input.toPlainText() + '\n' + self.README_temple.gen_toplink()
        # 生成 README.md 的 许可证 部分
        if section == '许可证':
            return self.license_input.toPlainText() + '\n' + self.README_temple.gen_toplink()
        # 生成 README.md 的 联系我们 部分
        if section == '联系我们':
            return self.contact_input.toPlainText() + '\n' + self.README_temple.gen_toplink()
        # 生成 README.md 的 致谢 部分
        if section == '致谢':
            return self.acknowledgements_input.toPlainText() + '\n' + self.README_temple.gen_toplink()

    def get_about(self):
        about_html = self.about_input.toHtml()
        about_html = about_html.replace(self.project_path + '/', '')  # 删除图片的路径
        about_html = about_html.splitlines()  # 将字符串按行分割成列表
        about_html = '\n'.join(about_html[4:])  # 跳过前四行
        return about_html

    def generate_LIENCE(self):
        if self.project_path:
            if not os.path.exists(self.project_path + '/LICENSE'):
                # 将 License 内容保存到文件中
                license_path = self.project_path + '/LICENSE'
                with open(license_path, 'w', encoding='utf-8') as license_file:
                    license_file.write(self.MIT_input.toPlainText())
                print(f"LICENSE generated successfully at {license_path}")
            # else:
            #     print("LICENSE already existed")
        else:
            print("Please select a folder")
    # TODO: 选择许可证模板

    def generate_requirements(self, path='.'):
        subprocess.run(['pipreqs', path, '--force'], check=True)

    def generate_run_bat(self):
        # TODO: 有问题
        batch_content = f"@echo off\npython {os.path.abspath(__file__)}"
        print(batch_content)
        with open('run.bat', 'w') as file:
            file.write(batch_content)

    def generate_gitignore(self):
        if self.project_path:
            if not os.path.exists(self.project_path + '/.gitignore'):
                # 将 License 内容保存到文件中
                license_path = self.project_path + '/.gitignore'
                with open(license_path, 'w', encoding='utf-8') as license_file:
                    pass
                print(f".gitignore generated successfully at {license_path}")
            # else:
            #     print(".gitignore already existed")
        else:
            print("Please select a folder")
    # TODO: 用户界面选择哪些文件忽略


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App_window()
    window.show()
    sys.exit(app.exec_())


# TODO: 添加release版本控制
# TODO: 再次打开时，图片路径有问题，无法显示
